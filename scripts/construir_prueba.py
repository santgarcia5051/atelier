#!/usr/bin/env python3
"""Construye prueba.html: la página completa con el diseño "Crema Profundo"
(claro y fácil, letra elegante, fotos sobre tonos profundos del color de cada perfume; modo oscuro negro y dorado)
y animaciones en toda la página. Parte de index.html, así que conserva catálogo, ficha, similares y carrito.

Uso: python3 scripts/construir_prueba.py
"""
import os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(RAIZ, "index.html"), encoding="utf-8").read()


def rep(old, new, s, n=1):
    assert s.count(old) >= 1, "no encontré: " + old[:80]
    return s.replace(old, new, n)


s = src

# ---------- Tipografía
s = rep('family=Jost:wght@300;400;500&family=Albert+Sans:wght@400;500;600&display=swap',
        'family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Jost:wght@300;400;500;600&display=swap', s)

TEMA = r"""
<style id="tema-crema">
/* Crema Profundo: base clara y fácil (crema, tinta café), letra Cormorant + Jost, acento dorado.
   Modo oscuro: negro y dorado. Fotos sobre el tono profundo del color de cada perfume. */
:root {
  --bg: #F1EADF; --surface: #FBF8F3; --tile: #EFE7DA; --fg: #211B16; --muted: #7A6B5C; --line: #DCCFBC;
  --accent: #9A7B45; --accent-fg: #FBF8F3; --gold: #C8A96A; --deep: #16120E; --ink: #211B16;
  --overlay: rgba(33, 27, 22, .5); --shadow: 0 26px 50px -18px rgba(80, 55, 25, .28); --glow: rgba(255, 255, 255, .5);
  --font-display: "Cormorant Garamond", "Cormorant", Georgia, "Times New Roman", serif;
  --font-body: "Jost", "Futura", "Helvetica Neue", Arial, sans-serif;
  --r-md: 22px; --r-lg: 28px;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #0B0A09; --surface: #13110D; --tile: #15120E; --fg: #EDE5D7; --muted: #A3957D; --line: #2A241C;
    --accent: #C8A96A; --accent-fg: #0B0A09; --deep: #0B0A09; --ink: #13110D;
    --overlay: rgba(0, 0, 0, .65); --shadow: 0 30px 60px -20px rgba(0, 0, 0, .8); --glow: rgba(200, 169, 106, .14);
  }
}
:root[data-theme="dark"] {
  --bg: #0B0A09; --surface: #13110D; --tile: #15120E; --fg: #EDE5D7; --muted: #A3957D; --line: #2A241C;
  --accent: #C8A96A; --accent-fg: #0B0A09; --deep: #0B0A09; --ink: #13110D;
  --overlay: rgba(0, 0, 0, .65); --shadow: 0 30px 60px -20px rgba(0, 0, 0, .8); --glow: rgba(200, 169, 106, .14);
}
body { font-weight: 300; }
.wrap { max-width: 1320px; }
h1, h2, h3, .card-name, .d-name, #dName { font-family: var(--font-display); }
.eyebrow { font-family: var(--font-body); letter-spacing: .32em; color: var(--accent); }

/* Barra de avisos en movimiento */
.avisos { background: var(--ink); color: #E9DCC4; font-size: 11.5px; letter-spacing: .24em; text-transform: uppercase; overflow: hidden; white-space: nowrap; padding-block: 9px; }
.avisos > div { display: inline-flex; gap: 48px; padding-right: 48px; animation: marq 40s linear infinite; }
.avisos i { color: var(--gold); font-style: normal; }

/* Encabezado */
.top { backdrop-filter: blur(14px); }
.brand-mark { display: none; }
.brand-name { font-family: var(--font-display); font-size: 30px; font-weight: 500; letter-spacing: .34em; text-transform: uppercase; }
.links a { font-size: 14px; position: relative; text-decoration: none; }
.links a::after { content: ""; position: absolute; left: 0; right: 0; bottom: -4px; height: 1px; background: var(--accent); transform: scaleX(0); transform-origin: left; transition: transform .35s ease; }
.links a:hover::after { transform: scaleX(1); }
.cart-btn { background: var(--ink) !important; color: #F1EADF !important; border-color: var(--ink) !important; }
.cart-count { background: var(--gold) !important; color: var(--ink) !important; }
.cart-count.bump { animation: pulse .8s; }

/* Portada */
.hero2 { display: grid; grid-template-columns: 1fr 1.05fr; gap: 40px; align-items: center; padding-block: 56px 30px; }
.hero2 h1 { font-size: clamp(54px, 8.4vw, 118px); font-weight: 400; line-height: .9; margin-top: 20px; }
.hero2 h1 em { font-style: italic; color: var(--accent); }
.hero2 .lead { margin: 24px 0 0; max-width: 44ch; font-size: 18px; line-height: 1.6; color: var(--muted); }
.hero2 .ctas { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 32px; }
.hero2 .stats { display: flex; flex-wrap: wrap; gap: 36px; margin-top: 38px; }
.hero2 .stats b { display: block; font-family: var(--font-display); font-size: 44px; font-weight: 500; line-height: 1; }
.hero2 .stats span { font-size: 12px; letter-spacing: .16em; text-transform: uppercase; color: var(--muted); }
.mosaico { display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 14px; height: clamp(380px, 46vw, 570px); }
.mos { position: relative; overflow: hidden; border-radius: 28px; border: 0; padding: 0; cursor: pointer; display: flex; align-items: flex-end; justify-content: center; color: #F1EADF; text-align: left; transition: transform .5s cubic-bezier(.2,.7,.2,1), box-shadow .5s; }
.mos:hover, .mos:focus-visible { transform: translateY(-6px); box-shadow: var(--shadow); }
.mos img { height: 76%; margin-bottom: 6%; filter: drop-shadow(0 24px 26px rgba(0,0,0,.55)); transition: transform .7s cubic-bezier(.2,.7,.2,1); }
.mos:hover img { transform: translateY(-10px) rotate(-3deg) scale(1.04); }
.mos .cap { position: absolute; left: 22px; top: 18px; font-family: var(--font-display); font-size: 28px; line-height: 1.1; }
.mos .cap small { display: block; font-family: var(--font-body); font-size: 11px; letter-spacing: .2em; text-transform: uppercase; color: var(--gold); margin-top: 4px; }
.mos.m1 { grid-row: span 2; background: radial-gradient(circle at 50% 66%, #4A3618, #16120E 80%); }
.mos.m1 img { height: 70%; }
.mos.m2 { background: radial-gradient(circle at 50% 72%, #7A2430, #2A1215 85%); }
.mos.m3 { background: radial-gradient(circle at 50% 72%, #22405E, #111A24 85%); }
@media (max-width: 860px) { .hero2 { grid-template-columns: 1fr; } }

/* Test de aroma */
.estilo { display: grid; grid-template-columns: auto 1fr; gap: 28px; align-items: center; background: var(--surface); border: 1px solid var(--line); border-radius: 28px; padding: 24px 30px; margin: 40px 0 10px; }
.estilo h3 { font-size: clamp(28px, 3.4vw, 38px); font-weight: 400; line-height: 1; }
.estilo h3 em { color: var(--accent); }
.estilo p { margin: 6px 0 0; font-size: 14px; color: var(--muted); }
.estilo .opts { display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-end; }
.estilo button { border: 1.5px solid var(--line); background: var(--bg); border-radius: 999px; padding: 11px 19px; font-size: 14px; cursor: pointer; transition: all .3s; }
.estilo button:hover { border-color: var(--accent); transform: translateY(-2px); }
.estilo button[aria-pressed="true"] { background: var(--fg); color: var(--bg); border-color: var(--fg); }
@media (max-width: 860px) { .estilo { grid-template-columns: 1fr; } .estilo .opts { justify-content: flex-start; } }

/* Secciones */
section.block { border-top: 0; }
.block-head h2 { font-size: clamp(40px, 5.4vw, 66px); font-weight: 400; line-height: 1; }
.tabs { background: transparent; border: 0; padding: 0; gap: 8px; }
.tab { background: var(--surface); border: 1px solid var(--line); font-family: var(--font-body); font-size: 13px; letter-spacing: .14em; }
.tab[aria-selected="true"] { background: var(--fg); color: var(--bg); border-color: var(--fg); }
.select-wrap select { border-radius: 999px; }

/* Tarjetas */
.grid { gap: 18px !important; grid-template-columns: repeat(auto-fill, minmax(min(100%, 250px), 1fr)) !important; }
.card { background: var(--surface); border-radius: 26px !important; overflow: hidden; gap: 0 !important; padding: 0 !important; transition: transform .5s cubic-bezier(.2,.7,.2,1), box-shadow .5s; position: relative; }
.card:hover, .card:focus-visible { transform: translateY(-8px); box-shadow: var(--shadow); }
.card-media { margin: 10px; border-radius: 20px !important; aspect-ratio: 1 / 1.02 !important; }
.card-media.profundo { background: radial-gradient(circle at 50% 58%, var(--tint, #3A2E20), var(--deep) 85%) !important; }
.card-media.profundo img { filter: drop-shadow(0 20px 24px rgba(0,0,0,.7)) !important; mix-blend-mode: normal !important; }
.card-media.profundo .card-tag { background: rgba(0,0,0,.35); color: #EDE5D7; border-color: rgba(255,255,255,.2); }
.card-media img { transition: transform .7s cubic-bezier(.2,.7,.2,1) !important; }
.card:hover .card-media img, .card:focus-visible .card-media img { transform: scale(1.08) rotate(-3deg) !important; }
.card-body { padding: 8px 20px 20px !important; gap: 2px; }
.card-family { font-size: 11px !important; letter-spacing: .2em !important; text-transform: uppercase; color: var(--muted); font-weight: 500; }
.card-name { font-size: 28px !important; line-height: 1.04; font-weight: 500 !important; }
.card-lema { font-family: var(--font-display); font-size: 17px !important; }
.card-price { display: flex !important; align-items: center; gap: 6px; padding-right: 54px; min-height: 44px; }
.card-price .ahorro { display: none; }
.foto-tienda-wrap { background: #EFE7DA !important; }
.foto-tienda-wrap img { mix-blend-mode: multiply !important; }
.card.destacada .card-price { color: #F1EADF; }
.desc-badge { position: absolute; z-index: 2; top: 12px; right: 12px; background: var(--gold); color: #211B16; border-radius: 999px; padding: 5px 10px; font-size: 12px; font-weight: 600; }
.notas-hover { position: absolute; z-index: 2; left: 10px; right: 10px; bottom: 10px; background: rgba(251,248,243,.9); color: #211B16; backdrop-filter: blur(8px); border-radius: 14px; padding: 10px 13px; font-size: 13px; line-height: 1.4; transform: translateY(140%); transition: transform .5s cubic-bezier(.2,.7,.2,1); text-align: left; }
.notas-hover small { display: block; font-size: 10px; letter-spacing: .24em; text-transform: uppercase; color: #9A7B45; font-weight: 600; margin-bottom: 2px; }
.card:hover .notas-hover, .card:focus-visible .notas-hover { transform: none; }
.q-add { position: absolute; z-index: 3; right: 18px; bottom: 18px; height: 44px; min-width: 44px; border-radius: 999px; background: var(--fg); color: var(--bg); display: inline-flex; align-items: center; justify-content: center; padding: 0 14px; font-size: 12px; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; transition: all .4s; }
.q-add i { font-style: normal; font-size: 20px; line-height: 1; }
.q-add b { max-width: 0; overflow: hidden; white-space: nowrap; transition: max-width .4s, margin .4s; font-weight: 600; }
.card:hover .q-add b, .q-add:focus-visible b { max-width: 90px; margin-left: 8px; }
.q-add.ok { background: var(--accent); }
.card.agotado .q-add { display: none; }
@media (min-width: 1000px) {
  .card.destacada { grid-column: span 2; grid-row: span 2; background: var(--ink); color: #F1EADF; }
  .card.destacada .card-media { aspect-ratio: auto !important; flex: 1; min-height: 420px; }
  .card.destacada .card-name { font-size: 46px !important; }
  .card.destacada .card-family, .card.destacada .card-price s { color: #B5A792; }
  .card.destacada .card-lema { color: #D9B977 !important; font-size: 22px !important; }
  .card.destacada .q-add { background: var(--gold); color: #211B16; }
  .card.destacada { display: flex !important; flex-direction: column; }
}

/* Ficha y carrito */
.drawer:not([hidden]) { animation: drawerIn .55s cubic-bezier(.2,.7,.2,1); }
.overlay:not([hidden]) { animation: fade .4s ease; }
.btn { border-radius: 999px; transition: transform .3s, box-shadow .3s, opacity .3s !important; }
.btn:hover { transform: translateY(-2px); box-shadow: 0 12px 24px -12px rgba(0,0,0,.4); opacity: 1 !important; }

/* Animaciones */
@keyframes marq { to { transform: translateX(-50%); } }
@keyframes rise { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: none; } }
@keyframes fade { from { opacity: 0; } to { opacity: 1; } }
@keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-14px); } }
@keyframes pulse { 0%,100% { box-shadow: 0 0 0 0 rgba(200,169,106,.55); } 50% { box-shadow: 0 0 0 10px rgba(200,169,106,0); } }
@keyframes drawerIn { from { transform: translateX(40px); opacity: 0; } to { transform: none; opacity: 1; } }
@keyframes shine { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
.rv { animation: rise .9s cubic-bezier(.2,.7,.2,1) both; }
.rv.d2 { animation-delay: .1s; } .rv.d3 { animation-delay: .2s; } .rv.d4 { animation-delay: .3s; } .rv.d5 { animation-delay: .4s; }
.flota { animation: float 6s ease-in-out infinite; }
.mos.m2 img { animation-delay: -2s; } .mos.m3 img { animation-delay: -4s; }
.shine { background: linear-gradient(100deg, var(--accent) 20%, #E8CF95 40%, var(--accent) 60%); background-size: 200% 100%; -webkit-background-clip: text; background-clip: text; color: transparent; animation: shine 6s linear infinite; }
/* Aparecer al hacer scroll (solo si el script corre; sin script todo se ve) */
.js-anim .sr { opacity: 0; transform: translateY(28px); transition: opacity .8s cubic-bezier(.2,.7,.2,1), transform .8s cubic-bezier(.2,.7,.2,1); }
.js-anim .sr.in { opacity: 1; transform: none; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
  .js-anim .sr { opacity: 1; transform: none; }
}
</style>
"""
s = rep("</head>", TEMA + "</head>", s)

