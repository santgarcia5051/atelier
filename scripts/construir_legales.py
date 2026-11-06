#!/usr/bin/env python3
"""Genera las páginas legales con el diseño de la tienda:
  terminos.html   -> Términos y condiciones (incluye la política de devoluciones, #devoluciones)
  privacidad.html -> Aviso de privacidad (el contenido se toma de datos/privacidad.html)

Uso: python3 scripts/construir_legales.py   (desde la carpeta del sitio)
"""
import os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FECHA = "6 de noviembre de 2026"
ver = re.search(r'perfumes\.js\?v=(\d+)', open(os.path.join(RAIZ, "base.html"), encoding="utf-8").read()).group(1)

EXTRA = """
.legal { max-width:780px; margin:0 auto; padding:30px 0 60px; }
.legal p, .legal li { margin:0 0 14px; }
.legal ul, .legal ol { margin:0 0 16px 22px; }
.legal h2 { font-family:var(--display); font-weight:900; text-transform:uppercase; font-size:clamp(30px, 5vw, 44px); line-height:.95; margin:46px 0 14px; padding-top:18px; border-top:1px solid var(--line); scroll-margin-top:90px; }
.legal h3 { font-family:var(--type); font-size:20px; font-weight:700; margin:22px 0 8px; }
.legal strong, .legal b { font-weight:600; color:var(--fg); }
.legal a { color:var(--accent); }
.box { border:1px solid var(--line); background:var(--surface); padding:18px 20px; margin:0 0 16px; }
.box.dest { border-color:var(--accent); }
.box.dest .k { color:var(--accent); margin-bottom:8px; }
mark { background:var(--accent); color:var(--accent-fg); padding:0 5px; }
.indice { display:flex; flex-wrap:wrap; gap:8px; margin:26px 0 0; }
.indice a { font-size:11px; text-transform:uppercase; letter-spacing:.08em; text-decoration:none; border:1px solid var(--line); padding:7px 10px; transition:border-color .6s, color .6s; }
.indice a:hover { border-color:var(--accent); color:var(--accent); }
.pasos { counter-reset:p; list-style:none; margin-left:0 !important; }
.pasos li { counter-increment:p; position:relative; padding-left:46px; min-height:34px; }
.pasos li::before { content:counter(p, decimal-leading-zero); position:absolute; left:0; top:-2px; font-family:var(--display); font-weight:900; font-size:28px; line-height:1; color:var(--accent); }
.si-no { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:0 0 16px; }
.si-no .box { margin:0; }
.si-no ul { margin-left:18px; }
@media (max-width:640px) { .si-no { grid-template-columns:1fr; } .top nav { gap:12px; font-size:11px; } }
"""

def pagina(titulo, descripcion, ruta, etiqueta, h1, cuerpo):
    return f"""<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titulo} | Scantalia Perfumería</title>
<meta name="description" content="{descripcion}">
<meta property="og:title" content="{titulo} | Scantalia Perfumería">
<meta property="og:description" content="{descripcion}">
<meta property="og:site_name" content="Scantalia Perfumería">
<link rel="canonical" href="https://santgarcia5051.github.io/atelier/{ruta}">
<meta name="theme-color" content="#0F0F0E">
<script>try{{var t=localStorage.getItem("ag-theme");document.documentElement.setAttribute("data-theme",t==="light"?"light":"dark")}}catch(e){{document.documentElement.setAttribute("data-theme","dark")}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@900&family=IBM+Plex+Mono:wght@400;500;600&family=Courier+Prime:wght@400;700&display=swap">
<link rel="stylesheet" href="blog/blog.css?v={ver}">
<style>{EXTRA}</style>
</head>
<body>
<header class="top"><div class="top-in"><a class="logo" href="index.html">SCANTALIA</a><nav><a href="index.html#perfumes">Tienda</a><a href="blog/index.html">Guías</a><a href="index.html#test">Test</a></nav></div></header>
<main class="wrap">
<div style="padding-top:36px"><div class="k">Legal / {etiqueta}</div>
<h1>{h1}</h1>
<div class="meta"><span>Última actualización: {FECHA}</span><span>Scantalia Perfumería</span></div></div>
<div class="legal">
{cuerpo}
</div>
</main>
<footer><div class="wrap"><span>© 2026 Scantalia Perfumería · Perfumes originales · México</span><span><a href="terminos.html">Términos y condiciones</a> · <a href="terminos.html#devoluciones">Devoluciones</a> · <a href="privacidad.html">Aviso de privacidad</a></span></div></footer>
</body>
</html>
"""

