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
  await env.DB.prepare(
    `INSERT INTO pedidos (folio, creado_en, estado, nombre, telefono, correo, direccion, codigo_postal, items, total, es_prueba, envio, notas, ip)
     VALUES (?, datetime('now'), 'pendiente_pago', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
  ).bind(folio, c.nombre, c.tel, c.correo, direccion, c.cp, JSON.stringify(lineas), total, esPrueba, envio, c.notas, ip).run();

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

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    try {
      if (url.pathname === "/api/pedido" && request.method === "POST") return await crearPedido(request, env);
      if (url.pathname === "/api/stripe" && request.method === "POST") return await avisoStripe(request, env);
      return resp({ error: "No encontrado" }, 404);
    } catch (e) {
      return resp({ error: "Error del servidor" }, 500);
    }
  },
};
