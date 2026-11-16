// Worker de pedidos de Scantalia (scantalia.com/api/*).
// - POST /api/pedido: valida el pedido, calcula el total con los precios públicos de la tienda
//   (no con lo que mande el navegador), lo guarda en la base de datos y crea el cobro en Stripe.
// - POST /api/stripe: aviso de Stripe (webhook) cuando un pago se completa; marca el pedido como pagado.
// Secretos (se guardan en Cloudflare, nunca en este archivo): STRIPE_SECRET y STRIPE_WEBHOOK_SECRET.

const SITIO = "https://scantalia.com";
const ORIGENES = [SITIO, "https://www.scantalia.com"];
const CATALOGO_URL = SITIO + "/tienda.json";
const MAX_PEDIDOS_POR_IP = 5;      // por cada 15 minutos
const MINIMO_STRIPE = 10;          // Stripe no cobra menos de $10 MXN
const PRUEBA = { id: "prueba-scantalia", n: "Scantalia Prueba (producto de prueba)", d: true, p: { "120": 0.01 } };

const ESTADOS = [[1,16,"Ciudad de México"],[20,20,"Aguascalientes"],[21,22,"Baja California"],[23,23,"Baja California Sur"],[24,24,"Campeche"],[25,27,"Coahuila"],[28,28,"Colima"],[29,30,"Chiapas"],[31,33,"Chihuahua"],[34,35,"Durango"],[36,38,"Guanajuato"],[39,41,"Guerrero"],[42,43,"Hidalgo"],[44,49,"Jalisco"],[50,57,"Estado de México"],[58,61,"Michoacán"],[62,62,"Morelos"],[63,63,"Nayarit"],[64,67,"Nuevo León"],[68,71,"Oaxaca"],[72,75,"Puebla"],[76,76,"Querétaro"],[77,77,"Quintana Roo"],[78,79,"San Luis Potosí"],[80,82,"Sinaloa"],[83,85,"Sonora"],[86,86,"Tabasco"],[87,89,"Tamaulipas"],[90,90,"Tlaxcala"],[91,96,"Veracruz"],[97,97,"Yucatán"],[98,99,"Zacatecas"]];
const Z_LOCAL = ["Ciudad de México", "Estado de México"];
const Z_EXT = ["Baja California", "Baja California Sur", "Chiapas", "Quintana Roo", "Yucatán"];