TERMINOS = """
<p class="lead" style="margin-bottom:8px">Estos términos regulan el uso de este sitio y toda compra que haga en Scantalia Perfumería. Le pedimos leerlos con atención: al generar un pedido, usted confirma que los conoce y los acepta.</p>
<nav class="indice" aria-label="Secciones">
<a href="#definiciones">Definiciones</a><a href="#quienes">Quiénes somos</a><a href="#aceptacion">Aceptación</a><a href="#productos">Productos</a><a href="#precios">Precios</a><a href="#compra">Cómo comprar</a><a href="#pago">Pago</a><a href="#factura">Factura</a><a href="#envios">Envíos</a><a href="#cancelaciones">Cancelaciones</a><a href="#devoluciones">Devoluciones</a><a href="#garantia">Garantía</a><a href="#seguridad">Uso seguro</a><a href="#promociones">Promociones</a><a href="#sitio">Uso del sitio</a><a href="#propiedad">Propiedad intelectual</a><a href="#responsabilidad">Responsabilidad</a><a href="#datos">Datos personales</a><a href="#quejas">Quejas</a><a href="#generales">Disposiciones generales</a>
</nav>

<h2 id="definiciones">1. Definiciones</h2>
<ul>
<li><b>Scantalia</b> o <b>nosotros</b>: Scantalia Perfumería, tienda en línea que opera este sitio.</li>
<li><b>Cliente</b> o <b>usted</b>: la persona que navega en el sitio o hace un pedido.</li>
<li><b>Sitio</b>: esta página web, sus guías, el test de perfume y cualquier canal oficial de Scantalia en redes sociales o mensajería.</li>
<li><b>Pedido</b>: la solicitud de compra que usted genera en el carrito, identificada con un folio.</li>
<li><b>Producto</b>: cada perfume o artículo que se ofrece en el sitio.</li>
<li><b>Días hábiles</b>: de lunes a viernes, sin contar días festivos oficiales. <b>Días naturales</b>: todos los días del calendario.</li>
</ul>

<h2 id="quienes">2. Quiénes somos y cómo contactarnos</h2>
<p>Scantalia Perfumería es un comercio en línea que vende perfumes originales y realiza envíos a toda la República Mexicana. Los datos del responsable, el domicilio para recibir notificaciones y el correo de contacto se encuentran en nuestro <a href="privacidad.html">aviso de privacidad</a>. También puede escribirnos por mensaje directo en nuestras redes sociales oficiales.</p>
<p>Respondemos en un plazo de 1 a 2 días hábiles. Para cualquier aclaración, tenga a la mano el folio de su pedido.</p>

<h2 id="aceptacion">3. Aceptación de los términos</h2>
<ul>
<li>Para comprar debe ser mayor de 18 años y tener capacidad legal para contratar. Si es menor de edad, la compra debe hacerla su madre, padre o tutor.</li>
<li>Antes de generar su pedido le pedimos marcar dos casillas: una para aceptar estos términos y el aviso de privacidad, y otra para aceptar la política de devoluciones. Sin ambas casillas no es posible completar la compra.</li>
<li>La aceptación por medios electrónicos tiene plena validez, conforme al Código de Comercio y al Código Civil Federal.</li>
<li>Se aplica la versión de estos términos publicada el día en que usted generó su pedido.</li>
</ul>

<h2 id="productos">4. Productos e información</h2>
<ul>
<li>Todos nuestros perfumes son <b>originales, nuevos y se entregan sellados</b> en su empaque de fábrica. No vendemos imitaciones, decants ni probadores.</li>
<li>Las fotografías son ilustrativas. El diseño del frasco, de la caja o del celofán puede variar según el lote del fabricante, sin que cambie la fragancia.</li>
<li>Las notas olfativas, la familia, la duración, la proyección, la temporada y la ocasión que mostramos son orientativas. Cada piel, clima y forma de aplicación hacen que un perfume se perciba distinto, por lo que no constituyen una garantía del resultado.</li>
<li>El contenido de cada presentación (ml) y su concentración (Eau de Toilette, Eau de Parfum, Parfum, etc.) se indican en la ficha de cada producto.</li>
<li>Los resultados del test de perfume y las recomendaciones de nuestras guías son sugerencias para orientarle; la elección final es suya.</li>
<li>La disponibilidad se confirma al recibir su pedido. Si un producto se agota antes de que su pago se acredite, se lo informaremos y podrá elegir otro o cancelar sin costo.</li>
</ul>

<h2 id="precios">5. Precios</h2>
<ul>
<li>Los precios están en pesos mexicanos (MXN) y son el precio total del producto, sin cargos ocultos. El costo de envío se calcula con su código postal y se muestra por separado antes de generar su pedido.</li>
<li>El precio tachado es un <b>precio de referencia</b> de tiendas departamentales en México, para que pueda comparar. No es un precio al que Scantalia haya vendido antes.</li>
<li>Los precios pueden cambiar sin previo aviso, pero <b>siempre respetamos el precio confirmado en su pedido</b> mientras su link de pago esté vigente.</li>
<li>Si por un error evidente de captura un precio se publica de forma notoriamente incorrecta, se lo informaremos antes de cobrar y usted decidirá si continúa con la compra al precio correcto o la cancela sin costo.</li>
</ul>

<h2 id="compra">6. Cómo comprar</h2>
<ol class="pasos">
<li>Agregue sus perfumes al carrito y capture sus datos de entrega.</li>
<li>Marque las dos casillas de aceptación y genere su pedido. Recibirá un folio.</li>
<li>Envíenos su pedido por mensaje directo o correo.</li>
<li>Confirmamos disponibilidad y le enviamos un link de pago seguro por el total.</li>
<li>Su compra queda confirmada cuando el pago se acredita. A partir de ese momento preparamos su pedido y le enviamos su número de rastreo.</li>
</ol>
<p>Generar un pedido no le obliga a pagar; el contrato de compraventa se perfecciona cuando usted paga el link que le enviamos. Podemos no aceptar un pedido cuando el producto no esté disponible, cuando los datos de entrega estén incompletos o sean inconsistentes, o cuando existan indicios razonables de fraude. En esos casos se lo informaremos y, si ya hubiera pagado, le reembolsaremos el total.</p>

<h2 id="pago">7. Pago</h2>
<ul>
<li>Aceptamos tarjeta de crédito o débito, transferencia y efectivo en OXXO, a través de una plataforma de pagos segura.</li>
<li>Los datos de su tarjeta los captura y procesa directamente la plataforma de pagos; Scantalia no los recibe ni los almacena.</li>
<li>El link de pago tiene una vigencia de 48 horas. Si vence, puede pedirnos uno nuevo; el precio y la disponibilidad se confirman de nuevo.</li>
<li>Los pagos en efectivo pueden tardar hasta 48 horas en acreditarse. El pedido se envía una vez acreditado el pago.</li>
<li>Las promociones de meses sin intereses, cuando existan, dependen del banco emisor y de la plataforma de pagos.</li>
<li>Si usted desconoce un cargo ante su banco (contracargo) sin habernos contactado antes, podremos suspender el envío hasta aclarar la situación.</li>
</ul>

<h2 id="factura">8. Facturación</h2>
<p>Si necesita factura (CFDI), solicítela al hacer su pedido o dentro del mismo mes de su compra, con su nombre o razón social, RFC, código postal fiscal, régimen fiscal y uso del CFDI. Después de ese plazo podría no ser posible emitirla, conforme a las disposiciones fiscales.</p>

<h2 id="envios">9. Envíos y entrega</h2>
<ul>
<li><b>Local</b> (Ciudad de México y Estado de México): llega en 5 a 7 días hábiles.</li>
<li><b>Nacional</b> (resto de la República): llega en 7 a 10 días hábiles.</li>
<li><b>Extendida</b> (Baja California, Baja California Sur, Chiapas, Quintana Roo y Yucatán): llega en 8 a 12 días hábiles.</li>
</ul>
<p>Los días cuentan a partir de que su pago se acredita. El envío es gratis en pedidos de 2 perfumes o más, según se indica en el carrito.</p>
<ul>
<li>Todos los envíos van asegurados y con número de rastreo, que le enviamos cuando su paquete sale.</li>
<li>Los tiempos dependen de la paquetería y pueden extenderse en temporadas altas, por clima, por causas de fuerza mayor o en zonas de difícil acceso. Si eso ocurre, se lo informaremos.</li>
<li>Usted es responsable de que su domicilio esté completo y correcto. Si la paquetería no puede entregar por datos incorrectos o por ausencia reiterada y el paquete regresa, el reenvío tendrá un costo adicional.</li>
<li>La entrega se considera hecha cuando la paquetería entrega el paquete en el domicilio indicado, a usted o a la persona que lo reciba ahí.</li>
<li>No enviamos fuera de México por ahora.</li>
</ul>
<p><b>Al recibir su paquete, revíselo antes de abrir la caja del perfume.</b> Si llega golpeado, mojado o abierto, tómele fotos y repórtelo dentro de los 2 días naturales siguientes (vea la sección 11).</p>

<h2 id="cancelaciones">10. Cancelaciones</h2>
<ul>
<li><b>Antes de pagar:</b> puede cancelar su pedido en cualquier momento, sin costo; basta con no pagar el link o avisarnos.</li>
<li><b>Después de pagar y antes del envío:</b> escríbanos lo antes posible. Si su pedido aún no sale, le reembolsamos el total.</li>
<li><b>Después del envío:</b> ya no es posible cancelar; aplica la política de devoluciones de la sección 11.</li>
</ul>

<h2 id="devoluciones">11. Política de devoluciones</h2>
<div class="box dest">
<div class="k">En resumen</div>
<p style="margin:0">Tiene <b>2 días naturales</b> desde que recibe su pedido para solicitar una devolución, indicando el motivo. Solo aceptamos devoluciones de perfumes <b>con la caja cerrada y el sello o celofán intacto</b>.</p>
</div>

<h3>Cómo solicitarla</h3>
<ol class="pasos">
<li>Escríbanos dentro de los 2 días naturales siguientes a la entrega, según la fecha que marque la guía de rastreo.</li>
<li>Indique su número de pedido y el <b>motivo</b> de la devolución.</li>
<li>Envíe fotos claras del perfume, de su caja y del paquete en que lo recibió.</li>
<li>Le confirmaremos si procede y le daremos las indicaciones para enviarlo de regreso. No envíe productos sin nuestra confirmación.</li>
</ol>

<h3>Cuándo procede y cuándo no</h3>
<div class="si-no">
<div class="box"><div class="k">Sí procede</div><ul>
<li>La caja está cerrada y el sello o celofán de fábrica está intacto.</li>
<li>El perfume no se ha usado ni probado.</li>
<li>Se devuelve completo, con su empaque y lo que incluía.</li>
<li>La solicitud se hizo dentro de los 2 días naturales.</li>
</ul></div>
<div class="box"><div class="k">No procede</div><ul>
<li>La caja fue abierta o el sello o celofán está roto.</li>
<li>El perfume fue abierto, rociado o muestra uso.</li>
<li>El producto está incompleto o dañado por mal uso.</li>
<li>La solicitud llega después de los 2 días naturales.</li>
</ul></div>
</div>
<p>Por higiene y para garantizar la originalidad de lo que vendemos, <b>no aceptamos devoluciones de perfumes cuya caja haya sido abierta</b>. Que una fragancia no sea de su agrado una vez abierta no es motivo de devolución, por lo que le pedimos revisar con calma su elección antes de comprar; si tiene dudas, pruebe nuestro <a href="index.html#test">test de perfume</a> o escríbanos.</p>

<h3>Producto dañado, equivocado o incompleto</h3>
<p>Si su perfume llegó roto, con fugas, si recibió un producto distinto al que pidió o falta algún artículo, repórtelo dentro de los mismos 2 días naturales con fotos o video del paquete y del producto. En estos casos la caja abierta no impide la reposición: le enviaremos el producto correcto o le reembolsaremos, y nosotros cubrimos los envíos.</p>

<h3>Reembolsos</h3>
<ul>
<li>Revisamos el producto al recibirlo. Si cumple las condiciones, reembolsamos el precio del perfume por el mismo medio de pago en un plazo de hasta 10 días hábiles. El tiempo en que se refleje depende de su banco.</li>
<li>Cuando la devolución no se debe a un error nuestro, el costo del envío de regreso corre por cuenta del cliente y el envío original no es reembolsable.</li>
<li>Si el producto devuelto no cumple las condiciones, se lo regresaremos y el costo de ese envío correrá por su cuenta.</li>
<li>No hacemos reembolsos en efectivo.</li>
</ul>
<p>Esta política no limita los derechos que la Ley Federal de Protección al Consumidor le otorga.</p>

<h2 id="garantia">12. Garantía de originalidad y defectos</h2>
<ul>
<li>Garantizamos que todos los perfumes que vendemos son originales y provienen de distribuidores establecidos en México. Si tiene cualquier duda sobre la autenticidad de su perfume, escríbanos con su número de pedido.</li>
<li>Si detecta un defecto de fábrica (por ejemplo, un atomizador que no funciona), escríbanos con fotos o video. Revisaremos el caso y, si procede, le ofreceremos el cambio del producto o el reembolso, conforme a la ley.</li>
<li>La garantía no cubre daños por mal uso, caídas, exposición al calor o al sol, ni el cambio natural que un perfume puede tener con el tiempo una vez abierto.</li>
</ul>

<h2 id="seguridad">13. Uso seguro del producto</h2>
<ul>
<li>Los perfumes son productos cosméticos de uso externo e inflamables. Manténgalos lejos del fuego, de fuentes de calor y del alcance de niñas, niños y mascotas.</li>
<li>No los aplique sobre piel irritada o lastimada, ni cerca de los ojos.</li>
<li>Si tiene piel sensible o alergias, revise los ingredientes en la caja y haga una prueba en una zona pequeña antes de usarlo. Si aparece irritación, suspenda su uso y consulte a un médico.</li>
<li>Las guías y descripciones del sitio son informativas y no son una recomendación médica.</li>
</ul>

<h2 id="promociones">14. Promociones y descuentos</h2>
<ul>
<li>Cada promoción indica su vigencia y sus condiciones. Aplican hasta agotar existencias.</li>
<li>Salvo que se indique lo contrario, las promociones no son acumulables entre sí, no son canjeables por efectivo y aplican solo a pedidos pagados durante su vigencia.</li>
<li>Si devuelve parte de un pedido que obtuvo un beneficio (por ejemplo, envío gratis por comprar 2 perfumes), el reembolso descontará el beneficio que ya no corresponda.</li>
</ul>

<h2 id="sitio">15. Uso del sitio</h2>
<p>Usted se compromete a usar el sitio de forma lícita. No está permitido:</p>
<ul>
<li>Proporcionar datos falsos o de terceros sin su autorización.</li>
<li>Hacer pedidos con fines de reventa en volumen sin acuerdo previo con nosotros.</li>
<li>Copiar, extraer de forma automatizada o reproducir el contenido del sitio.</li>
<li>Intentar dañar, interferir o acceder sin autorización al sitio o a sus sistemas.</li>
</ul>
<p>Podemos suspender la atención o cancelar pedidos de quien incumpla estas reglas.</p>

<h2 id="propiedad">16. Propiedad intelectual</h2>
<p>Los textos, guías, test, fotografías propias, ilustraciones y el diseño del sitio pertenecen a Scantalia y están protegidos por la ley. No pueden copiarse, modificarse ni usarse con fines comerciales sin nuestra autorización por escrito.</p>
<p>Las marcas, logotipos y nombres de los perfumes pertenecen a sus respectivos titulares. Los mencionamos solo para identificar los productos que vendemos. Scantalia es un comercio independiente y no está afiliado, patrocinado ni respaldado por esas marcas. Algunas fotografías de producto provienen de las marcas, sus distribuidores u otras tiendas, y se usan solo para identificar el producto.</p>

<h2 id="responsabilidad">17. Limitación de responsabilidad</h2>
<ul>
<li>Hacemos lo posible por que la información del sitio sea correcta y esté actualizada, pero puede contener errores u omisiones involuntarios que corregiremos en cuanto los detectemos.</li>
<li>No somos responsables por interrupciones del sitio debidas a mantenimiento, fallas de internet o de proveedores externos.</li>
<li>No somos responsables por retrasos o incumplimientos causados por caso fortuito o fuerza mayor, como desastres naturales, contingencias sanitarias, paros, bloqueos o fallas generales de la paquetería.</li>
<li>Los enlaces a sitios de terceros se incluyen por comodidad; no controlamos su contenido ni sus políticas.</li>
<li>Nada de lo anterior limita la responsabilidad que la ley no permita excluir ni los derechos que le corresponden como consumidor.</li>
</ul>

<h2 id="datos">18. Datos personales y comunicaciones</h2>
<p>Tratamos sus datos conforme a nuestro <a href="privacidad.html">aviso de privacidad</a> y a la Ley Federal de Protección de Datos Personales en Posesión de los Particulares. Al hacer un pedido, usted acepta que nos comuniquemos con usted por correo, mensaje directo o WhatsApp para todo lo relacionado con su compra. Solo le enviaremos promociones si no se ha opuesto a recibirlas.</p>

<h2 id="quejas">19. Quejas y aclaraciones</h2>
<p>Si algo no salió como esperaba, escríbanos primero: queremos resolverlo. Le responderemos en un plazo de 1 a 2 días hábiles y buscaremos una solución en un máximo de 10 días hábiles.</p>
<p>Si no quedamos en un acuerdo, usted puede acudir a la Procuraduría Federal del Consumidor (Profeco), incluido su servicio de conciliación en línea, Concilianet.</p>

<h2 id="generales">20. Disposiciones generales</h2>
<ul>
<li><b>Modificaciones:</b> podemos actualizar estos términos para reflejar cambios en la ley o en nuestro servicio. La versión vigente estará siempre en esta página con su fecha de actualización.</li>
<li><b>Divisibilidad:</b> si alguna parte de estos términos se considera inválida, el resto seguirá vigente.</li>
<li><b>Idioma:</b> estos términos se redactan en español, que prevalece sobre cualquier traducción.</li>
<li><b>Ley aplicable y jurisdicción:</b> estos términos se rigen por las leyes de los Estados Unidos Mexicanos, en especial la Ley Federal de Protección al Consumidor y el Código de Comercio. Para cualquier controversia, las partes se someten a los tribunales competentes conforme a la ley, sin perjuicio de la competencia de la Profeco.</li>
</ul>
"""

# --- Términos ---
open(os.path.join(RAIZ, "terminos.html"), "w", encoding="utf-8").write(pagina(
    "Términos y condiciones", "Cómo comprar, pagar, envíos y política de devoluciones de Scantalia Perfumería.",
    "terminos.html", "Términos", "Términos y condiciones", TERMINOS))

# --- Aviso de privacidad: contenido de datos/privacidad.html con el diseño nuevo ---
src = open(os.path.join(RAIZ, "datos", "privacidad.html"), encoding="utf-8").read()
cuerpo = src[src.index("</p>", src.index('class="updated"')) + 4: src.index("</main>")]
open(os.path.join(RAIZ, "privacidad.html"), "w", encoding="utf-8").write(pagina(
    "Aviso de privacidad", "Qué datos recabamos, para qué los usamos y cómo ejercer sus derechos.",
    "privacidad.html", "Privacidad", "Aviso de privacidad", cuerpo.strip()))
print("terminos.html y privacidad.html listas")
