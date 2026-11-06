/* PASO 1 — Ejecutar en una pestaña de https://www.costco.com.mx/
   Lee todas las fragancias de Costco (solo perfumes con costo >= $800, los demás
   nunca alcanzan la ganancia mínima), las compara con datos/costco.json publicado
   y deja los cambios en window.name para el paso 2 (en Liverpool, misma pestaña).
   Devuelve un resumen corto. */
(async () => {
  const SITIO = "https://santgarcia5051.github.io/atelier/datos/costco.json";
  const COSTO_MIN = 800;
  const NO_PERFUME = /\b(set|estuche|kit|loci[oó]n corporal|desodorante|gel de ba[ñn]o|crema|mini|minis|travel|body|bruma|mist|paquete|coffret|d[uú]o|tr[ií]o|regalo|miniaturas?|vela|difusor|shower|jab[oó]n|aceite|cofre|pzas?|piezas)\b|\+/i;
  const todos = [];
  for (let pg = 0; pg < 20; pg++) {
    const r = await fetch(`/rest/v2/mexico/products/search?fields=FULL&query=:relevance:allCategories:cos_13.1&pageSize=100&currentPage=${pg}&lang=es_MX&curr=MXN`, { headers: { Accept: "application/json" } });
    const j = await r.json();
    for (const p of j.products || []) {
      if (NO_PERFUME.test(p.name)) continue;
      const costo = Math.max(p.basePrice ? p.basePrice.value : 0, p.price ? p.price.value : 0);
      if (costo < COSTO_MIN) continue;
      const cats = (p.addToCartFromPLPCategories || []).map(c => c.key);
      const img = ((p.images || []).find(i => i.format === "zoom") || (p.images || []).find(i => i.format === "product") || {}).url;
      const ml = (p.name.match(/(\d+(?:\.\d+)?)\s*ml/i) || [])[1];
      todos.push({
        codigo: p.code, nombre: p.name, ml: ml ? +ml : null, costo: Math.round(costo),
        existencia: p.stock && p.stock.stockLevelStatus === "inStock" ? 1 : 0,
        dama: cats.includes("cos_13.1.1") ? 1 : 0, caballero: cats.includes("cos_13.1.2") ? 1 : 0,
        foto: img ? "https://www.costco.com.mx" + img : null, url: "https://www.costco.com.mx" + p.url
      });
    }
    if (pg + 1 >= ((j.pagination || {}).totalPages || 0)) break;
  }
  if (todos.length < 50) return "ERROR: Costco devolvió muy pocos perfumes (" + todos.length + "). No se cambia nada.";
  let actual = { productos: [] };
  try { actual = await (await fetch(SITIO + "?t=" + Date.now(), { cache: "no-store" })).json(); } catch (e) {}
  const prev = new Map((actual.productos || []).map(p => [p.codigo, p]));
  const nuevos = [], cambios = [];
  for (const p of todos) {
    const a = prev.get(p.codigo);
    if (!a) { nuevos.push(p); continue; }
    const c = { codigo: p.codigo };
    for (const k of ["costo", "existencia", "foto", "ml"]) if (a[k] !== p[k]) c[k] = p[k];
    if (Object.keys(c).length > 1) cambios.push(c);
  }
  const hoy = todos.map(p => p.codigo);
  const quitados = [...prev.keys()].filter(c => !hoy.includes(c));
  window.name = "SCX2" + JSON.stringify({ fecha: new Date().toISOString(), presentes: hoy, nuevos, cambios, quitados });
  return `costco ${todos.length} perfumes (costo >= ${COSTO_MIN}) | nuevos ${nuevos.length} | cambios ${cambios.length} | quitados ${quitados.length} | agotados ${todos.filter(p => !p.existencia).length}`;
})();
