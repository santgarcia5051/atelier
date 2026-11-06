"""Genera atelier/nuevo.html (estilo oscuro y dorado) a partir de atelier/index.html.
El catálogo (perfumes.js) y las fotos se comparten entre las dos versiones."""
import re

import os
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(RAIZ, 'index.html')
DST = os.path.join(RAIZ, 'nuevo.html')
s = open(SRC, encoding='utf-8').read()

def R(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (old[:70], n)
    s = s.replace(old, new)

# ---------- Tokens: oscuro por defecto, claro crema con el botón ----------
a = s.index(':root {\n  --bg:')
b = s.index('* { box-sizing: border-box; }')
tokens = '''/* Layout: encabezado oscuro, fragancia destacada a pantalla, ingredientes en tres tarjetas, catálogo, precios, envíos y contacto. Oscuro con dorado por defecto; el botón cambia a crema. */
:root {
  --bg: #EFE8DD;
  --surface: #F8F3EA;
  --tile: #E3D8C7;
  --fg: #1B1815;
  --muted: #6C6357;
  --line: #D8CCBA;
  --accent: #8E6F34;
  --gold: #8E6F34;
  --gold-soft: #B08E4F;
  --accent-fg: #F8F3EA;
  --overlay: rgba(20, 17, 14, .5);
  --glass: rgba(255, 255, 255, .5);
  --glass-stroke: #8C8376;
  --cap: #2A2622;
  --shadow: 0 24px 60px -24px rgba(27, 24, 21, .45);
  --danger: #A6463A;
  --glow: rgba(255, 246, 228, .7);
  --ok: #4C6A43;
  --stage: #17110C;
  --stage-fg: #F3EBDD;

  --font-display: "Jost", "Futura", "Century Gothic", "Helvetica Neue", Arial, sans-serif;
  --font-body: "Albert Sans", "Helvetica Neue", Arial, sans-serif;

  --r-sm: 10px;
  --r-md: 18px;
  --r-lg: 28px;
  --r-pill: 999px;
}
:root[data-theme="dark"] {
  --bg: #0E0D0C; --surface: #171513; --tile: #1E1B18; --fg: #F2EBDF; --muted: #A39A8C;
  --line: #2C2824; --accent: #CDA85C; --gold: #CDA85C; --gold-soft: #E2C88F; --accent-fg: #0E0D0C;
  --overlay: rgba(0, 0, 0, .65); --glass: rgba(255, 255, 255, .07); --glass-stroke: #8E877C; --cap: #BDB4A6;
  --shadow: 0 24px 60px -24px rgba(0, 0, 0, .8); --danger: #E2907F; --glow: rgba(205, 168, 92, .16); --ok: #A3C495;
  --stage: #120D09; --stage-fg: #F3EBDD;
  color-scheme: dark;
}

'''
s = s[:a] + tokens + s[b:]

# Tema oscuro antes de pintar (sin parpadeo)
R('<style>\n:root { padding-top', '''<script>try{var t=localStorage.getItem("ag2-theme");document.documentElement.setAttribute("data-theme",t==="light"?"light":"dark")}catch(e){document.documentElement.setAttribute("data-theme","dark")}</script>
<style>
:root { padding-top''')
R('<title>Scantalia Perfumería</title>', '<title>Scantalia Perfumería</title>\n<meta name="theme-color" content="#0E0D0C">')

# ---------- Estilos nuevos ----------
R('/* Envíos */', '''/* ===== Estilo oscuro y dorado ===== */
.eyebrow { color: var(--gold); }
h2 { font-weight: 500 !important; letter-spacing: -.01em; }
.brand-name { font-weight: 500; }
.brand-sub { display: block; font-family: var(--font-display); font-size: 9.5px; letter-spacing: .32em; text-transform: uppercase; color: var(--gold); margin-top: 2px; }
.brand-mark { border-color: var(--gold); color: var(--gold); }
.btn.gold { background: transparent; color: var(--gold); border-color: var(--gold); text-transform: uppercase; letter-spacing: .14em; font-size: 13px; font-weight: 500; }
.btn.gold:hover { background: var(--gold); color: var(--accent-fg); opacity: 1; }
.btn.solid { text-transform: uppercase; letter-spacing: .14em; font-size: 13px; font-weight: 500; }

.spot { padding-block: 28px 56px; }
.spot-grid { display: grid; grid-template-columns: 1.05fr 1fr; gap: 48px; align-items: center; }
.spot-media {
  position: relative; aspect-ratio: 4 / 5; max-width: 100%; border-radius: var(--r-md); overflow: hidden;
  background:
    radial-gradient(ellipse 55% 42% at 50% 40%, rgba(232, 168, 90, .30), transparent 70%),
    radial-gradient(ellipse 90% 35% at 50% 100%, color-mix(in srgb, var(--tint, #E8A85A) 26%, transparent), transparent 70%),
    radial-gradient(circle at 18% 22%, rgba(255, 214, 150, .16) 0 6px, transparent 7px),
    radial-gradient(circle at 82% 16%, rgba(255, 214, 150, .12) 0 10px, transparent 11px),
    radial-gradient(circle at 72% 34%, rgba(255, 214, 150, .10) 0 4px, transparent 5px),
    radial-gradient(circle at 12% 48%, rgba(255, 214, 150, .08) 0 12px, transparent 13px),
    linear-gradient(180deg, #1A120B 0%, var(--stage) 60%, #080604 100%);
  box-shadow: var(--shadow);
}
.spot-media::after { content: ""; position: absolute; left: 8%; right: 8%; bottom: 9%; height: 7%; border-radius: 50%; background: radial-gradient(ellipse at center, rgba(0,0,0,.55), transparent 70%); }
.spot-media img { position: absolute; z-index: 1; left: 50%; bottom: 11%; height: 74%; width: auto; max-width: 80%; object-fit: contain; transform: translateX(-50%); filter: drop-shadow(0 18px 30px rgba(0,0,0,.55)); transition: opacity .45s ease, transform .6s cubic-bezier(.2,.8,.2,1); }
.spot-media > svg.spot-img { position: absolute; z-index: 1; left: 50%; bottom: 11%; height: 70%; width: auto; transform: translateX(-50%); }
.spot-media.swap img { opacity: 0; transform: translateX(-50%) translateY(10px); }
.spot-tag { position: absolute; z-index: 2; left: 16px; bottom: 16px; padding: 6px 12px; border-radius: var(--r-pill); background: rgba(14, 13, 12, .72); color: var(--stage-fg); font-size: 11px; letter-spacing: .12em; text-transform: uppercase; border: 1px solid rgba(205, 168, 92, .45); }
.spot-nav { position: absolute; z-index: 2; right: 14px; bottom: 14px; display: flex; gap: 6px; }
.spot-nav button { width: 36px; height: 36px; border-radius: 50%; border: 1px solid rgba(205, 168, 92, .5); background: rgba(14, 13, 12, .6); color: var(--stage-fg); cursor: pointer; display: grid; place-items: center; }
.spot-nav button svg { width: 16px; height: 16px; }
.spot-copy { display: grid; gap: 18px; min-width: 0; }
.spot-copy h1 { font-size: clamp(34px, 5vw, 58px); font-weight: 500; line-height: 1.06; color: var(--gold-soft); letter-spacing: -.01em; }
.spot-copy p { margin: 0; color: var(--muted); max-width: 54ch; }
.spot-copy p.lead { color: var(--fg); font-size: 17px; }
.spot-meta { font-size: 13px; color: var(--muted); display: flex; flex-wrap: wrap; gap: 6px 14px; font-variant-numeric: tabular-nums; }
.spot-meta b { color: var(--fg); font-weight: 500; }
.spot-actions { display: grid; gap: 10px; justify-items: start; }
.spot-actions small { font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }
.dots { display: flex; gap: 6px; }
@media (max-width: 860px) { .spot-grid { grid-template-columns: 1fr; gap: 26px; } .spot { padding-block: 16px 40px; } .spot-actions .btn { width: 100%; } .spot-actions { justify-items: stretch; } }

.notes-sec { padding-block: 56px; border-top: 1px solid var(--line); }
.notes-head { display: grid; gap: 10px; margin-bottom: 28px; }
.notes-head h2 { font-size: clamp(26px, 3.6vw, 40px); }
.notes-head p { margin: 0; color: var(--muted); max-width: 62ch; }
.notes-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.ntile { display: grid; gap: 10px; min-width: 0; }
.nvis {
  position: relative; aspect-ratio: 4 / 5; border-radius: var(--r-md); overflow: hidden; max-width: 100%;
  background:
    radial-gradient(circle at 30% 30%, color-mix(in srgb, var(--c) 70%, white 10%) 0 8%, transparent 9%),
    radial-gradient(circle at 62% 46%, color-mix(in srgb, var(--c) 80%, black 5%) 0 11%, transparent 12%),
    radial-gradient(circle at 42% 66%, color-mix(in srgb, var(--c) 65%, white 15%) 0 7%, transparent 8%),
    radial-gradient(circle at 74% 74%, color-mix(in srgb, var(--c) 75%, black 10%) 0 9%, transparent 10%),
    radial-gradient(circle at 24% 82%, color-mix(in srgb, var(--c) 60%, black 20%) 0 6%, transparent 7%),
    radial-gradient(ellipse 80% 70% at 50% 45%, color-mix(in srgb, var(--c) 45%, transparent), transparent 75%),
    linear-gradient(160deg, #19140F, #0B0907);
}
.nvis::before { content: ""; position: absolute; inset: 0; background: radial-gradient(circle at 50% 50%, transparent 40%, rgba(0,0,0,.55)); }
.nvis::after { content: ""; position: absolute; inset: 0; backdrop-filter: blur(1.5px); -webkit-backdrop-filter: blur(1.5px); }
.nvis span { position: absolute; z-index: 1; left: 12px; top: 10px; font-family: var(--font-display); font-size: 10px; letter-spacing: .2em; text-transform: uppercase; color: rgba(243, 235, 221, .8); }
.ntile b { font-family: var(--font-display); font-weight: 500; font-size: 17px; text-align: center; }
.ntile small { display: block; text-align: center; font-size: 12px; color: var(--muted); margin-top: -8px; }
@media (max-width: 520px) { .notes-grid { gap: 8px; } .ntile b { font-size: 14px; } .nvis span { font-size: 8.5px; left: 8px; } }

.card-media { box-shadow: none; }
:root[data-theme="dark"] .card-media, :root[data-theme="dark"] .d-media, :root[data-theme="dark"] .ci-media {
  background: radial-gradient(ellipse 60% 45% at 50% 55%, rgba(205, 168, 92, .18), transparent 70%), linear-gradient(180deg, #1C1712, #110E0B);
}
.card-name { font-weight: 500; }
.tab[aria-selected="true"] { background: var(--gold); color: var(--accent-fg); }
.cart-count { background: var(--gold); color: var(--accent-fg); }
.accord-fill { background: var(--gold); }
.dots i.on { background: var(--gold); }
.summary .row.total, .folio { color: var(--gold-soft); }


.nvis.photo { background: #0B0907; }
.nvis.photo img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; transition: transform .7s cubic-bezier(.2,.8,.2,1); }
.nvis.photo::before { z-index: 1; background: linear-gradient(180deg, rgba(0,0,0,.35), transparent 30%, transparent 70%, rgba(0,0,0,.35)); }
.nvis.photo::after { display: none; }
.nvis.photo span { z-index: 2; }
.ntile:hover .nvis.photo img { transform: scale(1.06); }

#drawer { width: min(1080px, 100%); }
#drawer .drawer-scroll { gap: 40px; padding: 28px clamp(16px, 3vw, 36px) 40px; }
.dx-top { display: grid; grid-template-columns: 1fr 1fr; gap: 36px; align-items: center; }
.dx-media { aspect-ratio: 4 / 5; }
.dx-copy { display: grid; gap: 16px; min-width: 0; }
.dx-copy h2 { font-size: clamp(30px, 3.6vw, 44px); line-height: 1.08; color: var(--gold-soft); }
.dx-copy p { margin: 0; color: var(--muted); }
.dx-copy p.lead { color: var(--fg); font-size: 16.5px; }
.dx-actions { display: grid; gap: 10px; }
.dx-actions small { font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }
.dx-notes { display: grid; gap: 18px; padding-top: 32px; border-top: 1px solid var(--line); }
.dx-notes h3 { font-family: var(--font-display); font-size: clamp(22px, 2.6vw, 30px) !important; font-weight: 500; letter-spacing: -.01em !important; text-transform: none !important; color: var(--fg) !important; }
.dx-notes p { margin: 0; color: var(--muted); max-width: 64ch; }
.dx-sim { padding-top: 32px; border-top: 1px solid var(--line); }
.dx-sim .sim-head .eyebrow { color: var(--gold, var(--accent)); }
.dx-more { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 32px; padding-top: 32px; border-top: 1px solid var(--line); }
.dx-more .d-section:first-child { grid-column: 1 / -1; }
@media (max-width: 900px) { .dx-top { grid-template-columns: 1fr; gap: 22px; } .dx-more { grid-template-columns: 1fr; } }
@media (max-width: 640px) {
  #drawer { top: 0; max-height: none; border-radius: 0; }
  #drawer .drawer-scroll { gap: 30px; }
}

.spot-media.has-scene { background: #0B0907; }
.spot-media.has-scene::after { display: none; }
.spot-media img.scene { left: 0; bottom: 0; top: 0; width: 100%; height: 100%; max-width: none; object-fit: cover; transform: none; filter: none; }
.spot-media.swap img.scene { opacity: 0; transform: scale(1.02); }

/* Envíos */''')

# ---------- Encabezado ----------
R('<span class="brand-name">Scantalia</span>', '<span><span class="brand-name">Scantalia</span><span class="brand-sub">El arte de la perfumería</span></span>')

# ---------- Portada: fragancia destacada + ingredientes ----------
a = s.index('  <div class="wrap hero">')
b = s.index('  <section class="block" id="perfumes"')
hero = '''  <section class="spot" aria-labelledby="spotTitle">
    <div class="wrap spot-grid">
      <div class="spot-media" id="spotMedia">
        <span class="spot-tag" id="spotTag"></span>
        <div class="spot-nav">
          <button type="button" id="spotPrev" aria-label="Fragancia anterior"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button>
          <button type="button" id="spotNext" aria-label="Fragancia siguiente"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button>
        </div>
      </div>
      <div class="spot-copy">
        <span class="eyebrow" id="spotEyebrow"></span>
        <h1 id="spotTitle"></h1>
        <p class="lead" id="spotLead"></p>
        <p id="spotBody"></p>
        <div class="spot-meta" id="spotMeta"></div>
        <div class="spot-actions">
          <button class="btn gold" type="button" id="spotCta">Descubre la fragancia →</button>
          <small id="heroShip">Envío gratis en 2 perfumes o más</small>
        </div>
      </div>
    </div>
  </section>

  <section class="notes-sec" aria-labelledby="notesTitle">
    <div class="wrap">
      <div class="notes-head">
        <span class="eyebrow">Pirámide olfativa</span>
        <h2 id="notesTitle">Más que un aroma, una declaración de estilo.</h2>
        <p id="notesText"></p>
      </div>
      <div class="notes-grid" id="notesGrid"></div>
    </div>
  </section>

'''
s = s[:a] + hero + s[b:]

# Catálogo
R('<h2 id="perfumes-title">Perfumes</h2>', '<h2 id="perfumes-title">Tu próxima fragancia favorita.</h2>')

# heroShip ya no tiene el texto largo: renderShipInfo lo sobrescribe; lo dejamos corto
R('$("heroShip").textContent = `Envío gratis a todo México en la compra de ${ENVIO.gratisDesde} perfumes o más.`;',
  '$("heroShip").textContent = `Envío gratis en ${ENVIO.gratisDesde} perfumes o más · Todo México`;')

# ---------- Tema: oscuro por defecto ----------
R('''function effectiveTheme() {
  const attr = document.documentElement.getAttribute("data-theme");
  if (attr === "dark" || attr === "light") return attr;
  return matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}''', '''function effectiveTheme() { return document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark"; }''')
R('''try { const t = localStorage.getItem("ag-theme"); if (t === "dark" || t === "light") document.documentElement.setAttribute("data-theme", t); } catch (e) {}''', '')
R('''  try { localStorage.setItem("ag-theme", next); } catch (e) {}''', '''  try { localStorage.setItem("ag2-theme", next); } catch (e) {}''')

# ---------- Lógica de la fragancia destacada ----------
R('renderAll();\n</script>', r'''/* ===== Fragancia destacada =====
   DESTACADO: id del perfume que aparece primero en la portada. */
const DESTACADO = "percival";
const NOTE_COLORS = {
  "cardamomo": "#7E9A52", "lavanda": "#7B62B8", "vainilla": "#C98E3E", "jazmín": "#E9DDB7", "caramelo": "#B9702D",
  "sal": "#BFC8CC", "iris": "#8C7BB8", "notas amaderadas": "#7A5434", "bergamota": "#C7C44F", "mandarina": "#E58A2B",
  "limón de amalfi": "#E5CF3E", "neroli": "#F0E2B0", "flor de naranjo": "#F2E6C2", "ámbar": "#C1782B", "toronja rosada": "#E07B6A",
  "grosella negra": "#5B2A4E", "vetiver": "#6B6B3A", "maderas secas": "#8A6A45", "notas marinas": "#3E7FA6", "mandarina verde": "#8EAF3A",
  "mimosa": "#E6C33A", "pachulí": "#6B4A2E", "ládano": "#8E5A2A", "oud": "#5A3A24", "trufa": "#4A3A30", "roble": "#7A5A3A",
  "salvia": "#8DA08A", "elemí": "#B9B77A", "geranio": "#C76A8A", "romero": "#6E8E6A", "angélica": "#A7B88A"
};
const TIER_COLORS = { salida: "#A9B45A", corazon: "#B07AA8", fondo: "#B9773A" };
const TIER_LABEL = { salida: "Salida", corazon: "Corazón", fondo: "Fondo" };
const TINT = p => p.liquido || "#E8A85A";
let spotIdx = Math.max(0, PERFUMES.findIndex(p => p.id === DESTACADO));


function sceneHTML(p) {
  if (!p.img) return media(p);
  return `<img class="spot-img scene" src="fotos/escenas/${p.id}.webp?v=4" alt="${p.marca} ${p.nombre}" onerror="this.onerror=null;this.classList.remove('scene');this.src='${p.img}'">`;
}

function notaInfo(p, t, i) {
  const k = (p.destacadas || [])[i];
  const n = k && typeof NOTAS !== "undefined" ? NOTAS[k] : null;
  const fallback = t === "salida" ? p.salida[0] : t === "corazon" ? p.corazon[0] : p.fondo[0];
  const foto = n && n.foto !== false ? (n.foto || k) : null;
  return { k: foto, nombre: n ? n.nombre : fallback, desc: n ? n.desc : TIER_LABEL[t], color: n && n.color };
}
function noteTiles(p) {
  return ["salida", "corazon", "fondo"].map((t, i) => {
    const n = notaInfo(p, t, i);
    const vis = n.k
      ? `<div class="nvis photo"><img src="fotos/notas/${n.k}.webp" alt="${n.nombre}" loading="lazy"><span>${TIER_LABEL[t]}</span></div>`
      : `<div class="nvis" style="--c:${n.color || NOTE_COLORS[n.nombre.toLowerCase()] || TIER_COLORS[t]}" aria-hidden="true"><span>${TIER_LABEL[t]}</span></div>`;
    return `<div class="ntile">${vis}<b>${n.nombre}</b><small>${n.desc}</small></div>`;
  }).join("");
}
const yo = t => t.toLowerCase().replace(" · ", " y ").replace(" y i", " e i");
function notesSentence(p) {
  const ns = ["salida", "corazon", "fondo"].map((t, i) => notaInfo(p, t, i).nombre.toLowerCase());
  return `La combinación de ${ns[0]}, ${ns[1]} y ${ns[2]} define el carácter de ${p.nombre}. Ideal para ${yo(p.temporada)}, especialmente en ${yo(p.ocasion)}.`;
}

/* Ficha editorial: reemplaza al panel original al abrir cualquier perfume */
function renderDrawer(p) {
  const sizes = p.pres.map(x => [x.ml, x.precio]);
  selectedSize = sizes[sizes.length - 1][0];
  const parts = p.venta.split(/(?<=\.)\s+/);
  const notes = arr => arr.map(n => `<span class="note">${n}</span>`).join("");
  $("drawerBody").innerHTML = `
    <div class="dx-top reveal">
      <div class="spot-media dx-media${p.img ? " has-scene" : ""}" style="--tint:${TINT(p)}">${sceneHTML(p)}<span class="spot-tag">${p.marca} · ${p.seccion}</span></div>
      <div class="dx-copy">
        <span class="eyebrow">${p.marca} · ${p.nombre}</span>
        <h2 id="dName">${p.lema}</h2>
        <p class="lead">${parts[0]}</p>
        <p>${parts.slice(1).join(" ")}</p>
        <div class="spot-meta"><span><b>${p.conc}</b></span><span>${p.familia}</span><span>Duración ${p.duracion}</span></div>
        <div class="sizes" role="radiogroup" aria-label="Presentación">${sizes.map(([ml, v]) => `
          <button class="size" type="button" role="radio" data-ml="${ml}" aria-checked="${ml === selectedSize}">
            <b>${ml} ml</b><span>${fmt.format(v)}</span>
          </button>`).join("")}
        </div>
        <div class="dx-actions">
          <button class="btn gold block" type="button" id="addCart">Agregar al carrito →</button>
          <button class="btn ghost block" type="button" id="viewCart">Ver carrito</button>
          <small>Envío gratis en ${ENVIO.gratisDesde} perfumes o más · Todo México</small>
        </div>
      </div>
    </div>
    <div class="dx-notes reveal" style="animation-delay:.08s">
      <span class="eyebrow">Notas principales</span>
      <h3>Más que un aroma, una declaración de estilo.</h3>
      <p>${notesSentence(p)}</p>
      <div class="notes-grid">${noteTiles(p)}</div>
    </div>
    <div class="dx-more reveal" style="animation-delay:.14s">
      <div class="d-section">
        <h3>Pirámide olfativa completa</h3>
        <div class="pyramid">
          <div class="tier"><div class="tier-label">Salida<small>primeros minutos</small></div><div class="tier-notes">${notes(p.salida)}</div></div>
          <div class="tier"><div class="tier-label">Corazón<small>1 a 3 horas</small></div><div class="tier-notes">${notes(p.corazon)}</div></div>
          <div class="tier"><div class="tier-label">Fondo<small>estela final</small></div><div class="tier-notes">${notes(p.fondo)}</div></div>
        </div>
      </div>
      <div class="d-section">
        <h3>Acordes principales</h3>
        <div class="accords">${p.acordes.map(([a, v]) => `
          <div class="accord"><span>${a}</span><div class="accord-track" role="img" aria-label="${a}: ${v} %"><div class="accord-fill" data-w="${v}"></div></div></div>`).join("")}
        </div>
      </div>
      <div class="d-section">
        <h3>Desempeño</h3>
        <div class="facts">
          <div class="fact"><span>Duración</span><b>${p.duracion}</b></div>
          <div class="fact"><span>Proyección</span><b>${dots(p.proyeccion)}</b></div>
          <div class="fact"><span>Temporada</span><b>${p.temporada}</b></div>
          <div class="fact"><span>Ocasión</span><b>${p.ocasion}</b></div>
        </div>
      </div>
    </div>
    <div class="dx-sim reveal" style="animation-delay:.2s">${similaresHTML(p)}</div>`;
}

function lista(arr) { return arr.length > 1 ? arr.slice(0, -1).join(", ") + " y " + arr[arr.length - 1] : arr[0]; }

function renderSpot(animate) {
  const p = PERFUMES[spotIdx]; const m = $("spotMedia");
  const apply = () => {
    m.style.setProperty("--tint", TINT(p));
    m.querySelector(".spot-img")?.remove();
    m.classList.toggle("has-scene", !!p.img);
    const tmp = document.createElement("div"); tmp.innerHTML = sceneHTML(p);
    const el = tmp.firstElementChild; el.classList.add("spot-img"); if (el.tagName === "IMG") el.loading = "eager"; m.insertBefore(el, m.firstChild);
    $("spotTag").textContent = `${p.marca} · ${p.seccion}`;
    $("spotEyebrow").textContent = `${p.marca} · ${p.conc} · ${p.familia}`;
    $("spotTitle").textContent = p.lema;
    const parts = p.venta.split(/(?<=\.)\s+/);
    $("spotLead").textContent = parts[0];
    $("spotBody").textContent = parts.slice(1).join(" ");
    $("spotMeta").innerHTML = `<span>${p.pres.map(x => x.ml + " ml").join(" · ")}</span><span><b>${fmt.format(minPrice(p))}</b></span><span>Duración ${p.duracion}</span>`;
    $("notesText").textContent = notesSentence(p);
    $("notesGrid").innerHTML = noteTiles(p);
    m.classList.remove("swap");
  };
  if (animate) { m.classList.add("swap"); setTimeout(apply, 260); } else apply();
}
$("spotPrev").addEventListener("click", () => { spotIdx = (spotIdx - 1 + PERFUMES.length) % PERFUMES.length; renderSpot(true); });
$("spotNext").addEventListener("click", () => { spotIdx = (spotIdx + 1) % PERFUMES.length; renderSpot(true); });
$("spotCta").addEventListener("click", e => openDrawer(PERFUMES[spotIdx].id, e.currentTarget));

renderSpot(false);
renderAll();
</script>''')

open(DST, 'w', encoding='utf-8').write(s)
print('ok', len(s))