const JSON_H = { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" };
const resp = (datos, estado = 200) => new Response(JSON.stringify(datos), { status: estado, headers: JSON_H });
const txt = (v, max) => String(v ?? "").trim().slice(0, max);

let catalogo = null, catalogoHasta = 0;
async function leerCatalogo() {
  if (catalogo && Date.now() < catalogoHasta) return catalogo;
  const r = await fetch(CATALOGO_URL + "?t=" + Math.floor(Date.now() / 300000), { cf: { cacheTtl: 300 } });
  if (!r.ok) throw new Error("catalogo " + r.status);
  catalogo = await r.json();
  catalogoHasta = Date.now() + 5 * 60 * 1000;
  return catalogo;
}

function zonaDeCP(cp) {
  if (!/^\d{5}$/.test(cp)) return null;
  const n = Number(cp.slice(0, 2));
  const e = ESTADOS.find(([a, b]) => n >= a && n <= b);
  if (!e) return null;
  return { estado: e[2], key: Z_LOCAL.includes(e[2]) ? "local" : Z_EXT.includes(e[2]) ? "extendida" : "nacional" };
}

function nuevoFolio() {
  const d = new Date(Date.now() - 6 * 3600 * 1000); // hora de CDMX
  const dd = String(d.getUTCDate()).padStart(2, "0"), mm = String(d.getUTCMonth() + 1).padStart(2, "0");
  const azar = crypto.getRandomValues(new Uint32Array(1))[0] % 9000 + 1000;
  return `SC-${dd}${mm}-${azar}`;
}

async function crearPedido(request, env) {
  const origen = request.headers.get("Origin");
  if (origen && !ORIGENES.includes(origen)) return resp({ error: "Origen no permitido" }, 403);
  const largo = Number(request.headers.get("Content-Length") || 0);
  if (largo > 20000) return resp({ error: "Pedido demasiado grande" }, 413);
  let d;
  try { d = JSON.parse((await request.text()).slice(0, 20000)); } catch { return resp({ error: "Datos no válidos" }, 400); }

  const c = {
    nombre: txt(d.nombre, 100), tel: txt(d.tel, 10).replace(/\D/g, ""), correo: txt(d.correo, 120),
    calle: txt(d.calle, 120), colonia: txt(d.colonia, 80), cp: txt(d.cp, 5), destino: txt(d.destino, 80),
    ref: txt(d.ref, 150), notas: txt(d.notas, 300),
  };
  const zona = zonaDeCP(c.cp);
  if (c.nombre.length < 2 || c.tel.length !== 10 || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(c.correo) ||
      c.calle.length < 4 || c.colonia.length < 3 || c.destino.length < 3 || !zona) {
    return resp({ error: "Faltan datos de entrega o no son válidos" }, 400);
  }
  if (!Array.isArray(d.items) || d.items.length < 1 || d.items.length > 20) return resp({ error: "Carrito no válido" }, 400);

  const cat = await leerCatalogo();
  const lineas = [];
  for (const it of d.items) {
    const id = txt(it.id, 120), ml = String(Number(it.ml)), qty = Math.floor(Number(it.qty));
    const p = id === PRUEBA.id ? PRUEBA : cat.perfumes[id];
    if (!p || !p.d || !(ml in p.p) || !(qty >= 1 && qty <= 10)) return resp({ error: "Un perfume del carrito ya no está disponible. Actualice la página." }, 409);
    lineas.push({ id, nombre: `${p.n} ${ml} ml`, ml: Number(ml), cantidad: qty, precio: p.p[ml] });
  }
  const piezas = lineas.reduce((s, l) => s + l.cantidad, 0);
  const subtotal = Math.round(lineas.reduce((s, l) => s + l.precio * l.cantidad, 0) * 100) / 100;
  const envio = piezas >= cat.envio.gratisDesde ? 0 : cat.envio.zonas[zona.key];
  const total = Math.round((subtotal + envio) * 100) / 100;
  const esPrueba = lineas.some(l => l.id === PRUEBA.id) ? 1 : 0;

  const ip = request.headers.get("CF-Connecting-IP") || "";
  const recientes = await env.DB.prepare("SELECT COUNT(*) AS n FROM pedidos WHERE ip = ? AND creado_en > datetime('now', '-15 minutes')").bind(ip).first();
  if (recientes && recientes.n >= MAX_PEDIDOS_POR_IP) return resp({ error: "Demasiados pedidos seguidos. Intente en unos minutos." }, 429);

  const folio = nuevoFolio();
  const direccion = `${c.calle}, col. ${c.colonia}, ${c.destino}, ${zona.estado}` + (c.ref ? ` · Ref: ${c.ref}` : "");
  const cuenta = await sesionActual(request, env).catch(() => null);
  await env.DB.prepare(
    `INSERT INTO pedidos (folio, creado_en, estado, nombre, telefono, correo, direccion, codigo_postal, items, total, es_prueba, envio, notas, ip, cliente_id)
     VALUES (?, datetime('now'), 'pendiente_pago', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
  ).bind(folio, c.nombre, c.tel, c.correo, direccion, c.cp, JSON.stringify(lineas), total, esPrueba, envio, c.notas, ip, cuenta ? cuenta.id : null).run();

  let pagoUrl = null;
  if (env.STRIPE_SECRET && total >= MINIMO_STRIPE) {
    const f = new URLSearchParams();
    f.set("mode", "payment"); f.set("locale", "es-419"); f.set("customer_email", c.correo);
    f.set("client_reference_id", folio); f.set("metadata[folio]", folio); f.set("payment_intent_data[metadata][folio]", folio);
    f.set("success_url", `${SITIO}/?pago=ok&folio=${folio}`); f.set("cancel_url", `${SITIO}/?pago=cancelado&folio=${folio}`);
    const todas = envio > 0 ? [...lineas, { nombre: `Envío (${zona.estado})`, cantidad: 1, precio: envio }] : lineas;
    todas.forEach((l, i) => {
      f.set(`line_items[${i}][quantity]`, String(l.cantidad));
      f.set(`line_items[${i}][price_data][currency]`, "mxn");
      f.set(`line_items[${i}][price_data][unit_amount]`, String(Math.round(l.precio * 100)));
      f.set(`line_items[${i}][price_data][product_data][name]`, l.nombre);
    });
    const r = await fetch("https://api.stripe.com/v1/checkout/sessions", {
      method: "POST", body: f,
      headers: { Authorization: "Bearer " + env.STRIPE_SECRET, "Content-Type": "application/x-www-form-urlencoded", "Idempotency-Key": folio },
    });
    const s = await r.json().catch(() => ({}));
    if (r.ok && s.url) {
      pagoUrl = s.url;
      await env.DB.prepare("UPDATE pedidos SET stripe_session = ? WHERE folio = ?").bind(s.id, folio).run();
    }
  }
  return resp({ ok: true, folio, subtotal, envio, total, pagoUrl });
}

function hex(buf) { return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, "0")).join(""); }
function igual(a, b) { if (a.length !== b.length) return false; let x = 0; for (let i = 0; i < a.length; i++) x |= a.charCodeAt(i) ^ b.charCodeAt(i); return x === 0; }

async function avisoStripe(request, env) {
  if (!env.STRIPE_WEBHOOK_SECRET) return resp({ error: "Sin configurar" }, 503);
  const cuerpo = await request.text();
  const firma = request.headers.get("Stripe-Signature") || "";
  const partes = Object.fromEntries(firma.split(",").map(x => x.split("=")).filter(x => x.length === 2).map(([k, v]) => [k, v]));
  const v1s = firma.split(",").filter(x => x.startsWith("v1=")).map(x => x.slice(3));
  const t = Number(partes.t);
  if (!t || Math.abs(Date.now() / 1000 - t) > 300 || !v1s.length) return resp({ error: "Firma no válida" }, 400);
  const llave = await crypto.subtle.importKey("raw", new TextEncoder().encode(env.STRIPE_WEBHOOK_SECRET), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const esperado = hex(await crypto.subtle.sign("HMAC", llave, new TextEncoder().encode(`${t}.${cuerpo}`)));
  if (!v1s.some(v => igual(v, esperado))) return resp({ error: "Firma no válida" }, 400);

  const ev = JSON.parse(cuerpo);
  const s = ev.data && ev.data.object;
  if (s && (ev.type === "checkout.session.completed" || ev.type === "checkout.session.async_payment_succeeded") && s.payment_status === "paid") {
    await env.DB.prepare("UPDATE pedidos SET estado = 'pagado', pagado_en = datetime('now') WHERE folio = ? AND stripe_session = ?")
      .bind(s.metadata && s.metadata.folio, s.id).run();
  }
  if (s && ev.type === "checkout.session.async_payment_failed") {
    await env.DB.prepare("UPDATE pedidos SET estado = 'pago_fallido' WHERE folio = ? AND stripe_session = ?").bind(s.metadata && s.metadata.folio, s.id).run();
  }
  return resp({ recibido: true });
}

// ───────────────────────── Cuentas de clientes ─────────────────────────
// POST /api/cuenta/<accion>: crear, entrar, verificar, reenviar, olvide, nueva, sesion, salir. GET/POST estado.
// Contraseñas con PBKDF2-SHA256; códigos de 5 dígitos y tokens de sesión se guardan solo como hash.
// El código se envía por correo con Resend (secreto RESEND_KEY). Sin RESEND_KEY la cuenta queda desactivada.

const CODIGO_MIN = 10, REENVIO_S = 60, INTENTOS = 5, SESION_DIAS = 30, PBKDF2_IT = 100000;
const MAX_CODIGOS_HORA = 8;
const REMITENTE = "Scantalia Perfumería <codigos@scantalia.com>";
const COOKIE = "sc_sesion";

const b64 = buf => btoa(String.fromCharCode(...new Uint8Array(buf)));
const b64url = buf => b64(buf).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const deB64 = s => Uint8Array.from(atob(s), ch => ch.charCodeAt(0));
async function sha256(texto) { return hex(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(texto))); }

async function hashPass(pass, salB64) {
  const sal = salB64 ? deB64(salB64) : crypto.getRandomValues(new Uint8Array(16));
  const llave = await crypto.subtle.importKey("raw", new TextEncoder().encode(pass), "PBKDF2", false, ["deriveBits"]);
  const bits = await crypto.subtle.deriveBits({ name: "PBKDF2", hash: "SHA-256", salt: sal, iterations: PBKDF2_IT }, llave, 256);
  return `pbkdf2$${PBKDF2_IT}$${b64(sal)}$${b64(bits)}`;
}
async function passOk(pass, guardado) {
  const [tipo, , sal] = String(guardado || "").split("$");
  if (tipo !== "pbkdf2" || !sal) return false;
  return igual(await hashPass(pass, sal), guardado);
}

const correoOk = c => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(c);
const passValida = p => typeof p === "string" && p.length >= 8 && p.length <= 200 && /[A-Za-zÁÉÍÓÚáéíóúÑñ]/.test(p) && /\d/.test(p);
const hashCodigo = (correo, motivo, codigo) => sha256(`${correo.toLowerCase()}|${motivo}|${codigo}`);

function leerCookie(request, nombre) {
  const m = (request.headers.get("Cookie") || "").match(new RegExp(`(?:^|;\\s*)${nombre}=([^;]+)`));
  return m ? m[1] : "";
}
function cookieSesion(token, segundos) {
  return `${COOKIE}=${token}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${segundos}`;
}
function respCookie(datos, cookie, estado = 200) {
  return new Response(JSON.stringify(datos), { status: estado, headers: { ...JSON_H, "Set-Cookie": cookie } });
}

async function sesionActual(request, env) {
  const token = leerCookie(request, COOKIE);
  if (!token) return null;
  return await env.DB.prepare(
    `SELECT c.id, c.nombre, c.correo FROM sesiones s JOIN clientes c ON c.id = s.cliente_id
     WHERE s.token_hash = ? AND s.expira_en > datetime('now') AND c.estado = 'activo'`
  ).bind(await sha256(token)).first();
}

async function enviarCorreoCodigo(env, correo, codigo, motivo) {
  const asunto = { registro: "Confirme su cuenta en Scantalia", entrar: "Su código para iniciar sesión", recuperar: "Su código para cambiar la contraseña" }[motivo];
  const texto = `Su código de verificación es: ${codigo}\n\nVence en ${CODIGO_MIN} minutos. Si usted no lo pidió, ignore este correo; nadie podrá entrar a su cuenta sin este código.\n\nEl equipo de Scantalia\nhttps://scantalia.com`;
  const html = `<div style="font-family:Arial,Helvetica,sans-serif;max-width:480px;margin:0 auto;color:#1E1D1C">
    <p style="font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:#8C6A2E">Scantalia Perfumería</p>
    <p style="font-size:16px">Su código de verificación es:</p>
    <p style="font-size:34px;letter-spacing:.35em;font-weight:bold;margin:12px 0">${codigo}</p>
    <p style="font-size:14px;color:#555">Vence en ${CODIGO_MIN} minutos. Si usted no lo pidió, ignore este correo; nadie podrá entrar a su cuenta sin este código.</p>
    <p style="font-size:14px">El equipo de Scantalia</p></div>`;
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: "Bearer " + env.RESEND_KEY, "Content-Type": "application/json" },
    body: JSON.stringify({ from: REMITENTE, to: [correo], subject: asunto, text: texto, html }),
  });
  return r.ok;
}

