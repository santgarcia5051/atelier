#!/usr/bin/env python3
"""Construye el blog (carpeta blog/): índice y artículos con el diseño del Mostrador de recetas.
Cada perfume citado se muestra con su ficha viva (precio, descuento, disponibilidad y notas) leída de perfumes.js,
y un botón que lleva a su ficha en la tienda para comprarlo.

Para agregar un artículo: añada un dict a ARTICULOS. En el texto, [[id-del-perfume]] inserta la ficha de compra.
Uso: python3 scripts/construir_blog.py
"""
import html, json, os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIENDA = "../index.html"
SITIO = "https://santgarcia5051.github.io/atelier"

ARTICULOS = [
{
 "slug": "mejores-fragancias-invierno-2026",
 "titulo": "Las mejores fragancias para invierno 2026",
 "corto": "Invierno 2026",
 "desc": "Vainilla, ámbar, cuero y especias: los perfumes que mejor funcionan con el frío, para ella, para él y para compartir.",
 "fecha": "6 de noviembre de 2026", "lectura": "6 min",
 "portada": ["vainilla", "ambar", "cuero"],
 "cuerpo": """
<p class="entrada">Con el frío, el perfume se comporta distinto. La piel está más fría, el aire más seco y las notas ligeras se apagan en un par de horas. Por eso en invierno ganan las fragancias con fondo: vainilla, ámbar, maderas, cuero y especias, que se quedan cerca de la piel y se sienten como una bufanda.</p>
<p>Elegimos las que mejor funcionan esta temporada, todas originales y disponibles en nuestra tienda.</p>

<h2>Para ella</h2>
<h3>Devotion Intense, Dolce &amp; Gabbana</h3>
<p>La versión más profunda de Devotion. Abre con avellana, pasa a flor de azahar y se asienta en una vainilla cremosa que dura toda la noche. Es dulce sin empalagar y huele a postre caro. Ideal para cenas y para quien quiere que le pregunten qué perfume trae.</p>
[[devotion-intense]]
<h3>Very Good Girl Elixir, Carolina Herrera</h3>
<p>Cereza negra, rosa y vainilla en concentración parfum. Es de las que más duran del catálogo, entre 9 y 11 horas, y tiene ese carácter seductor de la línea Good Girl, pero más oscuro y más invernal.</p>
[[carolina-herrera-very-good-girl-elixir-parfum-mujer]]
<h3>La Belle, Jean Paul Gaultier</h3>
<p>Pera jugosa al inicio, vetiver en el corazón y vainilla de fondo. Ese contraste entre lo fresco y lo cálido la hace muy versátil: funciona de día con suéter y de noche con abrigo.</p>
[[jean-paul-gaultier-la-belle-edp-mujer]]
<h3>Shalimar, Guerlain</h3>
<p>Un clásico desde 1925 que sigue sin pasar de moda. Bergamota, iris y una vainilla ahumada y empolvada que es la firma de la casa. Si busca algo elegante y con historia, es esta.</p>
[[shalimar]]

<h2>Para él</h2>
<h3>Eros Eau de Parfum, Versace</h3>
<p>Menta fresca arriba, haba tonka y vainilla de Madagascar abajo. Es intenso, se nota al entrar a un lugar y es de los más pedidos para salir de noche.</p>
[[versace-eros-edp-hombre]]
<h3>Bad Boy Cobalt Elixir, Carolina Herrera</h3>
<p>Pimienta negra, trufa y vainilla con incienso. Más oscuro y más duradero que el Bad Boy original, con un frasco que ya es una declaración.</p>
[[carolina-herrera-bad-boy-cobalt-elixir-parfum-hombre]]
<h3>L'Homme Idéal L'Intense, Guerlain</h3>
<p>Chile, rosa de Damasco y cuero. Suena atrevido y lo es, pero en la piel se vuelve suave y muy elegante. Para eventos formales y noches largas.</p>
[[homme-ideal-intense]]
<h3>Legend Red, Montblanc</h3>
<p>Naranja sanguina, cedro y haba tonka. Es la opción más fácil de llevar de esta lista: cálida, limpia y segura para la oficina en temporada de frío.</p>
[[legend-red]]

<h2>Para compartir</h2>
<h3>Side Effect, Initio</h3>
<p>Canela, tabaco y sándalo. Un perfume de nicho que huele a chimenea encendida y a whisky. No es para todos los días, pero es de esos que la gente recuerda.</p>
[[initio-side-effect-edp-unisex]]

<h2>Cómo hacer que dure más con el frío</h2>
<ul>
<li>Aplíquelo después de bañarse, con la piel aún un poco húmeda o recién hidratada.</li>
<li>Muñecas, cuello y detrás de las orejas. No frote las muñecas: rompe las notas de salida.</li>
<li>Un toque en la bufanda o en el abrigo hace que el aroma dure mucho más.</li>
</ul>
<p>Recuerde que en la compra de dos perfumes el envío es gratis a todo México.</p>
"""},
{
 "slug": "perfumes-para-regalar-navidad-por-presupuesto",
 "titulo": "Perfumes para regalar esta Navidad, según su presupuesto",
 "corto": "Regalos de Navidad",
 "desc": "Ideas de perfumes originales para regalar en tres rangos de precio, con opciones para ella, para él y para quien todavía no conoce bien.",
 "fecha": "6 de noviembre de 2026", "lectura": "5 min",
 "portada": ["canela", "mandarina", "vainilla"],
 "cuerpo": """
<p class="entrada">Un perfume es de los regalos que más se agradecen, siempre que se acierte. La clave es pensar en la persona: si es de aromas frescos o dulces, si lo usará de día o de noche, y cuánto quiere gastar usted. Armamos esta guía en tres presupuestos para que acierte sin pagar precio de tienda departamental.</p>

<h2>Menos de $1,500</h2>
<h3>Asad, Lattafa</h3>
<p>Pimienta negra, pachulí y vainilla. Un perfume árabe con mucha presencia y duración por un precio muy accesible. Para él, y para quien le gustan los aromas cálidos.</p>
[[lattafa-asad-edp-hombre]]
<h3>Boss Alive, Hugo Boss</h3>
<p>Vainilla de Madagascar, jazmín sambac y maderas suaves. Femenino, cálido y fácil de llevar todos los días: un regalo seguro.</p>
[[hugo-boss-boss-alive-edp-mujer]]
<h3>The Most Wanted Intense, Azzaro</h3>
<p>Cardamomo, toffee y amberwood. Dulce, especiado y muy de noche. De los que más rinden por su precio.</p>
[[azzaro-the-most-wanted-intense-edp-hombre]]

<h2>De $1,500 a $2,500</h2>
<h3>Q Parfum, Dolce &amp; Gabbana</h3>
<p>Cereza, jazmín sambac y vainilla en concentración parfum. Dura todo el día y el frasco con la corona luce mucho envuelto para regalo.</p>
[[dolce-gabbana-q-parfum-mujer]]
<h3>Scandal Pour Homme, Jean Paul Gaultier</h3>
<p>Esclarea, caramelo y vetiver. Dulce pero masculino, con un frasco que siempre da de qué hablar.</p>
[[jean-paul-gaultier-scandal-pour-homme-edt-hombre]]
<h3>Dylan Blue, Versace</h3>
<p>Notas acuáticas, violeta y almizcle. Fresco y limpio, perfecto para quien prefiere algo discreto o lo usará en la oficina.</p>
[[versace-dylan-blue-edt-hombre]]

<h2>Más de $2,500</h2>
<h3>La Belle, Jean Paul Gaultier</h3>
<p>Pera, vetiver y vainilla en el icónico frasco de torso. Un regalo que se nota desde la caja.</p>
[[jean-paul-gaultier-la-belle-edp-mujer]]
<h3>Perseus, Parfums de Marly</h3>
<p>Toronja, vetiver y maderas secas. Perfumería de nicho francesa: para alguien que ya tiene de todo y aprecia lo distinto.</p>
[[parfums-de-marly-perseus-edp-hombre]]

<h2>¿No sabe qué le gusta?</h2>
<p>Si no está seguro de los gustos de la persona, elija algo versátil y de concentración Eau de Parfum: funciona de día y de noche. O haga nuestro test de dos minutos pensando en ella o en él y le sugerimos tres opciones.</p>
<p><a class="cta-link" href="TIENDA#test">Hacer el test de perfume →</a></p>
"""},
{
 "slug": "perfumes-que-duran-todo-el-dia",
 "titulo": "Perfumes que duran todo el día: de 9 a 11 horas en la piel",
 "corto": "Larga duración",
 "desc": "Las fragancias con mayor duración de nuestro catálogo y por qué la concentración importa más de lo que parece.",
 "fecha": "6 de noviembre de 2026", "lectura": "5 min",
 "portada": ["ambar", "maderas", "oud"],
 "cuerpo": """
<p class="entrada">Que un perfume dure depende de tres cosas: su concentración, sus notas de fondo y su piel. Las versiones Parfum y Elixir tienen más esencia que un Eau de Toilette, y las notas como ámbar, sándalo, vainilla u oud se evaporan mucho más lento que los cítricos.</p>
<p>Estas son las fragancias de nuestro catálogo que mejor aguantan una jornada completa, entre 9 y 11 horas.</p>

<h2>Para él</h2>
<h3>Phantom Elixir, Paco Rabanne</h3>
<p>Notas marinas, minerales y vaina de vainilla. Fresco al inicio y cremoso al final, con una estela que dura hasta la noche.</p>
[[paco-rabanne-phantom-elixir-parfum-hombre]]
<h3>Invictus Victory Absolu, Paco Rabanne</h3>
<p>Pimienta negra, ámbar y sándalo. La versión más intensa de Invictus: profunda, cálida y muy duradera.</p>
[[paco-rabanne-invictus-victory-absolu-parfum-hombre]]
<h3>1 Million Gold Elixir, Paco Rabanne</h3>
<p>Mandarina amarilla, sándalo y vainilla. Dorado como su frasco, dulce y luminoso.</p>
[[paco-rabanne-1-million-gold-elixir-parfum-hombre]]
<h3>Luna Rossa Ocean Le Parfum, Prada</h3>
<p>Limón, azafrán y ámbar. Para quien quiere algo fresco que no desaparezca a media mañana.</p>
[[prada-luna-rossa-ocean-le-parfum-parfum-hombre]]

<h2>Para ella</h2>
<h3>Good Fortune Elixir Intense, Viktor &amp; Rolf</h3>
<p>Incienso, jazmín y vainilla Bourbon. Envolvente y misterioso, de los que se quedan en la ropa al día siguiente.</p>
[[viktor-rolf-good-fortune-elixir-intense-parfum-mujer]]
<h3>Scandal Le Parfum Intense, Jean Paul Gaultier</h3>
<p>Jazmín, caramelo y vainilla. Dulce, femenino y con muchísima presencia.</p>
[[jean-paul-gaultier-scandal-le-parfum-intense-parfum-mujer]]

<h2>Nicho</h2>
<h3>Favonius, Nishane</h3>
<p>Lichi, rosa y oud. Perfumería turca de nicho en concentración extrait, para quien busca algo que nadie más en la oficina trae puesto.</p>
[[nishane-favonius-parfum-unisex]]

<h2>Tres trucos para que dure más</h2>
<ul>
<li>Hidrate la piel antes: el perfume se adhiere mejor a la piel hidratada.</li>
<li>Guárdelo lejos del sol y del baño; el calor y la humedad lo degradan.</li>
<li>Aplique en zonas de pulso y un poco en la ropa, que retiene el aroma por más tiempo.</li>
</ul>
"""},
{
 "slug": "perfumes-de-vainilla-guia",
 "titulo": "Vainilla: cómo encontrar el perfume de vainilla perfecto para usted",
 "corto": "Guía de vainilla",
 "desc": "No todas las vainillas huelen igual. Le explicamos las diferencias y le recomendamos una para cada estilo.",
 "fecha": "6 de noviembre de 2026", "lectura": "5 min",
 "portada": ["vainilla", "caramelo", "cacao"],
 "cuerpo": """
<p class="entrada">La vainilla es la nota más querida de la perfumería, pero no es una sola. Puede ser fresca y luminosa, cremosa como un postre, ahumada como un clásico o tostada como un café. Lo que la acompaña decide su carácter.</p>

<h2>Vainilla luminosa</h2>
<h3>Devotion, Dolce &amp; Gabbana</h3>
<p>Limón confitado y flor de azahar alrededor de la vainilla. Es dulce pero limpia, perfecta para el día.</p>
[[dolce-gabbana-devotion-edp-mujer]]

<h2>Vainilla con fruta</h2>
<h3>La Belle, Jean Paul Gaultier</h3>
<p>La pera le da frescura y el vetiver un toque terroso. Una vainilla moderna y fácil de llevar.</p>
[[jean-paul-gaultier-la-belle-edp-mujer]]

<h2>Vainilla especiada</h2>
<h3>Scandal Intense, Jean Paul Gaultier</h3>
<p>Cardamomo e ylang-ylang con absoluto de vainilla. Más adulta, más cálida, ideal para la noche.</p>
[[jean-paul-gaultier-scandal-intense-edp-mujer]]

<h2>Vainilla fresca para él</h2>
<h3>Eros Eau de Parfum, Versace</h3>
<p>La menta y la vainilla de Madagascar hacen un contraste que engancha. Dulce, pero con energía.</p>
[[versace-eros-edp-hombre]]
<h3>Phantom Elixir, Paco Rabanne</h3>
<p>Una vainilla marina y mineral, diferente a todas. Fresca al inicio y cremosa al final.</p>
[[paco-rabanne-phantom-elixir-parfum-hombre]]

<h2>Vainilla con gamuza y té</h2>
<h3>Al Areeq Gold, Lattafa</h3>
<p>Té negro, gamuza y vainilla. Suave, sofisticada y para cualquiera. Una joya por su precio.</p>
[[lattafa-al-areeq-gold-edp-unisex]]
<h3>Ishq Al Shuyukh Gold, Lattafa</h3>
<p>Caramelo, gamuza y vainilla. Para quien quiere la vainilla más golosa posible.</p>
[[lattafa-ishq-al-shuyukh-gold-edp-unisex]]

<p>¿Quiere ver todas las fragancias con vainilla? En la tienda puede filtrar por nota en la barra "Mi receta lleva…".</p>
<p><a class="cta-link" href="TIENDA#notas">Buscar perfumes por nota →</a></p>
"""},
]