# ---------- Barra de avisos
AVISO = "".join('<span>Envío gratis en 2 o más perfumes</span><i>✦</i><span>100% originales</span><i>✦</i><span>Hasta 25% bajo tienda departamental</span><i>✦</i>' for _ in range(4))
s = rep('<header class="top">', f'<div class="avisos" aria-hidden="true"><div>{AVISO}</div></div>\n<header class="top">', s)

# ---------- Portada
i = s.index('  <div class="wrap hero">')
j = s.index('  <section class="block" id="perfumes"')
HERO = """  <div class="wrap">
    <div class="hero2">
      <div>
        <div class="eyebrow rv">Perfumería · México</div>
        <h1 class="rv d2">Huele a<br><em class="shine">quien eres.</em></h1>
        <p class="lead rv d3">Fragancias originales de las grandes casas y de nicho, por debajo del precio de tienda departamental. <span id="heroShip">Envío gratis a todo México en la compra de 2 perfumes o más.</span></p>
        <div class="ctas rv d4"><a class="btn" href="#perfumes">Ver catálogo</a><a class="btn ghost" href="#estilo">Encontrar mi aroma</a></div>
        <div class="stats rv d5"><div><b id="stTotal">330</b><span>Fragancias</span></div><div><b id="stCasas">90</b><span>Casas</span></div><div><b id="stMax">−25%</b><span>Hasta</span></div></div>
      </div>
      <div class="mosaico rv d3">
        <button class="mos m1" type="button" data-ir="Unisex"><span class="cap">Unisex y nicho<small id="mosU">Fragancias</small></span><img class="flota" src="fotos/perseus.webp" alt=""></button>
        <button class="mos m2" type="button" data-ir="Mujer"><span class="cap">Para ella<small id="mosM">Fragancias</small></span><img class="flota" src="fotos/very-good-girl.webp" alt=""></button>
        <button class="mos m3" type="button" data-ir="Hombre"><span class="cap">Para él<small id="mosH">Fragancias</small></span><img class="flota" src="fotos/acqua-di-gio-profondo-parfum.webp" alt=""></button>
      </div>
    </div>
    <div class="estilo sr" id="estilo">
      <div><h3>¿Qué le gusta <em>oler</em>?</h3><p>Elija un estilo y le mostramos los perfumes que van con usted.</p></div>
      <div class="opts" id="estiloOpts">
        <button type="button" data-estilo="" aria-pressed="true">Todos</button>
        <button type="button" data-estilo="floral" aria-pressed="false">Floral</button>
        <button type="button" data-estilo="amaderado" aria-pressed="false">Amaderado</button>
        <button type="button" data-estilo="fresco" aria-pressed="false">Fresco</button>
        <button type="button" data-estilo="dulce" aria-pressed="false">Dulce</button>
        <button type="button" data-estilo="especiado" aria-pressed="false">Especiado</button>
        <button type="button" data-estilo="oriental" aria-pressed="false">Oriental</button>
      </div>
    </div>
  </div>

"""
s = s[:i] + HERO + s[j:]

