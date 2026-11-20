# Scantalia Perfumería — guía técnica para continuar el proyecto

Tienda en línea de perfumes originales (México). La tienda es HTML + CSS + JavaScript sin framework ni paso de compilación de Node, con datos en un archivo JS. Lo publica **GitHub Pages** desde la rama `main` de `santgarcia5051/atelier`. Los pedidos, el cobro y las cuentas los atiende un **Worker de Cloudflare** con base de datos D1.

- Sitio: https://scantalia.com (archivo `CNAME`; DNS en Cloudflare).
- El repositorio es **público**: no subir secretos, correos personales ni datos internos. Los secretos viven solo en Cloudflare.
- Todo el texto público va en **español formal (usted)**.

## Reglas del proyecto (pedidas por el dueño)

- En ninguna parte del sitio debe notarse que se hizo con IA. Los textos van firmados por «el equipo de Scantalia».
- El nombre real del dueño no aparece en el sitio. Se usa «Scantalia Perfumería» / «equipo de Scantalia».
- Diseño vigente: **«Mostrador de recetas»**.
  - Tema oscuro predeterminado y claro tipo papel.
  - Acento dorado (`#C9A35E` en oscuro, `#8C6A2E` en claro).
  - **Sin rojo y sin colores pastel.**
  - Animaciones lentas.
  - Al menos **3 perfumes por renglón con su foto**, también en celular.
  - Fondo de las fotos de frasco: beige `#E9E1D5` (claro) y gris `#292929` (oscuro), variable `--foto-bg` en `construir_recetas.py`. Todas las fotos ocupan el mismo cuadro.
- No cambiar `datos/reglas.json` ni `scripts/precios.py` sin que el dueño lo pida.
- No poner precios a mano: los calcula `precios.py`.
- No borrar fichas existentes.
- Antes de aplicar un cambio de diseño, mostrar ejemplos o una prueba; se aplica cuando el dueño lo aprueba.
- Simular la página con Playwright antes de publicar.
- No mandar correos, comprar ni aceptar términos sin un sí explícito. Nunca escribir contraseñas, claves de API ni datos de tarjeta: eso lo hace el dueño.

## Mapa de archivos

| Ruta | Qué es | ¿Se edita a mano? |
|---|---|---|
| `base.html` | **Plantilla fuente** de la tienda: estructura, carrito, ficha, pedido, cookies, estilos base | Sí (cambios de funcionalidad) |
| `index.html` | Página principal **generada** por `scripts/construir_recetas.py` desde `base.html` | **No** (se sobrescribe) |
| `prueba.html` | Redirección a `index.html` (enlace viejo), generada por `construir_recetas.py` | No |
| `nuevo.html` | Diseño anterior (oscuro y dorado), generado por `construir_nuevo.py`. Ya no se enlaza | No |
| `perfumes.js` | Catálogo **generado** por `scripts/generar.py` (`PERFUMES`, `NOTAS`, `SECCIONES`, `ENVIO`) | No |
| `tienda.json` | Precios públicos y envíos, generado por `generar.py`. El Worker lo lee para calcular el total en el servidor | No |
| `worker/pedidos.js` | Worker `scantalia-pedidos` (ruta `scantalia.com/api/*`): pedidos, Stripe y cuentas | Sí (se despliega aparte a Cloudflare) |
| `db/0001_base_completa.sql` | Esquema de la base D1 | Sí (probar migraciones primero en la base de pruebas) |
| `blog/` | Guías de compra, generadas por `scripts/construir_blog.py` | No (editar el script) |
| `terminos.html`, `privacidad.html` | Páginas legales, generadas por `scripts/construir_legales.py` | No |
| `datos/costco.json` | Lo que hay hoy en Costco: código, nombre, ml, costo, existencia, foto, descripción, tipo, precio de referencia | Lo escribe `aplicar.py` |
| `datos/fichas.json` | Ficha de cada perfume por código de Costco: marca, nombre, notas, textos, familia… | Sí, con cuidado |
| `datos/base.js` | `NOTAS` (notas olfativas con foto y color), `SECCIONES`, `ENVIO` (zonas, tarifas, días) | Sí |
| `datos/reglas.json` | Reglas de precio y comisión | **Solo si el dueño lo pide** |
| `datos/privacidad.html` | Texto fuente del aviso de privacidad | Sí |
| `datos/palacio.json`, `arome_fotos.json`, `liverpool_fotos.json`, `amazon_fotos.json` | Qué foto externa usa cada perfume (id → pid o URL) | Sí |
| `fotos/` | Fotos propias: `notas/` (46, una por nota), `escenas/` (43), frascos sueltos (`*.webp`) | — |
| `scripts/` | Generadores y pipeline del catálogo (ver abajo) | Sí |