CSS = r"""
:root, :root[data-theme="dark"] { --bg:#0F0F0E; --surface:#171715; --fg:#ECE9E2; --muted:#9C988F; --line:#2A2926; --accent:#C9A35E; --accent-fg:#111110; --paper:#ECE9E2; --dim:#4A4843; color-scheme:dark;
  --display:"Big Shoulders Display", Impact, "Arial Narrow", sans-serif; --body:"IBM Plex Mono", ui-monospace, Menlo, monospace; --type:"Courier Prime", "Courier New", monospace; }
:root[data-theme="light"] { --bg:#EFEDE7; --surface:#F8F6F1; --fg:#141413; --muted:#6E6B64; --line:#141413; --accent:#8C6A2E; --accent-fg:#FFFFFF; --paper:#F8F6F1; --dim:#B5B0A6; color-scheme:light; }
* { box-sizing:border-box; margin:0; padding:0; }
html { -webkit-text-size-adjust:100%; }
body { background:var(--bg); color:var(--fg); font-family:var(--body); font-size:15px; line-height:1.75; -webkit-font-smoothing:antialiased; }
img { display:block; max-width:100%; }
a { color:inherit; }
.top { position:sticky; top:env(safe-area-inset-top,0px); z-index:20; background:color-mix(in srgb, var(--bg) 92%, transparent); backdrop-filter:blur(12px); border-bottom:1px solid var(--line); }
.top-in { max-width:1200px; margin:0 auto; display:flex; align-items:center; justify-content:space-between; gap:14px; padding:12px max(16px, env(safe-area-inset-right,0px)) 12px max(16px, env(safe-area-inset-left,0px)); }
.logo { font-family:var(--display); font-weight:900; font-size:28px; letter-spacing:.04em; text-decoration:none; }
.top nav { display:flex; gap:20px; font-size:12px; text-transform:uppercase; letter-spacing:.08em; }
.top nav a { text-decoration:none; }
.top nav a:hover { color:var(--accent); }
.wrap { max-width:1200px; margin:0 auto; padding-left:max(16px, env(safe-area-inset-left,0px)); padding-right:max(16px, env(safe-area-inset-right,0px)); }
.k { font-size:12px; text-transform:uppercase; letter-spacing:.1em; color:var(--muted); }
h1 { font-family:var(--display); font-weight:900; text-transform:uppercase; font-size:clamp(46px, 9vw, 112px); line-height:.86; letter-spacing:-.005em; margin:14px 0 18px; text-wrap:balance; }
.lead { font-family:var(--type); font-size:clamp(17px, 2vw, 21px); line-height:1.45; max-width:62ch; }
.strip { display:grid; grid-template-columns:repeat(3,1fr); height:clamp(160px, 28vw, 300px); margin:28px 0 0; border:1px solid var(--line); }
.strip div { position:relative; overflow:hidden; border-right:1px solid var(--line); }
.strip div:last-child { border-right:0; }
.strip img { width:100%; height:100%; object-fit:cover; animation:wipe 1.87s cubic-bezier(.16,.8,.2,1) both; }
.strip div:nth-child(2) img { animation-delay:0.26s; } .strip div:nth-child(3) img { animation-delay:0.51s; }
.strip span { position:absolute; left:10px; bottom:10px; background:var(--paper); color:#111; font-size:11px; text-transform:uppercase; padding:4px 7px; }
.meta { display:flex; gap:18px; flex-wrap:wrap; font-size:12px; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); border-top:1px solid var(--line); border-bottom:1px solid var(--line); padding:12px 0; margin-top:28px; }
article.post { max-width:760px; margin:0 auto; padding:36px 0 40px; }
article.post p { margin:0 0 18px; }
article.post p.entrada { font-family:var(--type); font-size:20px; line-height:1.5; }
article.post h2 { font-family:var(--display); font-weight:900; text-transform:uppercase; font-size:clamp(36px, 6vw, 56px); line-height:.95; margin:44px 0 16px; padding-top:18px; border-top:1px solid var(--line); }
article.post h3 { font-family:var(--type); font-size:23px; font-weight:700; margin:26px 0 8px; }
article.post ul { margin:0 0 18px 20px; } article.post li { margin-bottom:6px; }
.cta-link { display:inline-block; background:var(--fg); color:var(--bg); text-decoration:none; padding:14px 18px; font-size:12px; text-transform:uppercase; letter-spacing:.1em; font-weight:600; }
.cta-link:hover { background:var(--accent); color:var(--accent-fg); }
.pz { display:grid; grid-template-columns:120px 1fr auto; gap:0; border:1px solid var(--line); margin:12px 0 26px; background:var(--surface); text-decoration:none; transition:border-color 0.51s, transform 0.68s cubic-bezier(.16,.8,.2,1); }
.pz:hover { border-color:var(--accent); transform:translateY(-3px); }
.pz .fr { background:var(--paper); display:flex; align-items:center; justify-content:center; padding:10px; }
.pz .fr img { max-height:130px; object-fit:contain; mix-blend-mode:multiply; }
.pz .tx { padding:14px 16px; min-width:0; }
.pz .tx small { display:block; font-size:11px; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); }
.pz .tx b { display:block; font-family:var(--display); font-weight:900; text-transform:uppercase; font-size:34px; line-height:.95; margin:4px 0 8px; }
.pz .mn { display:flex; gap:4px; align-items:center; flex-wrap:wrap; }
.pz .mn img, .pz .mn i { width:30px; height:30px; object-fit:cover; display:block; }
.pz .mn em { font-style:normal; font-size:11px; text-transform:uppercase; color:var(--muted); margin-left:6px; }
.pz .cp { padding:14px 16px; display:flex; flex-direction:column; justify-content:space-between; align-items:flex-end; gap:10px; border-left:1px solid var(--line); min-width:160px; }
.pz .pr { font-family:var(--type); font-size:26px; line-height:1; text-align:right; }
.pz .pr s { display:block; font-size:13px; color:var(--muted); margin-top:4px; }
.pz .ds { color:var(--accent); border:1.5px solid var(--accent); padding:2px 7px; font-size:12px; font-weight:600; transform:rotate(-3deg); }
.pz .go { background:var(--fg); color:var(--bg); padding:11px 14px; font-size:11px; text-transform:uppercase; letter-spacing:.1em; font-weight:600; white-space:nowrap; }
.pz:hover .go { background:var(--accent); color:var(--accent-fg); }
.pz.off { opacity:.6; }
.lista { display:grid; grid-template-columns:repeat(2, 1fr); border-top:1px solid var(--line); margin-top:30px; }
.lista a { display:grid; grid-template-rows:auto auto 1fr; text-decoration:none; border-right:1px solid var(--line); border-bottom:1px solid var(--line); padding:0 0 22px; transition:background 0.51s; }
.lista a:nth-child(2n) { border-right:0; }
.lista a:hover { background:var(--surface); }
.lista a:hover h2 { color:var(--accent); }
.lista .im { display:grid; grid-template-columns:repeat(3,1fr); height:170px; }
.lista .im img { width:100%; height:100%; object-fit:cover; filter:grayscale(1); transition:filter 0.85s; }
.lista a:hover .im img { filter:none; }
.lista .k { padding:16px 20px 0; }
.lista h2 { font-family:var(--display); font-weight:900; text-transform:uppercase; font-size:clamp(32px, 4vw, 46px); line-height:.95; padding:8px 20px 8px; transition:color 0.51s; }
.lista p { padding:0 20px; color:var(--muted); font-size:14px; }
.mas { border-top:1px solid var(--line); padding:30px 0 10px; }
.mas h2 { font-family:var(--display); font-weight:900; text-transform:uppercase; font-size:40px; margin-bottom:12px; }
.mas .ls { display:flex; flex-direction:column; }
.mas .ls a { display:flex; justify-content:space-between; gap:12px; text-decoration:none; padding:14px 0; border-bottom:1px solid var(--line); font-family:var(--type); font-size:20px; }
.mas .ls a:hover { color:var(--accent); }
.testban { display:flex; align-items:center; justify-content:space-between; gap:18px; flex-wrap:wrap; background:var(--paper); color:#111; padding:22px 24px; margin:36px 0; box-shadow:8px 8px 0 var(--accent); }
.testban b { font-family:var(--display); font-weight:900; text-transform:uppercase; font-size:clamp(30px, 5vw, 44px); line-height:.95; display:block; }
.testban a { background:#111; color:#fff; text-decoration:none; padding:14px 18px; font-size:12px; text-transform:uppercase; letter-spacing:.1em; font-weight:600; }
footer { border-top:1px solid var(--line); padding:26px 0 40px; font-size:12px; color:var(--muted); }
footer .wrap { display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px; }
@keyframes wipe { from { clip-path:inset(0 100% 0 0); } to { clip-path:inset(0 0 0 0); } }
@keyframes up { from { opacity:0; transform:translateY(24px); } to { opacity:1; transform:none; } }
.u { animation:up 1.53s cubic-bezier(.16,.8,.2,1) both; } .u2 { animation-delay:0.17s; } .u3 { animation-delay:0.34s; }
@media (max-width:720px) {
  .top nav a:not(.keep) { display:none; }
  .pz { grid-template-columns:92px 1fr; }
  .pz .cp { grid-column:1 / -1; flex-direction:row; align-items:center; border-left:0; border-top:1px solid var(--line); min-width:0; }
  .pz .pr { text-align:left; } .pz .pr s { display:inline; margin-left:6px; }
  .pz .tx b { font-size:28px; }
  .lista { grid-template-columns:1fr; } .lista a { border-right:0; }
  article.post p.entrada { font-size:18px; }
}
@media (prefers-reduced-motion:reduce) { *, *::before, *::after { animation:none !important; transition:none !important; } }
"""