// Genera un código nuevo (distinto del anterior), invalida los anteriores y lo envía.
async function nuevoCodigo(env, correo, motivo) {
  const hora = await env.DB.prepare("SELECT COUNT(*) AS n FROM codigos WHERE correo = ? AND creado_en > datetime('now', '-1 hour') AND codigo_hash NOT LIKE 'permiso:%'").bind(correo).first();
  if (hora && hora.n >= MAX_CODIGOS_HORA) return { error: "Pidió demasiados códigos. Intente en una hora.", estado: 429 };
  const ultimo = await env.DB.prepare("SELECT codigo_hash, creado_en FROM codigos WHERE correo = ? AND motivo = ? AND codigo_hash NOT LIKE 'permiso:%' ORDER BY id DESC LIMIT 1").bind(correo, motivo).first();
  let codigo;
  do { codigo = String(crypto.getRandomValues(new Uint32Array(1))[0] % 100000).padStart(5, "0"); }
  while (ultimo && ultimo.codigo_hash === await hashCodigo(correo, motivo, codigo));
  await env.DB.prepare("UPDATE codigos SET usado_en = datetime('now') WHERE correo = ? AND motivo = ? AND usado_en IS NULL").bind(correo, motivo).run();
  await env.DB.prepare(`INSERT INTO codigos (correo, motivo, codigo_hash, intentos, expira_en) VALUES (?, ?, ?, ?, datetime('now', '+${CODIGO_MIN} minutes'))`)
    .bind(correo, motivo, await hashCodigo(correo, motivo, codigo), INTENTOS).run();
  if (!(await enviarCorreoCodigo(env, correo, codigo, motivo))) {
    await env.DB.prepare("UPDATE codigos SET usado_en = datetime('now') WHERE correo = ? AND motivo = ? AND usado_en IS NULL").bind(correo, motivo).run();
    return { error: "No pudimos enviar el código. Intente en unos minutos.", estado: 502 };
  }
  return { ok: true };
}

