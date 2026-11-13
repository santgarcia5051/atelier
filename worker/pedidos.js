// Recibe los pedidos de la página de Scantalia y los guarda en la base de datos.
// No contiene claves ni contraseñas.

const ORIGEN_PERMITIDO = "https://scantalia.com";

const cabeceras = {
  "Access-Control-Allow-Origin": ORIGEN_PERMITIDO,
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Content-Type": "application/json; charset=utf-8",
};

function respuesta(datos, estado = 200) {
  return new Response(JSON.stringify(datos), { status: estado, headers: cabeceras });
}

function limpiar(valor, largo) {
  return String(valor ?? "").trim().slice(0, largo);
}

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: cabeceras });
    }
    if (request.method !== "POST") {
      return respuesta({ error: "Método no permitido" }, 405);
    }

    let datos;
    try {
      datos = await request.json();
    } catch {
      return respuesta({ error: "Datos no válidos" }, 400);
    }

    const folio = limpiar(datos.folio, 30);
    const nombre = limpiar(datos.nombre, 100);
    const correo = limpiar(datos.correo, 120);
    const telefono = limpiar(datos.telefono, 20);
    const direccion = limpiar(datos.direccion, 300);
    const codigoPostal = limpiar(datos.codigo_postal, 5);
    const total = Number(datos.total) || 0;
    const items = JSON.stringify(Array.isArray(datos.items) ? datos.items.slice(0, 50) : []);
    const esPrueba = datos.es_prueba ? 1 : 0;

    if (!folio || !nombre || !correo.includes("@")) {
      return respuesta({ error: "Faltan datos del pedido" }, 400);
    }

    try {
      await env.DB.prepare(
        `INSERT INTO pedidos
           (folio, creado_en, estado, nombre, telefono, correo, direccion, codigo_postal, items, total, es_prueba)
         VALUES (?, datetime('now'), 'pendiente_pago', ?, ?, ?, ?, ?, ?, ?, ?)`
      )
        .bind(folio, nombre, telefono, correo, direccion, codigoPostal, items, total, esPrueba)
        .run();
    } catch (error) {
      return respuesta({ error: "No se pudo guardar el pedido" }, 500);
    }

    return respuesta({ ok: true, folio });
  },
};