JS = r"""
(function () {
  try { var t = localStorage.getItem("ag-theme"); document.documentElement.setAttribute("data-theme", t === "light" ? "light" : "dark"); } catch (e) {}
  var fmt = new Intl.NumberFormat("es-MX", { style: "currency", currency: "MXN", maximumFractionDigits: 0 });
  var FOTOS = new Set(%FOTOS%);
  var ALIAS = { sandalo: "maderas", cedro: "maderas", azahar: "neroli", musgo: "vetiver", almizcle: "ambar", incienso: "oud" };
  function foto(k) { return FOTOS.has(k) ? k : (ALIAS[k] && FOTOS.has(ALIAS[k]) ? ALIAS[k] : null); }
  var NF = [["notas marinas","mar"],["marin","mar"],["acuat","mar"],["azahar","neroli"],["tonka","haba"],["sandalo","maderas"],["cedro","maderas"],["madera","maderas"],["amaderad","maderas"],["almizcle","ambar"],["ambar","ambar"],["chocolate","cacao"],["naranja","mandarina"],["lima","limon"],["citric","limon"],["higo","maderas"],["incienso","oud"],["cachemira","maderas"],["praline","caramelo"],["tofe","caramelo"]];
  function fotoNombre(n) { var t = (n || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); var r = null;
    FOTOS.forEach(function (k) { if (!r && t.indexOf(k) >= 0) r = k; }); if (r) return r;
    for (var i = 0; i < NF.length; i++) if (t.indexOf(NF[i][0]) >= 0 && FOTOS.has(NF[i][1])) return NF[i][1]; return null; }
  function disp(p) { return p.disponible !== false; }
  document.querySelectorAll("[data-perfume]").forEach(function (el) {
    var CAT = typeof PERFUMES !== "undefined" ? PERFUMES : [], NT = typeof NOTAS !== "undefined" ? NOTAS : {};
    var p = CAT.find(function (x) { return x.id === el.dataset.perfume; });
    if (!p) { el.remove(); return; }
    var pr = p.pres[0], d = disp(p) && p.antes && p.pres.length === 1 && p.antes > pr.precio ? Math.round((1 - pr.precio / p.antes) * 100) : 0;
    var ns = [p.salida[0], p.corazon[0], p.fondo[0]].map(function (nom, i) { var k = (p.destacadas || [])[i], n = NT[k] || {}; return { f: nom ? fotoNombre(nom) : foto(k), n: nom || n.nombre || k, c: n.color || "#6E6B64" }; }).filter(function (x) { return x.n; });
    el.className = "pz" + (disp(p) ? "" : " off");
    el.href = el.getAttribute("href");
    el.innerHTML = '<span class="fr">' + (p.img ? '<img src="' + (/^https?:/.test(p.img) ? p.img : "../" + p.img) + '" alt="' + p.nombre + '" loading="lazy" referrerpolicy="no-referrer">' : "") + '</span>' +
      '<span class="tx"><small>' + p.marca + " · " + p.conc + " · " + p.pres.map(function (x) { return x.ml + " ml"; }).join(" / ") + '</small><b>' + p.nombre + '</b><span class="mn">' +
      ns.map(function (n) { return n.f ? '<img src="../fotos/notas/' + n.f + '.webp" alt="" loading="lazy">' : '<i style="background:' + n.c + '"></i>'; }).join("") +
      '<em>' + ns.map(function (n) { return n.n; }).join(" + ") + '</em></span></span>' +
      '<span class="cp">' + (d ? '<span class="ds">−' + d + '% vs tienda</span>' : "<span></span>") +
      '<span class="pr">' + (disp(p) ? (p.pres.length > 1 ? "Desde " : "") + fmt.format(Math.min.apply(null, p.pres.map(function (x) { return x.precio; }))) + (d ? "<s>" + fmt.format(p.antes) + "</s>" : "") : "Agotado por ahora") + '</span>' +
      '<span class="go">' + (disp(p) ? "Ver y comprar →" : "Ver ficha →") + '</span></span>';
  });
})();
"""


