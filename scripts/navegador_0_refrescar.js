/* OPCIONAL (lunes) — Ejecutar en la pestaña de Liverpool ANTES del paso 2.
   Pide volver a revisar el precio de Liverpool de los perfumes que ya tienen precio de referencia,
   para que el "Antes $X" no se quede viejo. */
(async () => {
  const d = await (await fetch("https://santgarcia5051.github.io/atelier/datos/costco.json?t=" + Date.now(), { cache: "no-store" })).json();
  const con = d.productos.filter(p => p.antes);
  window.__REFRESCAR = con.map(p => p.codigo);
  window.__NOMBRES = Object.fromEntries(con.map(p => [p.codigo, p.nombre]));
  window.__GENEROS = Object.fromEntries(con.map(p => [p.codigo, p.dama && !p.caballero ? "dama" : p.caballero && !p.dama ? "caballero" : ""]));
  return "a refrescar: " + con.length;
})();