# ---------- Tarjetas: tono del perfume, descuento, notas al pasar el cursor, botón rápido de agregar
old_card = '''    <button class="card${disponible(p) ? "" : " agotado"}" type="button" data-id="${p.id}" aria-label="Ver ficha de ${p.nombre}${disponible(p) ? "" : " (no disponible)"}">
      <div class="card-media${esFotoTienda(p) ? " foto-tienda-wrap" : ""}${p.recorte ? " recorte-wrap" : ""}">${disponible(p) ? `<span class="card-tag">${p.conc}</span>` : `<span class="card-tag agotado-tag">No disponible</span>`}${media(p)}</div>'''
new_card = '''    <button class="card sr${disponible(p) ? "" : " agotado"}${p.id === destacadaId ? " destacada" : ""}" type="button" data-id="${p.id}" aria-label="Ver ficha de ${p.nombre}${disponible(p) ? "" : " (no disponible)"}" style="--tint:${tono(p.liquido)}">
      <div class="card-media${fondoProfundo(p) ? " profundo" : (esFotoTienda(p) ? " foto-tienda-wrap" : "")}">${disponible(p) ? `<span class="card-tag">${p.conc}</span>` : `<span class="card-tag agotado-tag">No disponible</span>`}${descBadge(p)}${media(p)}<span class="notas-hover"><small>Notas</small>${[p.salida[0], p.corazon[0], p.fondo[0]].filter(Boolean).join(" · ")}</span></div>'''