def pagina(titulo, desc, cuerpo, canon, raiz="../"):
    fotos = sorted(f[:-5] for f in os.listdir(os.path.join(RAIZ, "fotos", "notas")) if f.endswith(".webp"))
    js = JS.replace("%FOTOS%", json.dumps(fotos))
    return f"""<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(titulo)} | Scantalia Perfumería</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(titulo)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Scantalia Perfumería">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#0F0F0E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@900&family=IBM+Plex+Mono:wght@400;500;600&family=Courier+Prime:wght@400;700&display=swap">
<link rel="stylesheet" href="blog.css">
<script>try{{var t=localStorage.getItem("ag-theme");document.documentElement.setAttribute("data-theme",t==="light"?"light":"dark")}}catch(e){{}}</script>
</head>
<body>
<header class="top"><div class="top-in"><a class="logo" href="{TIENDA}">SCANTALIA</a><nav><a href="{TIENDA}#perfumes">Tienda</a><a href="index.html" class="keep">Guías</a><a href="{TIENDA}#test" class="keep">Test de perfume</a></nav></div></header>
{cuerpo}
<footer><div class="wrap"><span>© 2026 Scantalia Perfumería · Perfumes originales · México</span><span><a href="../privacidad.html">Aviso de privacidad</a></span></div></footer>
<script src="../perfumes.js?v=VERSION"></script>
<script>{js}</script>
</body>
</html>
"""