async function abrirSesion(request, env, cliente) {
  const token = b64url(crypto.getRandomValues(new Uint8Array(32)));
  await env.DB.prepare(`INSERT INTO sesiones (token_hash, cliente_id, expira_en, ip) VALUES (?, ?, datetime('now', '+${SESION_DIAS} days'), ?)`)
    .bind(await sha256(token), cliente.id, request.headers.get("CF-Connecting-IP") || "").run();
  await env.DB.prepare("UPDATE clientes SET ultimo_acceso = datetime('now') WHERE id = ?").bind(cliente.id).run();
  await env.DB.prepare("DELETE FROM sesiones WHERE expira_en < datetime('now')").run();
  return token;
}

async function pedidosDe(env, cliente) {
  const r = await env.DB.prepare(
    `SELECT folio, creado_en, estado, total FROM pedidos
     WHERE (cliente_id = ? OR lower(correo) = lower(?)) AND es_prueba = 0 AND estado <> 'pendiente_pago'
     ORDER BY id DESC LIMIT 30`
  ).bind(cliente.id, cliente.correo).all();
  return r.results || [];
}

async function cuentaRuta(request, env, accion) {
  const listo = !!env.RESEND_KEY;
  if (accion === "estado") return resp({ listo });
  if (request.method !== "POST") return resp({ error: "Método no permitido" }, 405);
  const origen = request.headers.get("Origin");
  if (origen && !ORIGENES.includes(origen)) return resp({ error: "Origen no permitido" }, 403);
  if (Number(request.headers.get("Content-Length") || 0) > 4000) return resp({ error: "Datos demasiado grandes" }, 413);
  let d = {};
  try { d = JSON.parse((await request.text()).slice(0, 4000) || "{}"); } catch { return resp({ error: "Datos no válidos" }, 400); }
  const correo = txt(d.correo, 120).toLowerCase();

  if (accion === "sesion") {
    const c = await sesionActual(request, env);
    return resp({ ok: true, sesion: c ? { nombre: c.nombre, correo: c.correo, pedidos: await pedidosDe(env, c) } : null });
  }
  if (accion === "salir") {
    const token = leerCookie(request, COOKIE);
    if (token) await env.DB.prepare("DELETE FROM sesiones WHERE token_hash = ?").bind(await sha256(token)).run();
    return respCookie({ ok: true }, cookieSesion("", 0));
  }
  if (!listo) return resp({ error: "Las cuentas todavía no están disponibles." }, 503);

  if (accion === "crear") {
    const nombre = txt(d.nombre, 100);
    if (nombre.length < 2 || !correoOk(correo) || !passValida(d.pass)) return resp({ error: "Revise su nombre, su correo y su contraseña." }, 400);
    const existe = await env.DB.prepare("SELECT id, verificado FROM clientes WHERE correo = ?").bind(correo).first();
    if (existe && existe.verificado) return resp({ error: "Ya existe una cuenta con ese correo. Inicie sesión." }, 409);
    const hash = await hashPass(d.pass);
    if (existe) await env.DB.prepare("UPDATE clientes SET nombre = ?, pass_hash = ? WHERE id = ?").bind(nombre, hash, existe.id).run();
    else await env.DB.prepare("INSERT INTO clientes (correo, nombre, pass_hash) VALUES (?, ?, ?)").bind(correo, nombre, hash).run();
    const r = await nuevoCodigo(env, correo, "registro");
    return r.error ? resp({ error: r.error }, r.estado) : resp({ ok: true, motivo: "registro" });
  }
  if (accion === "entrar") {
    const c = await env.DB.prepare("SELECT id, pass_hash, verificado, estado FROM clientes WHERE correo = ?").bind(correo).first();
    if (!c || c.estado !== "activo" || !(await passOk(String(d.pass || ""), c.pass_hash))) return resp({ error: "El correo o la contraseña no son correctos." }, 401);
    const motivo = c.verificado ? "entrar" : "registro";
    const r = await nuevoCodigo(env, correo, motivo);
    return r.error ? resp({ error: r.error }, r.estado) : resp({ ok: true, motivo });
  }
  if (accion === "olvide") {
    if (correoOk(correo)) {
      const c = await env.DB.prepare("SELECT id FROM clientes WHERE correo = ? AND verificado = 1 AND estado = 'activo'").bind(correo).first();
      if (c) { const r = await nuevoCodigo(env, correo, "recuperar"); if (r.estado === 429) return resp({ error: r.error }, 429); }
    }
    return resp({ ok: true, motivo: "recuperar" });
  }
  if (accion === "reenviar") {
    const motivo = ["registro", "entrar", "recuperar"].includes(d.motivo) ? d.motivo : "";
    if (!motivo || !correoOk(correo)) return resp({ error: "Datos no válidos" }, 400);
    const u = await env.DB.prepare("SELECT (strftime('%s','now') - strftime('%s', creado_en)) AS seg FROM codigos WHERE correo = ? AND motivo = ? AND codigo_hash NOT LIKE 'permiso:%' ORDER BY id DESC LIMIT 1").bind(correo, motivo).first();
    if (!u) return resp({ error: "Vuelva a empezar." }, 400);
    if (u.seg < REENVIO_S) return resp({ error: `Espere ${REENVIO_S - u.seg} segundos para pedir otro código.` }, 429);
    const r = await nuevoCodigo(env, correo, motivo);
    return r.error ? resp({ error: r.error }, r.estado) : resp({ ok: true });
  }
  if (accion === "verificar") {
    const motivo = ["registro", "entrar", "recuperar"].includes(d.motivo) ? d.motivo : "";
    const codigo = txt(d.codigo, 5);
    if (!motivo || !/^\d{5}$/.test(codigo)) return resp({ error: "Escriba los 5 dígitos del código." }, 400);
    const p = await env.DB.prepare(
      `SELECT id, codigo_hash, intentos, (expira_en < datetime('now')) AS vencido FROM codigos
       WHERE correo = ? AND motivo = ? AND usado_en IS NULL AND codigo_hash NOT LIKE 'permiso:%' ORDER BY id DESC LIMIT 1`
    ).bind(correo, motivo).first();
    if (!p) return resp({ error: "Pida un código nuevo." }, 400);
    if (p.vencido) { await env.DB.prepare("UPDATE codigos SET usado_en = datetime('now') WHERE id = ?").bind(p.id).run(); return resp({ error: "El código venció. Pida uno nuevo." }, 400); }
    if (!igual(p.codigo_hash, await hashCodigo(correo, motivo, codigo))) {
      const quedan = p.intentos - 1;
      await env.DB.prepare(`UPDATE codigos SET intentos = ?${quedan <= 0 ? ", usado_en = datetime('now')" : ""} WHERE id = ?`).bind(Math.max(quedan, 0), p.id).run();
      return resp({ error: quedan > 0 ? `Código incorrecto. Le quedan ${quedan} intento${quedan === 1 ? "" : "s"}.` : "Demasiados intentos. Pida un código nuevo." }, 400);
    }
    await env.DB.prepare("UPDATE codigos SET usado_en = datetime('now') WHERE id = ?").bind(p.id).run();
    const c = await env.DB.prepare("SELECT id, nombre, correo FROM clientes WHERE correo = ?").bind(correo).first();
    if (!c) return resp({ error: "Vuelva a empezar." }, 400);
    if (motivo === "recuperar") {
      const permiso = b64url(crypto.getRandomValues(new Uint8Array(24)));
      await env.DB.prepare("INSERT INTO codigos (correo, motivo, codigo_hash, intentos, expira_en) VALUES (?, 'recuperar', ?, 1, datetime('now', '+15 minutes'))")
        .bind(correo, "permiso:" + await sha256(permiso)).run();
      return resp({ ok: true, permiso });
    }
    if (motivo === "registro") await env.DB.prepare("UPDATE clientes SET verificado = 1 WHERE id = ?").bind(c.id).run();
    const token = await abrirSesion(request, env, c);
    return respCookie({ ok: true, sesion: { nombre: c.nombre, correo: c.correo, pedidos: await pedidosDe(env, c) } }, cookieSesion(token, SESION_DIAS * 86400));
  }
  if (accion === "nueva") {
    if (!passValida(d.pass) || !correoOk(correo)) return resp({ error: "Revise la contraseña nueva." }, 400);
    const p = await env.DB.prepare(
      "SELECT id FROM codigos WHERE correo = ? AND motivo = 'recuperar' AND codigo_hash = ? AND usado_en IS NULL AND expira_en > datetime('now')"
    ).bind(correo, "permiso:" + await sha256(txt(d.permiso, 100))).first();
    if (!p) return resp({ error: "Vuelva a pedir el código." }, 400);
    await env.DB.prepare("UPDATE codigos SET usado_en = datetime('now') WHERE id = ?").bind(p.id).run();
    const c = await env.DB.prepare("SELECT id FROM clientes WHERE correo = ?").bind(correo).first();
    await env.DB.prepare("UPDATE clientes SET pass_hash = ? WHERE id = ?").bind(await hashPass(d.pass), c.id).run();
    await env.DB.prepare("DELETE FROM sesiones WHERE cliente_id = ?").bind(c.id).run();
    return resp({ ok: true });
  }
  return resp({ error: "No encontrado" }, 404);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    try {
      if (url.pathname === "/api/pedido" && request.method === "POST") return await crearPedido(request, env);
      if (url.pathname === "/api/stripe" && request.method === "POST") return await avisoStripe(request, env);
      if (url.pathname.startsWith("/api/cuenta/")) return await cuentaRuta(request, env, url.pathname.slice(12));
      return resp({ error: "No encontrado" }, 404);
    } catch (e) {
      return resp({ error: "Error del servidor" }, 500);
    }
  },
};