s = rep(old_card, new_card, s)
s = rep('''        <span class="card-price">${priceLine(p)}</span>
      </div>
    </button>`).join("")''', '''        <span class="card-price">${priceLine(p)}</span>
      </div>
      <span class="q-add" role="button" tabindex="0" data-add="${p.id}" aria-label="Agregar ${p.nombre} al carrito"><i>+</i><b>Agregar</b></span>
    </button>`).join("")''', s)
s = rep('$("grid").innerHTML = list.length ? list.map(p => `', '$("grid").innerHTML = list.length ? list.map((p, k) => `', s)
s = rep('const list = sorted(PERFUMES).filter(p => p.seccion === state.seccion);', 'const list = sorted(PERFUMES).filter(p => p.seccion === state.seccion && cumpleEstilo(p));\n  const destacadaId = (list.find(p => disponible(p) && p.antes && p.pres.length === 1 && fondoProfundo(p)) || list.find(p => disponible(p) && p.antes && p.pres.length === 1) || {}).id;', s)

# Agregar rápido sin abrir la ficha
s = rep('$("grid").addEventListener("click", e => { const c = e.target.closest(".card"); if (c) openDrawer(c.dataset.id, c); });',
        '''$("grid").addEventListener("click", e => {
  const a = e.target.closest(".q-add");
  if (a) { e.stopPropagation(); const p = PERFUMES.find(x => x.id === a.dataset.add); if (p && disponible(p)) { addToCart(p.id, p.pres[0].ml); gustoSumar(p.id, 3); a.classList.add("ok"); setTimeout(() => a.classList.remove("ok"), 1200); } return; }
  const c = e.target.closest(".card"); if (c) openDrawer(c.dataset.id, c); });
$("grid").addEventListener("keydown", e => { const a = e.target.closest(".q-add"); if (a && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); e.stopPropagation(); a.click(); } });''', s)