## Cómo se genera el sitio

```bash
python3 scripts/generar.py            # datos/* -> perfumes.js y tienda.json
python3 scripts/actualizar_version.py # nueva ?v= para perfumes.js en base.html y reconstruye TODO:
                                      #   construir_nuevo.py   -> nuevo.html
                                      #   construir_recetas.py -> index.html (+ prueba.html)
                                      #   construir_blog.py    -> blog/
                                      #   construir_legales.py -> terminos.html, privacidad.html
```

- Los builders hacen reemplazos exactos sobre `base.html` y fallan con `assert` si el texto buscado no existe. Si se cambia `base.html`, hay que correr `actualizar_version.py` y revisar que no truene.
- Solo usan Python 3 estándar. `scripts/fotos.py` es opcional y requiere `pip install "rembg[cpu]" pillow` (en la nube: `pip install --break-system-packages`).
- El blog toma los perfumes en vivo de `perfumes.js` (`[[id-del-perfume]]` en el texto inserta la ficha de compra) y avisa si un perfume citado ya no está en el catálogo.

## Pipeline del catálogo (Costco → tienda)

Un perfume se publica solo si:
- está en Costco,
- tiene ficha,
- y el precio cumple la regla.

Si está agotado se muestra «No disponible».

1. `scripts/navegador_1_costco.js`: corre **en un navegador en www.costco.com.mx**. Usa la API OCC `/rest/v2/mexico/products/search`, lee fragancias (sin sets ni kits) y su «Tipo» (EDT/EDP), compara contra el `datos/costco.json` publicado y deja el resultado en `window.name` (prefijo `SCX2`).
2. `scripts/navegador_0_refrescar.js` (los lunes) y `scripts/navegador_2_liverpool.js`: corren **en la misma pestaña en www.liverpool.com.mx**. Buscan el precio de tienda departamental (referencia «Antes $X») y dejan un paquete comprimido en `window.__P`, que se lee por partes con `window.__parte(i)`.
3. `python3 scripts/aplicar.py paquete.txt`: aplica el paquete a `datos/costco.json`. Si un producto agotado llega con costo 0, conserva el costo anterior.
4. `python3 scripts/fichas_auto.py` (con `--rehacer` opcional): escribe las fichas que faltan a partir de la descripción de Costco. Contiene alias de marca, erratas y correcciones por código.
5. `generar.py` → `actualizar_version.py` → commit → push.

**Precios** (`precios.py` + `reglas.json`):
- Con precio de referencia: referencia −20/−15/−10 % (el primero que deje al menos $350 de ganancia).
- Sin referencia: costo +30 %, con ganancia mínima de $350.
- En ambos casos se descuentan la comisión de cobro (4.05 % + $4.64, la de Mercado Pago, aunque ahora se cobra con Stripe), 10 % de impuestos y 5 % de comisión extra. El precio termina en 99.

