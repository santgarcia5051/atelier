#!/usr/bin/env python3
"""Construye prueba.html con el diseño "Mostrador de recetas":
negro (modo oscuro, predeterminado) o papel (modo claro); portada = receta de notas en foto + frasco;
búsqueda por nota; mostrador en 2 columnas con mini fotos de notas y ficha-receta fija a la derecha;
pensado primero para celular. Parte de index.html, así que conserva ficha, similares, carrito, pedido,
envíos, contacto, aviso de privacidad y cookies.

Uso: python3 scripts/construir_recetas.py
"""
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(RAIZ, "index.html"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    assert old in s, "no encontré: " + old[:90]
    s = s.replace(old, new, n)


def cortar(ini, fin, nuevo):
    global s
    i = s.index(ini); j = s.index(fin, i)
    s = s[:i] + nuevo + s[j:]


# ---------------------------------------------------------------- fuentes y tema predeterminado oscuro
rep('family=Jost:wght@300;400;500&family=Albert+Sans:wght@400;500;600&display=swap',
    'family=Big+Shoulders+Display:wght@700;900&family=IBM+Plex+Mono:wght@400;500;600&family=Courier+Prime:wght@400;700&family=Archivo:wght@400;500;600&display=swap')
rep('<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="theme-color" content="#0F0F0E">\n'
    '<script>try{var t=localStorage.getItem("ag-theme");document.documentElement.setAttribute("data-theme",t==="light"?"light":"dark")}catch(e){document.documentElement.setAttribute("data-theme","dark")}</script>')

CSS = r"""
<style id="tema-recetas">
/* Mostrador de recetas. Oscuro (predeterminado): negro, tinta crema, rojo de sello.
   Claro: papel con tinta negra. Letra: Big Shoulders (nombres), IBM Plex Mono (texto), Courier Prime (fichas). */
:root, :root[data-theme="dark"] {
  --bg: #0F0F0E; --surface: #171715; --tile: #1E1D1B; --fg: #ECE9E2; --muted: #9C988F; --line: #2A2926; --line2: #2A2926;
  --accent: #D2452B; --accent-fg: #FFFFFF; --paper: #ECE9E2; --ink: #111110; --dim: #4A4843;
  --overlay: rgba(0,0,0,.7); --shadow: 0 30px 60px -20px rgba(0,0,0,.8); --glow: rgba(210,69,43,.12); --danger: #E2907F; --ok: #A3C495;
  --font-display: "Big Shoulders Display", Impact, "Arial Narrow", sans-serif;
  --font-body: "IBM Plex Mono", ui-monospace, Menlo, monospace;
  --font-type: "Courier Prime", "Courier New", monospace;
  --r-sm: 0; --r-md: 0; --r-lg: 0; color-scheme: dark;
}
:root[data-theme="light"] {
  --bg: #EFEDE7; --surface: #F8F6F1; --tile: #E3E0D8; --fg: #141413; --muted: #6E6B64; --line: #141413; --line2: #CFCBC2;
  --accent: #C23B22; --accent-fg: #FFFFFF; --paper: #F8F6F1; --ink: #141413; --dim: #B5B0A6;
  --overlay: rgba(20,20,19,.5); --shadow: 0 26px 50px -20px rgba(0,0,0,.3); --glow: rgba(194,59,34,.08); --danger: #A6463A; --ok: #4C6A43;
  color-scheme: light;
}
body { background: var(--bg); color: var(--fg); font-family: var(--font-body); font-size: 14px; }
:root[data-theme="light"] body { background-image: radial-gradient(rgba(0,0,0,.03) 1px, transparent 1px); background-size: 4px 4px; }
h1, h2, h3 { font-family: var(--font-display); font-weight: 900; text-transform: uppercase; letter-spacing: -.005em; }
.eyebrow { font-family: var(--font-body); letter-spacing: .1em; color: var(--muted); }
.wrap { max-width: 1440px; }
.btn { border-radius: 0 !important; font-family: var(--font-body); text-transform: uppercase; letter-spacing: .1em; font-size: 12px; font-weight: 500; }
.btn:not(.ghost) { background: var(--fg); color: var(--bg); border-color: var(--fg); }
.btn:hover { background: var(--accent) !important; border-color: var(--accent) !important; color: #fff !important; opacity: 1 !important; }
section.block { border-top: 1px solid var(--line); padding-block: 56px; }
.block-head h2 { font-size: clamp(44px, 7vw, 80px); line-height: .9; font-weight: 900; }

/* Encabezado */
.rtop { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 40; background: color-mix(in srgb, var(--bg) 92%, transparent); backdrop-filter: blur(12px); border-bottom: 1px solid var(--line); }
.rtop-in { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 12px; padding: 12px max(16px, env(safe-area-inset-right, 0px)) 12px max(16px, env(safe-area-inset-left, 0px)); max-width: 1440px; margin: 0 auto; }
.rtop nav { display: flex; gap: 22px; font-size: 12px; text-transform: uppercase; letter-spacing: .08em; }
.rtop nav button, .rtop nav a { padding: 6px 0; text-decoration: none; position: relative; background: none; border: 0; cursor: pointer; }
.rtop nav button::after, .rtop nav a::after { content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 1.5px; background: var(--accent); transform: scaleX(0); transform-origin: left; transition: transform .35s; }
.rtop nav button:hover::after, .rtop nav a:hover::after { transform: scaleX(1); }
.rlogo { font-family: var(--font-display); font-weight: 900; font-size: 30px; letter-spacing: .04em; text-decoration: none; text-align: center; }
.top-actions { justify-self: end; display: flex; gap: 8px; }
.theme-toggle { border-radius: 0 !important; border: 1px solid var(--line2) !important; background: transparent !important; color: var(--fg) !important; font-family: var(--font-body) !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: .08em; }
.cart-btn { background: var(--fg) !important; color: var(--bg) !important; border-color: var(--fg) !important; }
.cart-count { background: var(--accent) !important; color: #fff !important; border-radius: 0 !important; }
.cart-count.bump { animation: pop .5s; }

/* Franja de marcas */
.ticker { border-bottom: 1px solid var(--line); overflow: hidden; white-space: nowrap; padding: 9px 0; font-size: 11px; text-transform: uppercase; letter-spacing: .12em; color: var(--muted); }
.ticker > div { display: inline-flex; gap: 30px; padding-right: 30px; animation: marq 45s linear infinite; }
.ticker i { color: var(--accent); font-style: normal; }

/* Portada: receta */
.rhero { display: grid; grid-template-columns: 1fr 1.1fr; border-bottom: 1px solid var(--line); min-height: 560px; max-width: 1440px; margin: 0 auto; }
.rhero .hl { padding: 40px 32px; display: flex; flex-direction: column; justify-content: space-between; gap: 28px; border-right: 1px solid var(--line); min-width: 0; }
.rhero .k { font-size: 12px; text-transform: uppercase; letter-spacing: .1em; color: var(--muted); }
.rhero h1 { font-family: var(--font-type); font-weight: 400; text-transform: none; font-size: clamp(30px, 3.6vw, 52px); line-height: 1.06; letter-spacing: -.02em; }
.rhero h1 b { display: block; font-family: var(--font-display); font-weight: 900; text-transform: uppercase; font-size: clamp(84px, 11vw, 168px); line-height: .84; letter-spacing: -.01em; margin-top: 8px; word-break: break-word; }
.rhero p { line-height: 1.7; color: var(--muted); max-width: 46ch; margin: 0; }
.rhero .ctas { display: flex; flex-wrap: wrap; gap: 10px; }
.rhero .hr { display: grid; grid-template-columns: repeat(3, 1fr); position: relative; min-height: 460px; overflow: hidden; }
.rhero .col { position: relative; overflow: hidden; border-right: 1px solid var(--line); background: var(--tile); }
.rhero .col:last-of-type { border-right: 0; }
.rhero .col img { width: 100%; height: 100%; object-fit: cover; filter: brightness(.72); animation: wipe 1.1s cubic-bezier(.16,.8,.2,1) both; }
.rhero .col:nth-child(2) img { animation-delay: .15s; } .rhero .col:nth-child(3) img { animation-delay: .3s; }
.rhero .col span { position: absolute; left: 12px; top: 14px; font-family: var(--font-display); font-weight: 900; font-size: clamp(26px, 3.4vw, 46px); text-transform: uppercase; line-height: 1; color: #fff; text-shadow: 0 2px 20px rgba(0,0,0,.45); }
.rhero .col span small { display: block; font-family: var(--font-body); font-weight: 400; font-size: 11px; letter-spacing: .08em; color: #eee; }
.rhero .hbt { position: absolute; left: 50%; bottom: 0; transform: translateX(-50%); height: 88%; max-width: 70%; object-fit: contain; z-index: 2; filter: drop-shadow(0 30px 40px rgba(0,0,0,.8)); animation: float 7s ease-in-out infinite; }
.rhero .hbt.blanco { mix-blend-mode: multiply; filter: none; }
.rhero .stamp { position: absolute; z-index: 3; left: 16px; bottom: 22px; width: 112px; height: 112px; border: 3px solid var(--accent); border-radius: 50%; color: var(--accent); display: flex; flex-direction: column; align-items: center; justify-content: center; font-weight: 600; text-transform: uppercase; font-size: 10px; letter-spacing: .06em; transform: rotate(-14deg); animation: stamp .7s cubic-bezier(.2,1.6,.4,1) 1.1s both; background: color-mix(in srgb, var(--bg) 55%, transparent); }
.rhero .stamp b { font-family: var(--font-type); font-size: 30px; line-height: 1; }
.rhero .lbl { position: absolute; z-index: 3; right: 16px; bottom: 20px; background: var(--paper); color: #111; padding: 10px 13px; font-size: 12px; transform: rotate(-2deg); box-shadow: 6px 6px 0 var(--accent); max-width: 60%; }
.rhero .lbl b { display: block; font-family: var(--font-type); font-size: 20px; }

/* Buscar por nota */
.notas { display: flex; align-items: stretch; border-bottom: 1px solid var(--line); max-width: 1440px; margin: 0 auto; }
.notas .q { padding: 14px 24px; font-family: var(--font-type); font-size: 20px; border-right: 1px solid var(--line); white-space: nowrap; display: flex; align-items: center; }
.notas .ch { display: flex; overflow-x: auto; scroll-snap-type: x proximity; scrollbar-width: none; -webkit-overflow-scrolling: touch; }
.notas .ch::-webkit-scrollbar { display: none; }
.notas button { flex: none; display: flex; align-items: center; gap: 10px; padding: 8px 16px 8px 8px; border: 0; border-right: 1px solid var(--line); background: transparent; color: var(--fg); font: 500 12px var(--font-body); text-transform: uppercase; letter-spacing: .06em; white-space: nowrap; cursor: pointer; scroll-snap-align: start; transition: background .2s, color .2s; }
.notas button img, .notas button i { width: 42px; height: 42px; object-fit: cover; filter: grayscale(1) brightness(.85); transition: filter .3s; display: block; }
.notas button:hover, .notas button[aria-pressed="true"] { background: var(--accent); color: #fff; }
.notas button:hover img, .notas button[aria-pressed="true"] img { filter: none; }

/* Mostrador */
#perfumes { padding-top: 0 !important; border-top: 0 !important; }
#perfumes .block-head { padding: 26px 0 8px; margin: 0; }
.tabs { border-radius: 0 !important; background: transparent !important; border: 0 !important; padding: 0 !important; gap: 0 !important; margin: 0 0 0 !important; display: flex !important; border-top: 1px solid var(--line) !important; }
.tab { border-radius: 0 !important; flex: 1; justify-content: center; border-right: 1px solid var(--line) !important; padding: 14px 10px !important; font-family: var(--font-body) !important; font-size: 12px !important; }
.tab:last-child { border-right: 0 !important; }
.tab[aria-selected="true"] { background: var(--fg) !important; color: var(--bg) !important; }
.select-wrap select { border-radius: 0 !important; font-family: var(--font-body); font-size: 12px; background: var(--surface); }
.split { display: grid; grid-template-columns: 1.4fr .6fr; align-items: start; border-top: 1px solid var(--line); }
.lst { border-right: 1px solid var(--line); min-width: 0; }
.lst .hd { display: flex; justify-content: space-between; gap: 12px; padding: 12px 20px; font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); border-bottom: 1px solid var(--line); }
#grid { display: grid !important; grid-template-columns: 1fr 1fr !important; gap: 0 !important; }
.it { position: relative; display: grid; grid-template-columns: 1fr auto; text-align: left; padding: 14px 20px; border: 0; border-bottom: 1px solid var(--line); border-right: 1px solid var(--line); background: transparent; color: var(--fg); cursor: pointer; overflow: hidden; min-width: 0; font: inherit; }
.it:nth-child(2n) { border-right: 0; }
.it::before { content: ""; position: absolute; inset: 0; background: var(--accent); transform: scaleX(0); transform-origin: left; transition: transform .5s cubic-bezier(.16,.8,.2,1); }
.it > * { position: relative; min-width: 0; }
.it .n { grid-column: 1 / -1; font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.it .n b { color: var(--accent); font-weight: 600; }
.it .t { grid-column: 1; font-family: var(--font-display); font-weight: 900; font-size: clamp(34px, 3.3vw, 46px); line-height: .98; text-transform: uppercase; color: var(--dim); margin: 3px 0 8px; transition: color .3s, transform .5s cubic-bezier(.16,.8,.2,1); overflow-wrap: anywhere; }
.it .mn { grid-column: 1; display: flex; gap: 4px; align-items: center; min-width: 0; }
.it .mn img, .it .mn i { width: 30px; height: 30px; object-fit: cover; flex: none; filter: grayscale(1) brightness(.75); transition: filter .4s; display: block; }
.it .mn em { font-style: normal; font-size: 11px; color: var(--muted); margin-left: 6px; text-transform: uppercase; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.it .p { grid-column: 2; grid-row: 2 / 4; align-self: end; text-align: right; font-family: var(--font-type); font-size: 22px; color: var(--muted); padding-left: 10px; white-space: nowrap; }
.it .p s { display: block; font-size: 12px; opacity: .7; }
.it .th { display: none; }
.it .qa { position: absolute; right: 14px; top: 12px; width: 34px; height: 34px; border: 1px solid var(--line2); display: flex; align-items: center; justify-content: center; font-size: 18px; color: var(--fg); background: var(--bg); transition: all .3s; z-index: 2; }
.it .qa.ok { background: var(--accent); border-color: var(--accent); color: #fff; }
.it.off .t { text-decoration: line-through; text-decoration-thickness: 3px; }
.it.off .qa { display: none; }
@media (hover: hover) {
  .it:hover .t, .it.sel .t { color: var(--fg); transform: translateX(8px); }
  .it:hover .mn img, .it.sel .mn img { filter: none; }
  .it.sel::before { transform: scaleX(1); }
  .it.sel .t, .it.sel .n, .it.sel .p, .it.sel .mn em, .it.sel .n b { color: #fff; }
  .it .qa:hover { background: var(--fg); color: var(--bg); }
}
.side { position: sticky; top: calc(64px + env(safe-area-inset-top, 0px)); padding: 20px; }
.rcard { background: var(--paper); color: #111; padding: 20px 22px; position: relative; box-shadow: 8px 8px 0 var(--accent); }
.rcard .rn { font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: #555; padding-right: 80px; display: block; }
.rcard h3 { font-family: var(--font-display); font-weight: 900; font-size: clamp(44px, 4.2vw, 62px); line-height: .88; margin-top: 6px; animation: up .5s cubic-bezier(.16,.8,.2,1); }
.rcard .lm { font-family: var(--font-type); font-size: 17px; margin: 6px 0 14px; }
.eqn { display: grid; grid-template-columns: repeat(3, 1fr) 1.15fr; gap: 6px; height: 190px; }
.eqn .ph { position: relative; overflow: hidden; background: #ddd; }
.eqn .ph img { width: 100%; height: 100%; object-fit: cover; animation: wipe .7s cubic-bezier(.16,.8,.2,1) both; display: block; }
.eqn .ph:nth-child(2) img { animation-delay: .08s; } .eqn .ph:nth-child(3) img { animation-delay: .16s; }
.eqn .ph span { position: absolute; left: 5px; bottom: 5px; right: 5px; font-size: 9.5px; text-transform: uppercase; padding: 3px 5px; line-height: 1.25; background: var(--paper); color: #111; }
.eqn .ph span b { display: block; font-family: var(--font-type); font-size: 13px; text-transform: none; }
.eqn .eqb { display: flex; align-items: center; gap: 2px; min-width: 0; }
.eqn .eqb i { font-style: normal; font-family: var(--font-display); font-weight: 900; font-size: 36px; }
.eqn .eqb img { max-height: 180px; max-width: 82%; object-fit: contain; mix-blend-mode: multiply; animation: up .6s .2s cubic-bezier(.16,.8,.2,1) both; }
.rcard .row { display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-top: 16px; flex-wrap: wrap; }
.rcard .pr { font-family: var(--font-type); font-size: 30px; }
.rcard .pr s { font-size: 14px; color: #777; margin-left: 8px; }
.rcard .bts { display: flex; gap: 6px; }
.rcard .bts button { padding: 13px 14px; font: 600 11px var(--font-body); text-transform: uppercase; letter-spacing: .08em; cursor: pointer; border: 1.5px solid #111; background: transparent; color: #111; }
.rcard .bts .ad { background: #111; color: #fff; }
.rcard .bts button:hover { background: var(--accent); border-color: var(--accent); color: #fff; }
.rcard .stp { position: absolute; right: 16px; top: 14px; width: 74px; height: 74px; border: 2.5px solid var(--accent); border-radius: 50%; color: var(--accent); display: flex; align-items: center; justify-content: center; font-family: var(--font-type); font-weight: 700; font-size: 21px; transform: rotate(-12deg); }
.vacio { grid-column: 1 / -1; padding: 40px 20px; color: var(--muted); }

/* Resto de la página con el mismo lenguaje */
.ship, .ship-grid > *, .zone, .social, .small-btn, .field input, .field textarea, .order-box, .d-section, .sim-card, .cookies, .toast { border-radius: 0 !important; }
.zone { background: var(--surface) !important; border: 1px solid var(--line2) !important; }
.zone b { font-family: var(--font-type); font-size: 26px; font-weight: 400; }
.social { border: 1px solid var(--line2) !important; }
.social-name { font-family: var(--font-display); font-weight: 900; font-size: 26px; text-transform: uppercase; }
footer { border-top: 1px solid var(--line); font-size: 12px; }
.drawer { background: var(--bg) !important; border-left: 1px solid var(--line); }
#dName { font-size: clamp(44px, 9vw, 64px) !important; line-height: .9 !important; }
.foto-tienda-wrap, .d-media.foto-tienda-wrap, .dx-media.foto-tienda-wrap { background: var(--paper) !important; }
.sim-card { border-color: var(--line2) !important; }
.cookies b { font-family: var(--font-display); font-weight: 900; text-transform: uppercase; font-size: 22px; }
.cookies { background: var(--paper) !important; color: #111 !important; box-shadow: 8px 8px 0 var(--accent) !important; border: 0 !important; }
.cookies p { color: #444 !important; } .cookies button { border-color: #111 !important; color: #111 !important; border-radius: 0 !important; } .cookies button.ck-ok { background: #111 !important; color: #fff !important; }

/* Animaciones */
@keyframes up { from { opacity: 0; transform: translateY(26px); } to { opacity: 1; transform: none; } }
@keyframes fade { from { opacity: 0; } to { opacity: 1; } }
@keyframes marq { to { transform: translateX(-50%); } }
@keyframes float { 0%,100% { transform: translate(-50%, 0); } 50% { transform: translate(-50%, -12px); } }
@keyframes wipe { from { clip-path: inset(0 100% 0 0); } to { clip-path: inset(0 0 0 0); } }
@keyframes stamp { from { opacity: 0; transform: rotate(-14deg) scale(2.2); } to { opacity: 1; transform: rotate(-14deg) scale(1); } }
@keyframes letter { from { transform: translateY(105%); } to { transform: none; } }
@keyframes blink { 50% { opacity: 0; } }
@keyframes pop { 0% { transform: scale(1); } 40% { transform: scale(1.45); } 100% { transform: scale(1); } }
.lt { display: inline-block; overflow: hidden; vertical-align: bottom; }
.lt > span { display: inline-block; animation: letter 1s cubic-bezier(.16,.8,.2,1) both; }
.cur { display: inline-block; width: .5em; height: .9em; background: currentColor; vertical-align: -.1em; animation: blink 1s steps(1) infinite; margin-left: .1em; }
.u { animation: up .9s cubic-bezier(.16,.8,.2,1) both; } .u2 { animation-delay: .1s; } .u3 { animation-delay: .2s; } .u4 { animation-delay: .3s; }
.js-anim .sr { opacity: 0; transform: translateY(22px); transition: opacity .7s cubic-bezier(.16,.8,.2,1), transform .7s cubic-bezier(.16,.8,.2,1); }
.js-anim .sr.in { opacity: 1; transform: none; }

/* ===== Celular ===== */
@media (max-width: 900px) {
  .rtop-in { grid-template-columns: auto 1fr; }
  .rtop nav { display: none; }
  .rlogo { text-align: left; font-size: 26px; }
  #themeLabel, .cart-label { display: none; }
  .rhero { grid-template-columns: 1fr; min-height: 0; }
  .rhero .hl { border-right: 0; padding: 26px 16px 22px; gap: 18px; }
  .rhero h1 b { font-size: clamp(64px, 20vw, 110px); }
  .rhero .hr { min-height: 380px; border-top: 1px solid var(--line); }
  .rhero .ctas .btn { flex: 1; }
  .notas .q { display: none; }
  .notas button { padding: 6px 12px 6px 6px; }
  .split { grid-template-columns: 1fr; }
  .side { display: none; }
  .lst { border-right: 0; }
  .lst .hd span:last-child { display: none; }
  #grid { grid-template-columns: 1fr !important; }
  .it { border-right: 0; grid-template-columns: 1fr 78px; padding: 14px 16px; }
  .it .th { display: flex; grid-column: 2; grid-row: 2 / 4; align-items: center; justify-content: center; background: var(--paper); height: 92px; margin-left: 10px; }
  .it .th img { max-height: 84px; max-width: 64px; object-fit: contain; mix-blend-mode: multiply; }
  .it .p { grid-column: 1; grid-row: auto; text-align: left; padding: 8px 0 0; font-size: 20px; }
  .it .p s { display: inline; margin-left: 6px; }
  .it .qa { width: 40px; height: 40px; top: auto; bottom: 12px; right: 104px; }
  .it .t { font-size: clamp(32px, 10vw, 44px); }
  #perfumes .block-head { padding-top: 18px; }
  .controls { width: 100%; justify-content: space-between; }
}
@media (max-width: 900px) {
  .cookies { padding: 14px 16px !important; gap: 12px !important; bottom: calc(10px + env(safe-area-inset-bottom, 0px)) !important; }
  .cookies b { font-size: 16px !important; } .cookies p { font-size: 12px !important; line-height: 1.45 !important; }
  .cookies .ck-btns { flex-wrap: nowrap; } .cookies button { flex: 1; padding: 10px 8px !important; font-size: 12px !important; }
  .rtop-in { padding-block: 10px; } .rlogo { font-size: 24px; }
  .theme-toggle { padding: 8px 10px !important; }
}
@media (max-width: 400px) { .rhero .stamp { width: 92px; height: 92px; } .rhero .stamp b { font-size: 24px; } .rhero .lbl { font-size: 11px; } }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
  .js-anim .sr { opacity: 1; transform: none; }
}
</style>
"""
rep("</head>", CSS + "</head>")

# ---------------------------------------------------------------- encabezado, franja y portada
cortar('<header class="top">', '<main id="inicio">', '''<header class="rtop">
  <div class="rtop-in">
    <nav aria-label="Secciones"><button type="button" data-ir="Mujer">Mujer</button><button type="button" data-ir="Hombre">Hombre</button><button type="button" data-ir="Unisex">Unisex</button><a href="#envios">Envíos</a></nav>
    <a class="rlogo" href="#inicio" aria-label="Scantalia, inicio">SCANTALIA</a>
    <div class="top-actions">
      <button class="theme-toggle" id="themeToggle" type="button" aria-label="Cambiar entre modo claro y oscuro">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 1 0 16z" fill="currentColor"/></svg>
        <span id="themeLabel">Modo claro</span>
      </button>
      <button class="theme-toggle cart-btn" id="cartBtn" type="button" aria-label="Abrir carrito">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 8h14l-1.2 11.2a1 1 0 0 1-1 .8H7.2a1 1 0 0 1-1-.8z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/></svg>
        <span class="cart-label">Bolsa</span>
        <span class="cart-count" id="cartCount">0</span>
      </button>
    </div>
  </div>
</header>
<div class="ticker" aria-hidden="true"><div id="ticker"></div></div>

''')
cortar('  <div class="wrap hero">', '  <section class="block" id="perfumes"', '''  <section class="rhero" aria-label="Receta destacada">
    <div class="hl">
      <div class="k u">Recetario · <span id="stTotal">330</span> fragancias originales</div>
      <h1 id="heroEq" class="u u2">Bergamota + vetiver + pachulí =<b>Explorer</b></h1>
      <div class="u u3"><p>Cada perfume es una receta. Elija por sus ingredientes y llévelo original, sellado y por debajo del precio de tienda departamental. <span id="heroShip">Envío gratis a todo México en la compra de 2 perfumes o más.</span><span class="cur"></span></p></div>
      <div class="ctas u u4"><a class="btn" href="#perfumes">Ver el mostrador</a><a class="btn ghost" href="#notas">Buscar por nota</a></div>
    </div>
    <div class="hr" id="heroCols"></div>
  </section>
  <div class="notas" id="notas"><span class="q">Mi receta lleva…</span><div class="ch" id="notaChips" role="group" aria-label="Buscar por nota"></div></div>

''')

# ---------------------------------------------------------------- mostrador
rep('''      <div class="tabs" id="chips" role="tablist" aria-label="Sección"></div>
      <div class="grid" id="grid"></div>''', '''      <div class="tabs" id="chips" role="tablist" aria-label="Sección"></div>
    </div>
    <div class="split">
      <div class="lst"><div class="hd"><span id="lstHd">Mostrador</span><span>Pase el cursor: la receta aparece a la derecha</span></div><div class="grid" id="grid"></div></div>
      <aside class="side" id="side" aria-live="polite"></aside>''')

# renderGrid nuevo
i = s.index("function renderGrid() {")
j = s.index("\nfunction renderTable()", i)
s = s[:i] + r'''function renderGrid() {
  const list = sorted(PERFUMES).filter(p => p.seccion === state.seccion && cumpleNota(p));
  $("count").textContent = `${list.length} ${list.length === 1 ? "fragancia" : "fragancias"}`;
  const nota = state.nota ? ` · con ${NOTAS[state.nota] ? NOTAS[state.nota].nombre.toLowerCase() : state.nota}` : "";
  $("lstHd").textContent = `Mostrador · ${state.seccion}${nota} · ${list.length}`;
  $("grid").innerHTML = list.length ? list.map(p => {
    const ns = notas3(p), d = descPct(p);
    return `<button class="it sr${disponible(p) ? "" : " off"}" type="button" data-id="${p.id}" aria-label="Ver ficha de ${p.nombre}">
      <span class="n">${p.marca} · ${p.conc} · ${p.pres[0].ml} ml${d ? ` · <b>−${d}%</b>` : ""}${disponible(p) ? "" : " · <b>No disponible</b>"}</span>
      <span class="t">${p.nombre}</span>
      <span class="mn">${ns.map(n => notaImg(n)).join("")}<em>${ns.map(n => n.nombre).join(" + ")}</em></span>
      <span class="p">${precioCorto(p)}</span>
      <span class="th">${p.img ? `<img src="${p.img}" alt="" loading="lazy" referrerpolicy="no-referrer">` : ""}</span>
      ${disponible(p) ? `<span class="qa" role="button" tabindex="0" data-add="${p.id}" aria-label="Agregar ${p.nombre} a la bolsa">+</span>` : ""}
    </button>`;
  }).join("") : `<p class="vacio">No hay fragancias con esa nota en esta sección. Pruebe otra nota o quite el filtro.</p>`;
  const prim = list.find(disponible) || list[0];
  if (prim) mostrarReceta(prim.id); else $("side").innerHTML = "";
}
''' + s[j:]

rep('$("grid").addEventListener("click", e => { const c = e.target.closest(".card"); if (c) openDrawer(c.dataset.id, c); });',
    '''$("grid").addEventListener("click", e => {
  const a = e.target.closest(".qa");
  if (a) { e.stopPropagation(); const p = PERFUMES.find(x => x.id === a.dataset.add); if (p && disponible(p)) { addToCart(p.id, p.pres[0].ml); gustoSumar(p.id, 3); a.classList.add("ok"); a.textContent = "✓"; setTimeout(() => { a.classList.remove("ok"); a.textContent = "+"; }, 1300); } return; }
  const c = e.target.closest(".it"); if (c) openDrawer(c.dataset.id, c); });
$("grid").addEventListener("keydown", e => { const a = e.target.closest(".qa"); if (a && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); e.stopPropagation(); a.click(); } });
$("grid").addEventListener("mouseover", e => { const c = e.target.closest(".it"); if (c && matchMedia("(hover: hover)").matches) mostrarReceta(c.dataset.id); });''')

APOYO = r'''
/* ===== Mostrador de recetas ===== */
const FOTO_NOTA = new Set(%FOTOS%);
const ALIAS_NOTA = { sandalo: "maderas", cedro: "maderas", azahar: "neroli", azucena: "tuberosa", musgo: "vetiver", almizcle: "ambar", incienso: "oud", te: "menta", pimienta_rosa: "pimienta" };
const ETAPA = ["Salida", "Corazón", "Fondo"];
function claveFoto(k) { if (FOTO_NOTA.has(k)) return k; const a = ALIAS_NOTA[k]; return a && FOTO_NOTA.has(a) ? a : null; }
const sinAc = t => (t || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
const NOMBRE_FOTO = [["notas marinas", "mar"], ["marin", "mar"], ["acuat", "mar"], ["oceano", "mar"], ["azahar", "neroli"], ["tonka", "haba"], ["sandalo", "maderas"], ["cedro", "maderas"], ["madera", "maderas"], ["amaderad", "maderas"], ["almizcle", "ambar"], ["ambar", "ambar"], ["chocolate", "cacao"], ["naranja", "mandarina"], ["lima", "limon"], ["citric", "limon"], ["higo", "maderas"], ["incienso", "oud"], ["cachemira", "maderas"], ["praline", "caramelo"], ["tofe", "caramelo"], ["toffee", "caramelo"]];
function fotoDeNombre(n) {
  const t = sinAc(n);
  for (const k of FOTO_NOTA) if (t.includes(k)) return k;
  for (const [a, k] of NOMBRE_FOTO) if (t.includes(a) && FOTO_NOTA.has(k)) return k;
  return null;
}
function notas3(p) {
  const nombres = [p.salida[0], p.corazon[0], p.fondo[0]];
  return nombres.map((nombre, i) => {
    const k = (p.destacadas || [])[i];
    return { clave: k, foto: nombre ? fotoDeNombre(nombre) : claveFoto(k), nombre: nombre || (NOTAS[k] && NOTAS[k].nombre) || k, color: (NOTAS[k] && NOTAS[k].color) || "#6E6B64", etapa: ETAPA[i] };
  }).filter(n => n.nombre);
}

function notaImg(n) { return n.foto ? `<img src="fotos/notas/${n.foto}.webp" alt="" loading="lazy">` : `<i style="background:${n.color}"></i>`; }
function descPct(p) { return disponible(p) && p.antes && p.pres.length === 1 && p.antes > p.pres[0].precio ? Math.round((1 - p.pres[0].precio / p.antes) * 100) : 0; }
function precioCorto(p) {
  if (!disponible(p)) return "Agotado";
  const d = descPct(p);
  return p.pres.length > 1 ? `Desde ${fmt.format(minPrice(p))}` : `${fmt.format(p.pres[0].precio)}${d ? `<s>${fmt.format(p.antes)}</s>` : ""}`;
}
const fotoBlanca = p => /^https?:/.test(p.img || "") && !p.recorte;
function mostrarReceta(id) {
  const p = PERFUMES.find(x => x.id === id); if (!p) return;
  document.querySelectorAll("#grid .it.sel").forEach(x => x.classList.remove("sel"));
  const it = document.querySelector(`#grid .it[data-id="${CSS.escape(id)}"]`); if (it) it.classList.add("sel");
  const side = $("side"); if (side.dataset.id === id) return; side.dataset.id = id;
  const d = descPct(p), ns = notas3(p);
  side.innerHTML = `<div class="rcard">${d ? `<span class="stp">−${d}%</span>` : ""}<span class="rn">Receta · ${p.marca} · ${p.conc} · ${p.pres.map(x => x.ml + " ml").join(" / ")}</span><h3>${p.nombre}</h3><div class="lm">“${p.lema}”</div>
    <div class="eqn">${ns.map(n => `<div class="ph">${n.foto ? `<img src="fotos/notas/${n.foto}.webp" alt="">` : `<div style="background:${n.color};width:100%;height:100%"></div>`}<span>${n.etapa}<b>${n.nombre}</b></span></div>`).join("")}<div class="eqb"><i>=</i>${p.img ? `<img src="${p.img}" alt="${p.nombre}" referrerpolicy="no-referrer">` : ""}</div></div>
    <div class="row"><span class="pr">${disponible(p) ? fmt.format(minPrice(p)) : "No disponible"}${d ? `<s>${fmt.format(p.antes)}</s>` : ""}</span><span class="bts"><button type="button" data-ficha="${p.id}">Ver ficha</button>${disponible(p) ? `<button type="button" class="ad" data-add="${p.id}">+ Apartar</button>` : ""}</span></div></div>`;
}
$("side").addEventListener("click", e => {
  const f = e.target.closest("[data-ficha]"); if (f) { openDrawer(f.dataset.ficha, f); return; }
  const a = e.target.closest("[data-add]"); if (a) { const p = PERFUMES.find(x => x.id === a.dataset.add); if (p) { addToCart(p.id, p.pres[0].ml); gustoSumar(p.id, 3); } }
});
/* Buscar por nota */
state.nota = "";
function cumpleNota(p) {
  if (!state.nota) return true;
  if ((p.destacadas || []).includes(state.nota) || [...p.salida, ...p.corazon, ...p.fondo].some(n => fotoDeNombre(n) === state.nota)) return true;
  const nom = NOTAS[state.nota] ? NOTAS[state.nota].nombre.toLowerCase() : state.nota;
  return [...p.salida, ...p.corazon, ...p.fondo].join(" ").toLowerCase().includes(nom.slice(0, 5));
}
(function chipsNotas() {
  const cuenta = {};
  PERFUMES.forEach(p => new Set([...p.salida, ...p.corazon, ...p.fondo].map(fotoDeNombre).filter(Boolean)).forEach(f => { cuenta[f] = (cuenta[f] || 0) + 1; }));
  const top = Object.entries(cuenta).sort((a, b) => b[1] - a[1]).slice(0, 18).map(x => x[0]);
  $("notaChips").innerHTML = `<button type="button" data-nota="" aria-pressed="true" style="padding-left:16px">Todas</button>` +
    top.map(k => `<button type="button" data-nota="${k}" aria-pressed="false"><img src="fotos/notas/${k}.webp" alt="" loading="lazy">${(NOTAS[k] && NOTAS[k].nombre) || k}</button>`).join("");
  $("notaChips").addEventListener("click", e => {
    const b = e.target.closest("button"); if (!b) return;
    state.nota = b.dataset.nota;
    $("notaChips").querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
    renderGrid(); $("perfumes").scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  });
})();
/* Ir a sección desde el menú */
document.querySelectorAll("[data-ir]").forEach(b => b.addEventListener("click", () => {
  const sec = b.dataset.ir; if (!PERFUMES.some(p => p.seccion === sec)) return;
  state.seccion = sec; try { localStorage.setItem("ag-sec", sec); } catch (e) {}
  renderChips(); renderGrid(); $("perfumes").scrollIntoView({ behavior: "smooth" });
}));
/* Portada: receta de un perfume real del catálogo */
(function portada() {
  const ok = p => disponible(p) && notas3(p).every(n => n.foto);
  const cands = PERFUMES.filter(p => ok(p) && descPct(p) >= 15);
  const p = PERFUMES.find(x => /explorer/.test(x.id) && ok(x)) || cands.find(x => !fotoBlanca(x)) || cands[0] || PERFUMES[0];
  const ns = notas3(p), d = descPct(p);
  const letras = t => [...t].map((c, k) => `<span class="lt"><span style="animation-delay:${(.45 + k * .045).toFixed(2)}s">${c === " " ? "&nbsp;" : c}</span></span>`).join("");
  $("heroEq").innerHTML = `${ns.map(n => n.nombre).join(" + ")} =<b>${letras(p.nombre)}</b>`;
  $("heroCols").innerHTML = ns.map(n => `<div class="col"><img src="fotos/notas/${n.foto}.webp" alt=""><span><small>${n.etapa}</small>${n.nombre}</span></div>`).join("") +
    `<img class="hbt${fotoBlanca(p) ? " blanco" : ""}" src="${p.img}" alt="${p.nombre}" referrerpolicy="no-referrer">` +
    (d ? `<div class="stamp">Ahorro<b>−${d}%</b>vs tienda</div>` : "") +
    `<div class="lbl"><b>${p.nombre} · ${fmt.format(minPrice(p))}</b>${p.marca} · ${p.conc} · ${p.pres[0].ml} ml</div>`;
  $("heroCols").style.cursor = "pointer";
  $("heroCols").addEventListener("click", () => openDrawer(p.id, $("heroCols")));
  $("stTotal").textContent = PERFUMES.length;
  const marcas = [...new Set(PERFUMES.map(x => x.marca))];
  const fila = marcas.map(m => `<span>${m}</span><i>/</i>`).join("");
  $("ticker").innerHTML = fila + fila;
})();
/* Aparecer al hacer scroll */
document.documentElement.classList.add("js-anim");
const srIO = "IntersectionObserver" in window ? new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); srIO.unobserve(e.target); } }), { rootMargin: "0px 0px -5% 0px" }) : null;
function observarSR() { document.querySelectorAll(".sr:not(.in)").forEach((el, k) => { if (!srIO) { el.classList.add("in"); return; } el.style.transitionDelay = (k % 6) * 50 + "ms"; srIO.observe(el); }); }
document.querySelectorAll("#envios, #contacto .wrap > *, footer").forEach(el => el.classList.add("sr"));
new MutationObserver(observarSR).observe($("grid"), { childList: true });
setTimeout(observarSR, 30);
'''
fotos = sorted(f[:-5] for f in os.listdir(os.path.join(RAIZ, "fotos", "notas")) if f.endswith(".webp"))
import json
APOYO = APOYO.replace("%FOTOS%", json.dumps(fotos))
rep("function toast(msg) {", APOYO + "\nfunction toast(msg) {")

# El tema: etiqueta del botón según el modo efectivo (predeterminado oscuro)
rep('function syncThemeLabel() { $("themeLabel").textContent = effectiveTheme() === "dark" ? "Modo claro" : "Modo oscuro"; }',
    'function syncThemeLabel() { $("themeLabel").textContent = effectiveTheme() === "dark" ? "Modo claro" : "Modo oscuro"; const m = document.querySelector(\'meta[name="theme-color"]\'); if (m) m.content = effectiveTheme() === "dark" ? "#0F0F0E" : "#EFEDE7"; }')


# ---------------------------------------------------------------- Test de perfume, guías y enlaces directos
rep('<a href="#envios">Envíos</a></nav>', '<a href="#test" data-test>Test</a><a href="blog/index.html">Guías</a><a href="#envios">Envíos</a></nav>')
rep('<a class="btn ghost" href="#notas">Buscar por nota</a></div>', '<a class="btn ghost" href="#test" data-test>Hacer el test</a></div>')
rep('<div class="notas" id="notas">', """<div class="testband" id="testband"><div><span>¿No sabe qué perfume escoger?</span><b>Haga este test: 6 preguntas, 1 minuto</b></div><button type="button" class="btn" data-test>Empezar el test →</button></div>
  <div class="notas" id="notas">""")
rep('</main>', """<section class="block guias-band" id="guias"><div class="wrap"><div class="block-head"><div><span class="eyebrow">Recetario</span><h2>Guías</h2></div><a class="btn ghost" href="blog/index.html">Ver todas</a></div><div class="guias" id="guiasLista">
  <a href="blog/mejores-fragancias-invierno-2026.html"><span>Temporada</span><b>Las mejores fragancias para invierno 2026</b></a>
  <a href="blog/perfumes-para-regalar-navidad-por-presupuesto.html"><span>Regalos</span><b>Perfumes para regalar esta Navidad, según su presupuesto</b></a>
  <a href="blog/perfumes-que-duran-todo-el-dia.html"><span>Duración</span><b>Perfumes que duran todo el día</b></a>
  <a href="blog/perfumes-de-vainilla-guia.html"><span>Notas</span><b>Vainilla: cómo encontrar la suya</b></a>
</div></div></section>
</main>
<div class="quiz" id="quiz" role="dialog" aria-modal="true" aria-labelledby="qzTitulo" hidden>
  <div class="qz-top"><span class="qz-logo">SCANTALIA · TEST DE PERFUME</span><button type="button" class="qz-x" id="qzCerrar" aria-label="Cerrar el test">✕</button></div>
  <div class="qz-bar"><i id="qzBar"></i></div>
  <div class="qz-body" id="qzBody"></div>
</div>""")

rep("</style>\n</head>", r"""
/* ===== Test de perfume ===== */
.testband { max-width: 1440px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; padding: 18px 32px; border-bottom: 1px solid var(--line); background: var(--accent); color: #fff; }
.testband span { display: block; font-size: 12px; text-transform: uppercase; letter-spacing: .1em; opacity: .85; }
.testband b { font-family: var(--font-display); font-weight: 900; text-transform: uppercase; font-size: clamp(28px, 4vw, 44px); line-height: .95; }
.testband .btn { background: #111 !important; color: #fff !important; border-color: #111 !important; }
.quiz { position: fixed; inset: 0; z-index: 90; background: var(--bg); color: var(--fg); display: flex; flex-direction: column; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
.quiz:not([hidden]) { animation: qzIn .45s cubic-bezier(.16,.8,.2,1); }
@keyframes qzIn { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: none; } }
.qz-top { display: flex; justify-content: space-between; align-items: center; padding: 14px max(16px, env(safe-area-inset-right, 0px)) 14px max(16px, env(safe-area-inset-left, 0px)); border-bottom: 1px solid var(--line); }
.qz-logo { font-size: 12px; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }
.qz-x { width: 44px; height: 44px; border: 1px solid var(--line2); background: transparent; color: var(--fg); font-size: 18px; cursor: pointer; }
.qz-x:hover { background: var(--accent); border-color: var(--accent); color: #fff; }
.qz-bar { height: 4px; background: var(--line); } .qz-bar i { display: block; height: 100%; width: 0; background: var(--accent); transition: width .5s cubic-bezier(.16,.8,.2,1); }
.qz-body { flex: 1; overflow-y: auto; -webkit-overflow-scrolling: touch; padding: 28px max(16px, env(safe-area-inset-right, 0px)) 40px max(16px, env(safe-area-inset-left, 0px)); max-width: 1200px; width: 100%; margin: 0 auto; }
.qz-step { animation: qzStep .5s cubic-bezier(.16,.8,.2,1); }
@keyframes qzStep { from { opacity: 0; transform: translateX(40px); } to { opacity: 1; transform: none; } }
.qz-n { font-size: 12px; text-transform: uppercase; letter-spacing: .1em; color: var(--muted); display: flex; justify-content: space-between; gap: 12px; }
.qz-n button { background: none; border: 0; color: var(--muted); font: inherit; cursor: pointer; text-transform: uppercase; letter-spacing: .1em; }
.qz-n button:hover { color: var(--accent); }
.qz-q { font-family: var(--font-display); font-weight: 900; text-transform: uppercase; font-size: clamp(42px, 7vw, 88px); line-height: .9; margin: 12px 0 8px; text-wrap: balance; }
.qz-sub { font-family: var(--font-type); font-size: 18px; color: var(--muted); margin: 0 0 22px; }
.qz-ops { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 200px), 1fr)); gap: 10px; }
.qz-op { position: relative; display: flex; flex-direction: column; justify-content: flex-end; min-height: 150px; padding: 14px; border: 1px solid var(--line2); background: var(--surface); color: var(--fg); text-align: left; cursor: pointer; overflow: hidden; font: inherit; animation: up .5s cubic-bezier(.16,.8,.2,1) both; transition: border-color .25s, transform .3s; }
.qz-op:nth-child(2) { animation-delay: .05s; } .qz-op:nth-child(3) { animation-delay: .1s; } .qz-op:nth-child(4) { animation-delay: .15s; } .qz-op:nth-child(5) { animation-delay: .2s; } .qz-op:nth-child(6) { animation-delay: .25s; }
.qz-op img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; filter: grayscale(1) brightness(.55); transition: filter .4s, transform .6s; }
.qz-op .lb { position: relative; font-family: var(--font-display); font-weight: 900; text-transform: uppercase; font-size: 30px; line-height: .95; }
.qz-op .ds { position: relative; font-size: 12px; margin-top: 6px; color: var(--muted); }
.qz-op.foto .lb, .qz-op.foto .ds { color: #fff; } .qz-op.foto .ds { opacity: .85; }
.qz-op .big { position: relative; font-family: var(--font-display); font-weight: 900; font-size: 54px; line-height: 1; margin-bottom: 8px; color: var(--accent); }
.qz-op:hover, .qz-op:focus-visible { border-color: var(--accent); transform: translateY(-3px); outline: none; }
.qz-op:hover img, .qz-op:focus-visible img { filter: none; transform: scale(1.05); }
.qz-op.pick { border-color: var(--accent); background: var(--accent); color: #fff; } .qz-op.pick img { filter: none; } .qz-op.pick .ds { color: #fff; }
.qz-mix { min-height: 50vh; display: flex; flex-direction: column; justify-content: center; }
.qz-mix .qz-q { font-family: var(--font-type); font-weight: 400; text-transform: none; font-size: clamp(26px, 4vw, 44px); line-height: 1.2; }
.qz-mix .ings { display: flex; gap: 8px; margin-top: 22px; }
.qz-mix .ings img { width: 84px; height: 84px; object-fit: cover; animation: wipe .7s cubic-bezier(.16,.8,.2,1) both; }
.qz-mix .ings img:nth-child(2) { animation-delay: .35s; } .qz-mix .ings img:nth-child(3) { animation-delay: .7s; }
.qz-res { display: grid; grid-template-columns: 1.1fr .9fr; gap: 0; border: 1px solid var(--line); margin-top: 16px; }
.qz-res .a { padding: 22px; border-right: 1px solid var(--line); position: relative; min-width: 0; }
.qz-res .k { font-size: 12px; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); }
.qz-res h3 { font-family: var(--font-display); font-weight: 900; font-size: clamp(56px, 8vw, 104px); line-height: .85; margin: 10px 0 8px; text-transform: uppercase; }
.qz-res .lm { font-family: var(--font-type); font-size: 18px; margin-bottom: 14px; }
.qz-res ul { list-style: none; padding: 0; margin: 0 0 18px; display: grid; gap: 6px; }
.qz-res li { padding-left: 18px; position: relative; font-size: 14px; } .qz-res li::before { content: "✓"; position: absolute; left: 0; color: var(--accent); }
.qz-res .row { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.qz-res .pr { font-family: var(--font-type); font-size: 32px; margin-right: auto; } .qz-res .pr s { font-size: 15px; color: var(--muted); margin-left: 8px; }
.qz-res .b { background: var(--paper); color: #111; padding: 18px; display: flex; flex-direction: column; justify-content: center; position: relative; min-width: 0; }
.qz-res .b .eqn { height: 210px; }
.qz-pct { position: absolute; right: 18px; top: 16px; width: 104px; height: 104px; border: 3px solid var(--accent); border-radius: 50%; color: var(--accent); display: flex; flex-direction: column; align-items: center; justify-content: center; transform: rotate(-12deg); font-size: 10px; text-transform: uppercase; letter-spacing: .06em; font-weight: 600; animation: stamp .7s cubic-bezier(.2,1.6,.4,1) .3s both; z-index: 2; background: var(--bg); }
.qz-pct b { font-family: var(--font-type); font-size: 30px; line-height: 1; }
.qz-alt { display: grid; grid-template-columns: 1fr 1fr; border: 1px solid var(--line); border-top: 0; }
.qz-alt button { text-align: left; padding: 14px 18px; border: 0; border-right: 1px solid var(--line); background: transparent; color: var(--fg); cursor: pointer; font: inherit; display: grid; grid-template-columns: 1fr auto; gap: 4px 10px; }
.qz-alt button:last-child { border-right: 0; } .qz-alt button:hover { background: var(--surface); }
.qz-alt small { grid-column: 1 / -1; font-size: 11px; text-transform: uppercase; color: var(--muted); }
.qz-alt b { font-family: var(--font-display); font-weight: 900; font-size: 34px; line-height: .95; text-transform: uppercase; }
.qz-alt span { font-family: var(--font-type); font-size: 20px; align-self: end; }
.qz-fin { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 18px; }
.guias { display: grid; grid-template-columns: repeat(4, 1fr); border-top: 1px solid var(--line); }
.guias a { text-decoration: none; padding: 18px 18px 24px; border-right: 1px solid var(--line); border-bottom: 1px solid var(--line); transition: background .3s; }
.guias a:last-child { border-right: 0; } .guias a:hover { background: var(--surface); } .guias a:hover b { color: var(--accent); }
.guias span { display: block; font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); }
.guias b { display: block; font-family: var(--font-display); font-weight: 900; text-transform: uppercase; font-size: 32px; line-height: .95; margin-top: 8px; transition: color .3s; }
@media (max-width: 900px) {
  .testband { padding: 16px; } .testband .btn { width: 100%; justify-content: center; }
  .qz-ops { grid-template-columns: 1fr 1fr; } .qz-op { min-height: 120px; } .qz-op .lb { font-size: 24px; } .qz-op .big { font-size: 40px; }
  .qz-res { grid-template-columns: 1fr; } .qz-res .a { border-right: 0; border-bottom: 1px solid var(--line); }
  .qz-alt { grid-template-columns: 1fr; } .qz-alt button { border-right: 0; border-bottom: 1px solid var(--line); }
  .qz-pct { width: 86px; height: 86px; } .qz-pct b { font-size: 24px; }
  .guias { grid-template-columns: 1fr 1fr; } .guias a:nth-child(2n) { border-right: 0; } .guias b { font-size: 26px; }
}
</style>
</head>""")

QZJS = r"""
/* ===== Test de perfume ===== */
const QZ = [
  { id: "quien", q: "¿Para quién es?", sub: "Empecemos por lo básico.", ops: [
    { lb: "Para mí", ds: "Me gustan los perfumes de mujer", v: "Mujer", big: "Ella" },
    { lb: "Para mí", ds: "Me gustan los perfumes de hombre", v: "Hombre", big: "Él" },
    { lb: "Un regalo", ds: "Para ella", v: "Mujer", big: "🎁" },
    { lb: "Un regalo", ds: "Para él", v: "Hombre", big: "🎁" },
    { lb: "Me da igual", ds: "Que huela bien y ya", v: "", big: "∞" } ] },
  { id: "lugar", q: "Elija su lugar favorito", sub: "Sin pensarlo mucho.", ops: [
    { lb: "Playa al atardecer", ds: "Brisa, sal y sol", foto: "mar", v: "fresco" },
    { lb: "Café en tarde de lluvia", ds: "Algo dulce y caliente", foto: "cacao", v: "dulce" },
    { lb: "Jardín en primavera", ds: "Todo en flor", foto: "peonia", v: "floral" },
    { lb: "Cabaña en el bosque", ds: "Madera y chimenea", foto: "maderas", v: "amaderado" },
    { lb: "Mercado de especias", ds: "Exótico y cálido", foto: "canela", v: "especiado" } ] },
  { id: "postre", q: "¿Qué postre pide?", sub: "Esta dice más de usted de lo que cree.", ops: [
    { lb: "Sorbete de limón", ds: "Ligero y refrescante", foto: "limon", v: "fresco" },
    { lb: "Tarta de frutos rojos", ds: "Jugosa y alegre", foto: "frambuesa", v: "afrutado" },
    { lb: "Crème brûlée", ds: "Vainilla y caramelo", foto: "caramelo", v: "dulce" },
    { lb: "Chocolate con chile", ds: "Intenso y con picor", foto: "pimienta", v: "especiado" },
    { lb: "Solo un espresso", ds: "Sin azúcar, gracias", foto: "haba", v: "amaderado" } ] },
  { id: "momento", q: "¿Cuándo lo va a usar más?", sub: "", ops: [
    { lb: "De día", ds: "Oficina, escuela, diario", v: "dia", big: "☀" },
    { lb: "De noche", ds: "Cenas, citas, fiestas", v: "noche", big: "☾" },
    { lb: "Todo el tiempo", ds: "Uno solo para todo", v: "todo", big: "◐" } ] },
  { id: "fuerza", q: "¿Qué tan notorio lo quiere?", sub: "", ops: [
    { lb: "Discreto", ds: "Que solo lo note quien se acerque", v: 1, big: "·" },
    { lb: "Que se note", ds: "Que pregunten qué perfume es", v: 2, big: "··" },
    { lb: "Inolvidable", ds: "Que se quede en el elevador", v: 3, big: "···" } ] },
  { id: "precio", q: "¿Cuánto quiere invertir?", sub: "Todos son originales y por debajo de tienda departamental.", ops: [
    { lb: "Hasta $1,500", ds: "Gran perfume, gran precio", v: 1500, big: "$" },
    { lb: "$1,500 – $2,500", ds: "Las grandes casas", v: 2500, big: "$$" },
    { lb: "$2,500 – $3,500", ds: "Ediciones intensas", v: 3500, big: "$$$" },
    { lb: "Sin límite", ds: "Lo mejor, incluido el nicho", v: 99999, big: "∞" } ] }
];
const QZ_ESTILO = {
  fresco: /fresc|acuát|acuat|marin|cítric|citric|bergamota|limón|limon|toronja|mandarina|menta|ozón|verde/,
  dulce: /gourmand|vainill|caramel|cacao|chocolate|tonka|pralin|avellana|almendra|miel|tófe|toffee|café|cafe/,
  floral: /floral|rosa|jazm|peon|azahar|neroli|iris|violeta|tuberosa|magnolia|lirio|gardenia|flor/,
  amaderado: /amader|madera|vetiver|cedro|sándalo|sandalo|pachul|musgo|café|cafe|cuero|tabaco/,
  especiado: /especi|canela|pimienta|cardamomo|azafrán|azafran|oud|incienso|ámbar|ambar|clavo|jengibre|nuez moscada/,
  afrutado: /afrutad|frut|cereza|frambuesa|lichi|pera|manzana|mango|durazno|chabacano|ciruela|bayas|maracuy|piña|pina/
};
const QZ_TXT = { fresco: "frescas y luminosas", dulce: "dulces y cremosas", floral: "florales", amaderado: "amaderadas", especiado: "cálidas y especiadas", afrutado: "afrutadas" };
let qzR = {}, qzI = 0;
function qzTexto(p) { return [p.familia, ...(p.acordes || []).map(a => a[0]), ...p.salida, ...p.corazon, ...p.fondo].join(" ").toLowerCase(); }
function qzCalcular() {
  const ests = [qzR.lugar, qzR.postre];
  const res = PERFUMES.filter(disponible).filter(p => !qzR.quien || p.seccion === qzR.quien || p.seccion === "Unisex").map(p => {
    const t = qzTexto(p), why = [];
    let sc = 0;
    ests.forEach((e, i) => { if (QZ_ESTILO[e].test(t)) { sc += i ? 2 : 3; why.push(e); } });
    const oc = (p.ocasion || "").toLowerCase();
    if (qzR.momento === "dia" && /día|dia|oficina/.test(oc)) sc += 1.5;
    if (qzR.momento === "noche" && /noche|citas|evento/.test(oc)) sc += 1.5;
    if (qzR.momento === "todo" && (/día · noche|todo/.test(oc) || p.temporada === "Todo el año")) sc += 1.5;
    const dur = parseInt((p.duracion || "0").split(/[–-]/)[0], 10) || 5;
    const nivel = dur >= 9 || /parfum|elixir/i.test(p.conc + p.nombre) ? 3 : dur >= 7 ? 2 : 1;
    sc += nivel === qzR.fuerza ? 1.5 : Math.abs(nivel - qzR.fuerza) === 1 ? .5 : -.5;
    const pr = minPrice(p);
    sc += pr <= qzR.precio ? 2 : pr <= qzR.precio * 1.15 ? 0 : -5;
    if (/invierno/i.test(p.temporada || "") || p.temporada === "Todo el año") sc += .4;
    if (p.antes && p.antes > pr) sc += .3;
    if (!qzR.quien && p.seccion === "Unisex") sc += .3;
    return { p, sc, why: [...new Set(why)] };
  }).sort((a, b) => b.sc - a.sc);
  return res;
}
function qzRazones(r) {
  const out = [];
  if (r.why.length) out.push(`Tiene notas ${r.why.map(w => QZ_TXT[w]).join(" y ")}, como lo que eligió.`);
  out.push(`${r.p.familia}: ${[r.p.salida[0], r.p.corazon[0], r.p.fondo[0]].filter(Boolean).join(", ").toLowerCase()}.`);
  out.push(`Dura ${r.p.duracion} y va bien ${(r.p.ocasion || "").toLowerCase().replace(" · ", " y ")}.`);
  if (descPct(r.p)) out.push(`Está ${descPct(r.p)}% abajo del precio de tienda departamental.`);
  return out;
}
function qzPaso() {
  const b = $("qzBody"), Q = QZ[qzI];
  $("qzBar").style.width = (qzI / QZ.length * 100) + "%";
  b.innerHTML = `<div class="qz-step"><div class="qz-n"><span>Pregunta ${qzI + 1} de ${QZ.length}</span>${qzI ? '<button type="button" id="qzAtras">← Anterior</button>' : ""}</div>
    <h2 class="qz-q" id="qzTitulo">${Q.q}</h2>${Q.sub ? `<p class="qz-sub">${Q.sub}</p>` : ""}
    <div class="qz-ops">${Q.ops.map((o, k) => `<button type="button" class="qz-op${o.foto ? " foto" : ""}" data-k="${k}">${o.foto ? `<img src="fotos/notas/${o.foto}.webp" alt="">` : ""}${o.big ? `<span class="big">${o.big}</span>` : ""}<span class="lb">${o.lb}</span><span class="ds">${o.ds}</span></button>`).join("")}</div></div>`;
  b.scrollTop = 0;
  const at = $("qzAtras"); if (at) at.onclick = () => { qzI--; qzPaso(); };
  b.querySelectorAll(".qz-op").forEach(el => el.onclick = () => {
    el.classList.add("pick"); qzR[Q.id] = Q.ops[+el.dataset.k].v;
    setTimeout(() => { qzI++; qzI < QZ.length ? qzPaso() : qzMezclar(); }, 380);
  });
  const f = b.querySelector(".qz-op"); if (f && matchMedia("(hover: hover)").matches) f.focus({ preventScroll: true });
}
function qzMezclar() {
  $("qzBar").style.width = "100%";
  const top = qzCalcular();
  if (!top.length) { $("qzBody").innerHTML = `<div class="qz-step qz-mix"><h2 class="qz-q">No encontramos uno con todo eso.</h2><div class="qz-fin"><button class="btn" type="button" id="qzOtra">Repetir el test</button></div></div>`; $("qzOtra").onclick = qzEmpezar; return; }
  const ns = notas3(top[0].p).filter(n => n.foto);
  $("qzBody").innerHTML = `<div class="qz-step qz-mix"><div class="qz-n"><span>Mezclando su receta</span></div><h2 class="qz-q" id="qzTitulo"><span id="qzTipeo"></span><span class="cur"></span></h2><div class="ings">${ns.map(n => `<img src="fotos/notas/${n.foto}.webp" alt="">`).join("")}</div></div>`;
  const frase = `${ns.map(n => n.nombre).join(" + ") || "Sus respuestas"} = …`;
  let i = 0; const tip = setInterval(() => { const el = $("qzTipeo"); if (!el) { clearInterval(tip); return; } el.textContent = frase.slice(0, ++i); if (i >= frase.length) clearInterval(tip); }, 38);
  setTimeout(() => qzResultado(top), Math.min(2600, 900 + frase.length * 38));
}
function qzResultado(top) {
  const r = top[0], p = r.p, d = descPct(p), max = top[0].sc || 1;
  const pct = s => Math.max(72, Math.min(98, Math.round(74 + 24 * s / Math.max(max, 1))));
  const ns = notas3(p);
  $("qzBody").innerHTML = `<div class="qz-step"><div class="qz-n"><span>Su receta ideal</span><button type="button" id="qzOtra2">Repetir el test ↺</button></div>
    <div class="qz-res"><div class="a"><span class="qz-pct"><b>${pct(r.sc)}%</b>compatible</span><span class="k">${p.marca} · ${p.conc} · ${p.pres.map(x => x.ml + " ml").join(" / ")}</span><h3 id="qzTitulo">${p.nombre}</h3><div class="lm">“${p.lema}”</div>
      <ul>${qzRazones(r).map(x => `<li>${x}</li>`).join("")}</ul>
      <div class="row"><span class="pr">${fmt.format(minPrice(p))}${d ? `<s>${fmt.format(p.antes)}</s>` : ""}</span><button type="button" class="btn" id="qzAdd">+ Agregar a la bolsa</button><button type="button" class="btn ghost" data-ficha="${p.id}">Ver ficha</button></div></div>
      <div class="b"><div class="eqn">${ns.map(n => `<div class="ph">${n.foto ? `<img src="fotos/notas/${n.foto}.webp" alt="">` : `<div style="background:${n.color};width:100%;height:100%"></div>`}<span>${n.etapa}<b>${n.nombre}</b></span></div>`).join("")}<div class="eqb"><i>=</i>${p.img ? `<img src="${p.img}" alt="" referrerpolicy="no-referrer">` : ""}</div></div></div></div>
    <div class="qz-alt">${top.slice(1, 3).map(x => `<button type="button" data-ficha="${x.p.id}"><small>También le puede gustar · ${pct(x.sc)}% · ${x.p.marca}</small><b>${x.p.nombre}</b><span>${fmt.format(minPrice(x.p))}</span></button>`).join("")}</div>
    <div class="qz-fin"><button type="button" class="btn ghost" id="qzOtra">Repetir el test</button><button type="button" class="btn ghost" id="qzTienda">Ver toda la tienda</button></div></div>`;
  $("qzAdd").onclick = e => { addToCart(p.id, p.pres[0].ml); gustoSumar(p.id, 3); e.currentTarget.textContent = "✓ En su bolsa"; };
  $("qzBody").querySelectorAll("[data-ficha]").forEach(b => b.onclick = () => { qzCerrar(); openDrawer(b.dataset.ficha, b); });
  $("qzOtra").onclick = $("qzOtra2").onclick = qzEmpezar;
  $("qzTienda").onclick = () => { qzCerrar(); $("perfumes").scrollIntoView(); };
  gustoSumar(p.id, 1);
}
let qzPrevio = null;
function qzEmpezar() { qzR = {}; qzI = 0; qzPaso(); }
function qzAbrir() { qzPrevio = document.activeElement; $("quiz").hidden = false; document.body.style.overflow = "hidden"; qzEmpezar(); }
function qzCerrar() { $("quiz").hidden = true; document.body.style.overflow = ""; if (location.hash === "#test") history.replaceState(null, "", location.pathname); if (qzPrevio && qzPrevio.focus) qzPrevio.focus({ preventScroll: true }); }
document.querySelectorAll("[data-test]").forEach(b => b.addEventListener("click", e => { e.preventDefault(); qzAbrir(); }));
$("qzCerrar").addEventListener("click", qzCerrar);
document.addEventListener("keydown", e => { if (e.key === "Escape" && !$("quiz").hidden) qzCerrar(); });
/* Enlaces directos: #test abre el test; #perfume-ID abre la ficha (usado por las guías) */
function porHash() {
  const h = decodeURIComponent(location.hash || "");
  if (h === "#test") { qzAbrir(); return; }
  if (h.startsWith("#perfume-")) {
    const p = PERFUMES.find(x => x.id === h.slice(9));
    if (p) { if (state.seccion !== p.seccion) { state.seccion = p.seccion; renderChips(); renderGrid(); } setTimeout(() => openDrawer(p.id, null), 200); }
  }
}
window.addEventListener("hashchange", porHash);
setTimeout(porHash, 60);
"""
rep("function toast(msg) {", QZJS + "\nfunction toast(msg) {")

open(os.path.join(RAIZ, "prueba.html"), "w", encoding="utf-8").write(s)
print("prueba.html lista (Mostrador de recetas)")
