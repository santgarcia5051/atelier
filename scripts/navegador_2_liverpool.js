/* PASO 2 — En la MISMA pestaña del paso 1, navegar a https://www.liverpool.com.mx/tienda?s=perfume
   y ejecutar este script. Busca el precio de tienda departamental de cada perfume nuevo
   (y de los que se pidan en window.__REFRESCAR, una lista de códigos) y arma el paquete final.
   El paquete queda comprimido en window.__P; se lee por partes con window.__parte(i). */
(async () => {
  if (!window.name.startsWith("SCX2")) return "ERROR: no encontré el resultado del paso 1 en esta pestaña.";
  const D = JSON.parse(window.name.slice(4));
  const norm = s => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/&/g, " ").replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim();
  const GEN = new Set(["ml", "eau", "de", "para", "hombre", "mujer", "dama", "caballero", "unisex", "spray", "perfume", "fragancia", "y", "the", "for", "men", "women", "pour", "vaporizador", "vapo", "edicion", "limitada", "nuevo", "new", "refillable", "recargable", "refill", "oz"]);
  const conc = s => /eau de toilette|\bedt\b/.test(s) ? "edt" : /eau de parfum|\bedp\b/.test(s) ? "edp" : /\bextrait\b/.test(s) ? "ext" : /\bparfum\b|\bperfume\b/.test(s) ? "pp" : "";
  async function buscar(q) {
    const t = await (await fetch("/tienda?s=" + encodeURIComponent(q).replace(/%20/g, "+"))).text();
    const d = new DOMParser().parseFromString(t, "text/html");
    return [...d.querySelectorAll('[data-testid$="-card"]')].filter(c => /^\d+-card$/.test(c.getAttribute("data-testid"))).slice(0, 10).map(c => {
      const txt = [...c.querySelectorAll("p,span,h2,h3,h4,h5,h6,a")].filter(e => !e.children.length).map(e => e.textContent.trim()).filter(Boolean);
      const precios = (c.textContent.match(/\$\s?[\d,]+(?:\.\d+)?/g) || []).map(x => +x.replace(/[^\d.]/g, ""));
      return [txt.slice(0, 2).join(" ").slice(0, 90), precios];
    });
  }
  /* Coincidencia estricta: misma marca y línea, sin variantes (Intense, Elixir, 2, etc.) que no tenga el de Costco,
     sin sets ni otros artículos. El precio de referencia es el MÁS BAJO encontrado, para no exagerar el descuento. */
  function coincidir(nombre, res, genero) {
    const n = norm(nombre), cc = conc(n);
    const ct = n.replace(/\b\d+(\.\d+)?\s*ml\b/g, "").replace(/\b(edp|edt)\b/g, "").split(" ").filter(w => w && !GEN.has(w) && !/^\d+$/.test(w) || /^[2-9]$/.test(w) || w === "parfum");
    const ok = [];
    for (const [t, p] of res || []) {
      const lt = norm(t);
      if (!/eau de|perfume|parfum|colonia|extrait|elixir|cologne/.test(lt)) continue;
      if (/\bset\b|estuche|kit|monedero|bolsa|cartera|lentes|reloj|body|crema|corporal|desodorante|\bmini\b|cosmetiquera|mochila/.test(lt)) continue;
      const lc = conc(lt);
      if (cc && cc !== "pp" && lc && lc !== "pp" && lc !== cc) continue;
      /* Mismo público: no comparar uno de dama con uno "para hombre" ni al revés */
      if (genero === "dama" && /para hombre/.test(lt) || genero === "caballero" && /para mujer/.test(lt)) continue;
      /* Quitar solo la primera etiqueta de tipo (Eau de parfum, Perfume, etc.); un "Parfum" que quede es parte del nombre (p. ej. Bright Crystal Parfum) */
      const lt2 = lt.replace(/\b(eau de parfum|eau de toilette|eau de cologne|perfume|parfum|colonia|extrait de parfum)\b/, " ");
      const lts = new Set(lt2.split(" ").filter(w => w && !GEN.has(w) || w === "parfum"));
      if (!ct.every(w => lts.has(w))) continue;
      const extra = [...lts].filter(w => !ct.includes(w) && !["eau", "toilette", "de", "colonia", "cologne"].includes(w) && !(/^\d+$/.test(w) && +w >= 30));
      if (extra.length || !p || !p.length) continue;
      ok.push([t, Math.min(...p)]);
    }
    return ok.length ? { antes: Math.min(...ok.map(o => o[1])), liverpool: ok[0][0] } : null;
  }
  const refrescar = new Set(window.__REFRESCAR || []);
  const nombres = Object.fromEntries(D.nuevos.map(p => [p.codigo, p.nombre]));
  const generos = Object.fromEntries(D.nuevos.map(p => [p.codigo, p.dama && !p.caballero ? "dama" : p.caballero && !p.dama ? "caballero" : ""]));
  Object.assign(generos, window.__GENEROS || {});
  Object.assign(nombres, window.__NOMBRES || {});
  const refs = {};
  let i = 0;
  const lista = [...new Set([...D.nuevos.map(p => p.codigo), ...refrescar])];
  const trabajador = async () => {
    while (i < lista.length) {
      const c = lista[i++], nombre = nombres[c]; if (!nombre) continue;
      const q = nombre.replace(/\b\d+(\.\d+)?\s*ml\b/ig, "").replace(/\b(edp|edt)\b/ig, "").replace(/,/g, " ").trim();
      try { refs[c] = coincidir(nombre, await buscar(q), generos[c]); } catch (e) { refs[c] = { error: 1 }; }
    }
  };
  await Promise.all([trabajador(), trabajador(), trabajador(), trabajador()]);
  D.refs = refs;
  const bytes = new TextEncoder().encode(JSON.stringify(D));
  const gz = new Uint8Array(await new Response(new Blob([bytes]).stream().pipeThrough(new CompressionStream("gzip"))).arrayBuffer());
  let b = ""; for (let k = 0; k < gz.length; k++) b += String.fromCharCode(gz[k]);
  window.__P = btoa(b).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  window.__parte = k => window.__P.slice(k * 1400, (k + 1) * 1400);
  return `paquete listo: ${Math.ceil(window.__P.length / 1400)} partes | refs encontradas ${Object.values(refs).filter(r => r && r.antes).length}/${lista.length}`;
})();