**Fotos de frascos** (orden de prioridad en `generar.py`):
1. recorte propio (`fotos/recortes/<id>.webp`, 1200 × 1200, transparente, frasco al 70 %). Se crea con `scripts/fotos.py` (o `--local <id> <archivo>` para una foto ya recortada). Verificar antes que sea la versión exacta (EDT/EDP/Parfum, flanker).
2. El Palacio de Hierro (CDN demandware, 1000 px)
3. Arome México (`arome_fotos.json`; solo fotos que coinciden exactamente en perfume y presentación)
4. Liverpool (`ss701…/xl/`, unos 940 px; los marcados `"xl": false` usan `sp701…/i/`)
5. Amazon México (`m.media-amazon.com …_AC_SL1500_`)
6. Costco (740 px)

Las fotos externas se muestran **enlazadas** a esos servidores, no copiadas al repo. Si una tienda cambia la URL, esa foto deja de verse.
Las fotos de tienda con fondo blanco llevan la clase `.blanco` y se funden con `multiply` sobre el fondo del tema (`--foto-bg`), así que el blanco desaparece en claro y en oscuro. En oscuro se ven más oscuras porque `multiply` nunca supera el gris del fondo; el brillo completo solo se logra con recorte transparente. Las fotos con fondo gris (p. ej. El Palacio de Hierro, 1 Million Gold Elixir) no se funden: necesitan recorte propio.

## Funcionalidades del sitio

- Catálogo por secciones (Mujer, Hombre, Unisex), búsqueda y filtro por nota, orden, y ficha-receta fija en escritorio.
- Ficha del perfume con notas, acordes, duración, presentaciones y similares.
- Enlaces directos: `index.html#perfume-<id>` abre una ficha; `index.html#test` abre el test.
- **Test «¿No sabe qué perfume escoger?»**: 6 preguntas, resultado con % de compatibilidad y 2 alternativas.
- **Carrito y pedido**:
  - Datos de entrega y cálculo de envío por código postal (zonas en `ENVIO`; gratis desde 2 perfumes).
  - El pedido ya pide todo lo que Skydropx necesita para generar la guía: nombre, teléfono (10 dígitos), correo, calle y número, colonia, C.P., ciudad (el estado sale del C.P.) y referencias. Los datos no se guardan en el navegador.
  - **Dos casillas obligatorias** (términos/privacidad y devoluciones) habilitan «Generar pedido».
  - En scantalia.com el pedido se manda a `POST /api/pedido`: el Worker valida, calcula el total con `tienda.json`, lo guarda en D1 (folio `SC-DDMM-NNNN`) y crea la sesión de **Stripe Checkout**. Fuera de scantalia.com (p. ej. en local) la página cae al pedido por texto con folio.
  - El webhook `POST /api/stripe` marca el pedido como `pagado` o `pago_fallido`.
- **Cuentas de cliente** (`/api/cuenta/<accion>`): registro, inicio de sesión y código de 5 dígitos por correo (Resend). Sin la clave de Resend quedan desactivadas.
- Tema claro/oscuro y banner de cookies («Aceptar todo» o «Solo necesarias»). La preferencia de gustos solo se guarda con «todo».
- Blog con 4 guías de compra, términos y condiciones (20 secciones, devoluciones de 5 días hábiles según el art. 56 de la LFPC) y aviso de privacidad.

**`localStorage`** del navegador del cliente:

| Clave | Guarda |
|---|---|
| `ag-cart` | carrito |
| `ag-theme` | tema claro u oscuro |
| `ag-sec` | sección elegida |
| `ag-sort` | orden del catálogo |
| `sc-cookies` | consentimiento de cookies |
| `sc-gustos` | gustos del cliente (solo con «Aceptar todo») |

## Servicios externos