# Funciones de apoyo + animaciones + test de aroma + mosaicos
APOYO = r"""
/* ===== Diseño Crema Profundo ===== */
function tono(hex) {  // color del perfume oscurecido (sin pasteles)
  const h = (hex || "#9A7B45").replace("#", ""); const c = [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16) || 120);
  const b = [26, 22, 18]; return "#" + c.map((x, i) => Math.round(x * .45 + b[i] * .55).toString(16).padStart(2, "0")).join("");
}
function fondoProfundo(p) { return !!p.img && (p.recorte || !/^https?:/.test(p.img)); }
function descBadge(p) {
  if (!disponible(p) || !p.antes || p.pres.length !== 1 || p.antes <= p.pres[0].precio) return "";
  return `<span class="desc-badge">−${Math.round((1 - p.pres[0].precio / p.antes) * 100)}%</span>`;
}
const ESTILOS = {
  floral: /floral|rosa|jazm|azahar|tuberosa|peon|iris|lirio|gardenia|violeta|flor/,
  amaderado: /amader|madera|vetiver|cedro|s[aá]ndalo|pachul|oud|musgo/,
  fresco: /fresc|c[ií]tric|acu[aá]tic|marin|bergamota|lim[oó]n|toronja|menta|verde/,
  dulce: /dulce|gourmand|vainilla|caramelo|praline|tonka|miel|chocolate|caf[eé]|frut/,
  especiado: /especi|pimienta|canela|cardamomo|azafr[aá]n|jengibre|clavo|tabaco|cuero/,
  oriental: /oriental|[aá]mbar|ambar|incienso|resina|almizcle|oud|benju/
};
state.estilo = "";
function cumpleEstilo(p) {
  if (!state.estilo) return true;
  const t = [p.familia, ...(p.acordes || []).map(a => a[0]), ...p.salida, ...p.corazon, ...p.fondo].join(" ").toLowerCase();
  return ESTILOS[state.estilo].test(t);
}
document.getElementById("estiloOpts").addEventListener("click", e => {
  const b = e.target.closest("button"); if (!b) return;
  state.estilo = b.dataset.estilo;
  document.querySelectorAll("#estiloOpts button").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
  renderGrid(); document.getElementById("perfumes").scrollIntoView({ behavior: "smooth" });
});
document.querySelectorAll(".mos").forEach(m => m.addEventListener("click", () => {
  const sec = m.dataset.ir; if (!SECCIONES.includes(sec) || !PERFUMES.some(p => p.seccion === sec)) return;
  state.seccion = sec; try { localStorage.setItem("ag-sec", sec); } catch (e) {}
  renderChips(); renderGrid(); document.getElementById("perfumes").scrollIntoView({ behavior: "smooth" });
}));
(function cifras() {
  const n = s => PERFUMES.filter(p => p.seccion === s).length;
  const set = (id, v) => { const el = document.getElementById(id); if (el) el.textContent = v; };
  set("stTotal", PERFUMES.length); set("stCasas", new Set(PERFUMES.map(p => p.marca)).size);
  const max = Math.max(0, ...PERFUMES.filter(p => p.antes && p.pres.length === 1).map(p => Math.round((1 - p.pres[0].precio / p.antes) * 100)));
  set("stMax", max ? `−${max}%` : "Original");
  set("mosM", `${n("Mujer")} fragancias`); set("mosH", `${n("Hombre")} fragancias`); set("mosU", `${n("Unisex")} fragancias`);
})();
/* Aparecer al hacer scroll */
document.documentElement.classList.add("js-anim");
const srIO = "IntersectionObserver" in window ? new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); srIO.unobserve(e.target); } }), { rootMargin: "0px 0px -6% 0px" }) : null;
function observarSR(root) {
  (root || document).querySelectorAll(".sr:not(.in)").forEach((el, k) => {
    if (!srIO) { el.classList.add("in"); return; }
    el.style.transitionDelay = (k % 4) * 70 + "ms"; srIO.observe(el);
  });
}
document.querySelectorAll(".block-head, #priceBody, .ship, #contacto .wrap > *, footer").forEach(el => el.classList.add("sr"));
new MutationObserver(() => observarSR(document.getElementById("grid"))).observe(document.getElementById("grid"), { childList: true });
setTimeout(() => observarSR(), 50);
"""
s = rep("function toast(msg) {", APOYO + "\nfunction toast(msg) {", s)

# Ocultar el antiguo botón de tema dentro del nombre (se conserva el botón)
open(os.path.join(RAIZ, "prueba.html"), "w", encoding="utf-8").write(s)
print("prueba.html lista")