def fichas(texto):
    return re.sub(r"\[\[([a-z0-9-]+)\]\]", lambda m: f'<a data-perfume="{m.group(1)}" href="{TIENDA}#perfume-{m.group(1)}">Ver perfume</a>', texto)


def main():
    os.makedirs(os.path.join(RAIZ, "blog"), exist_ok=True)
    ver = re.search(r"perfumes\.js\?v=([0-9a-z]+)", open(os.path.join(RAIZ, "base.html"), encoding="utf-8").read()).group(1)
    open(os.path.join(RAIZ, "blog", "blog.css"), "w", encoding="utf-8").write(CSS)
    banner = f'<div class="testban"><div><span class="k" style="color:#555">¿No sabe cuál escoger?</span><b>Haga el test de perfume</b></div><a href="{TIENDA}#test">Empezar el test →</a></div>'
    for a in ARTICULOS:
        strip = "".join(f'<div><img src="../fotos/notas/{n}.webp" alt=""><span>{n}</span></div>' for n in a["portada"] if os.path.exists(os.path.join(RAIZ, "fotos", "notas", n + ".webp")))
        otros = "".join(f'<a href="{o["slug"]}.html"><span>{html.escape(o["titulo"])}</span><span>→</span></a>' for o in ARTICULOS if o is not a)
        cuerpo = f"""<main class="wrap">
<div style="padding-top:36px"><div class="k u"><a href="index.html" style="text-decoration:none">Guías Scantalia</a> / {html.escape(a['corto'])}</div>
<h1 class="u u2">{html.escape(a['titulo'])}</h1><p class="lead u u3">{html.escape(a['desc'])}</p>
<div class="strip">{strip}</div>
<div class="meta"><span>{a['fecha']}</span><span>Lectura de {a['lectura']}</span><span>Por el equipo de Scantalia</span></div></div>
<article class="post">{fichas(a['cuerpo'].replace('TIENDA', TIENDA))}{banner}</article>
<section class="mas"><h2>Más guías</h2><div class="ls">{otros}</div></section>
</main>"""
        open(os.path.join(RAIZ, "blog", a["slug"] + ".html"), "w", encoding="utf-8").write(
            pagina(a["titulo"], a["desc"], cuerpo, f"{SITIO}/blog/{a['slug']}.html").replace("VERSION", ver))
    tarjetas = "".join(f"""<a href="{a['slug']}.html"><div class="im">{''.join(f'<img src="../fotos/notas/{n}.webp" alt="" loading="lazy">' for n in a['portada'])}</div><div class="k">{a['fecha']} · {a['lectura']}</div><h2>{html.escape(a['titulo'])}</h2><p>{html.escape(a['desc'])}</p></a>""" for a in ARTICULOS)
    cuerpo = f"""<main class="wrap"><div style="padding-top:36px"><div class="k u">Guías Scantalia</div><h1 class="u u2">El recetario</h1><p class="lead u u3">Guías para elegir perfume según la temporada, la ocasión y lo que le gusta oler. Solo hablamos de fragancias que tenemos en existencia, originales y por debajo de tienda departamental.</p></div>
<div class="lista">{tarjetas}</div>{banner}</main>"""
    open(os.path.join(RAIZ, "blog", "index.html"), "w", encoding="utf-8").write(
        pagina("Guías de perfumes", "Guías para elegir perfume: temporada, regalos, duración y notas. Fragancias originales en México.", cuerpo, f"{SITIO}/blog/").replace("VERSION", ver))
    # comprobar que todos los perfumes citados existen en el catálogo
    cat = open(os.path.join(RAIZ, "perfumes.js"), encoding="utf-8").read()
    faltan = sorted({m for a in ARTICULOS for m in re.findall(r"\[\[([a-z0-9-]+)\]\]", a["cuerpo"]) if f'id: "{m}"' not in cat})
    print(json.dumps({"articulos": len(ARTICULOS), "perfumes_que_ya_no_estan": faltan}, ensure_ascii=False))


if __name__ == "__main__":
    main()