| Servicio | Uso | Estado |
|---|---|---|
| GitHub Pages | Hosting (`.nojekyll`) | Activo; el despliegue tarda de 1 a 5 min |
| Google Fonts | Big Shoulders Display, IBM Plex Mono, Courier Prime, Archivo | Activo |
| Costco México (API OCC y CDN de imágenes) | Fuente del catálogo, costos, existencias y fotos | Activo vía navegador |
| Liverpool | Precio de referencia y fotos | Activo vía navegador |
| El Palacio de Hierro, Amazon México | Fotos (enlazadas) | Activo |
| Instagram `@scantalia`, TikTok | Enlaces de contacto | TikTok sin URL de perfil |
| WhatsApp | Botón oculto (`wa.me/520000000000`) | Número pendiente |
| Cloudflare | DNS de scantalia.com, Worker `scantalia-pedidos` y D1 | Activo. Faltan los secretos del Worker (`STRIPE_SECRET`, `STRIPE_WEBHOOK_SECRET`, `RESEND_KEY`), que guarda el dueño |
| Correo (Zoho Mail) | `contacto@scantalia.com` y otros buzones | Activo. **No tocar los registros MX, SPF ni DKIM** |
| Stripe | Cobro con tarjeta (Checkout + webhook) | Cuenta activa; no cobra hasta que haya secretos |
| Resend | Códigos de verificación de cuentas | Falta cuenta, clave y verificar el dominio (sin tocar los registros de Zoho) |
| Skydropx (u otra paquetería) | Envíos | Cuenta por abrir por el dueño. Por ahora las guías se crean a mano en su panel con los datos del pedido; la API (cotizar y generar guías solas) necesita una función con sus credenciales, aún no hecha |

## Trabajar desde Claude Code en la nube

- Clonar: `git clone https://github.com/santgarcia5051/atelier`. Se trabaja y publica directo en `main`; cada push despliega.
- **Red del entorno cloud**: costco.com.mx, liverpool.com.mx, elpalaciodehierro.com, amazon.com.mx, arome.mx, cdn.shopify.com, scantalia.com, commons.wikimedia.org y github.io están bloqueados desde la shell. El Worker y D1 se manejan con el conector de Cloudflare. Para pip/npm hay que pasar el proxy explícito (`$HTTPS_PROXY`).
- **Lo que todavía depende de la computadora del dueño**: los pasos de navegador del catálogo (1 y 2) y cualquier búsqueda de fotos en tiendas. Se ejecutan en el navegador de la app de escritorio de Claude (herramientas `Claude_Browser`) con la sesión vinculada a su computadora.
- Hay una tarea programada **«Revisión diaria Costco Scantalia»** (8:59, hora de CDMX) que hace todo el pipeline. Necesita la computadora encendida con la app de Claude abierta; si no, queda suspendida por «device_absent». Su instrucción todavía verifica `nuevo.html` en github.io; debería verificar `https://scantalia.com/`.
- **Pruebas locales** (Chromium y Playwright ya instalados en la nube):
  - Servir con `python3 -m http.server 8765` desde la raíz del repo.
  - Probar con Playwright en tamaño iPhone 13 y en escritorio de 1440 px.
  - Interceptar `fonts.googleapis.com` y los dominios de imágenes, porque están bloqueados en la nube.
  - Siempre revisar: que no haya desbordamiento horizontal en celular (`scrollWidth === innerWidth`), que no haya errores de JS, que el test termine y que el carrito llegue a «Pedido generado».
- Commits en español; describir qué cambió para el cliente.

## Pendientes conocidos

- **Panel de administración** en `scantalia.com/admin` con rutas `/api/admin/...` protegidas por Cloudflare Access (código por correo). Bloqueado: el dueño debe activar Zero Trust. Hoy no existe ninguna cuenta de admin.
- Secretos de Stripe y Resend en el Worker, webhook de Stripe y prueba con el producto de $0.01 (con permiso del dueño).
- Aviso al dueño cuando entra un pedido pagado y guía de Skydropx automática.
- Confirmar si el envío es siempre gratis o sigue gratis desde 2 perfumes.
- Unos 90 perfumes solo tienen foto de El Palacio de Hierro: buscar otra fuente y recortar sin fondo (44 recortes propios hechos).
- Costos y reglas de precio son públicos porque el repo es público: decidir si se hace privado o se saca `datos/` del sitio.
- `nuevo.html`, `base.html` y `prueba.html` son públicos aunque no se enlazan.
- Domicilio del responsable en el aviso de privacidad, número de WhatsApp y URL de TikTok.
- Programa de lealtad (propuesto; no aprobado).
