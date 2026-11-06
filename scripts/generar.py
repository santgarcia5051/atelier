#!/usr/bin/env python3
"""Genera perfumes.js a partir de:
  datos/costco.json  -> lo que hay hoy en Costco (precio, existencias, foto, precio de referencia)
  datos/fichas.json  -> la ficha de cada perfume (notas, textos), por código de Costco
  datos/base.js      -> notas con foto, secciones y envíos (se copia tal cual)
  datos/reglas.json  -> reglas de precio

Un perfume aparece en la página solo si:
  - está en Costco (si Costco lo quita, desaparece de la página),
  - tiene ficha escrita,
  - su precio deja al menos la ganancia mínima con el descuento mínimo sobre tienda departamental.
Si Costco lo marca agotado, aparece como "No disponible".

Uso: python3 scripts/generar.py   (desde la carpeta del sitio)
"""
import json, math, os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
leer = lambda n: json.load(open(os.path.join(RAIZ, "datos", n), encoding="utf-8"))

costco = leer("costco.json")
fichas = leer("fichas.json")
base = open(os.path.join(RAIZ, "datos", "base.js"), encoding="utf-8").read()


import sys as _s; _s.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from precios import precio as precio_para
def js(v):
    return json.dumps(v, ensure_ascii=False)


salida, faltan_ficha, sin_margen = [], [], []
por_id = {}
for prod in costco["productos"]:
    code = prod["codigo"]
    r = precio_para(prod)
    if not r:
        sin_margen.append(code)
        continue
    f = fichas.get(code)
    if not f:
        faltan_ficha.append(code)
        continue
    precio, gan, antes = r
    pid = f.get("id") or code
    if pid in por_id:  # mismo perfume en otra presentación: se agrega como tamaño
        item = por_id[pid]
        if not any(x["ml"] == prod["ml"] for x in item["pres"]):
            item["pres"].append({"ml": prod["ml"], "precio": precio, "antes": antes})
            item["pres"].sort(key=lambda x: x["ml"])
            item["antes"] = item["pres"][0]["antes"]
            item["costco"] += "," + code
        item["disponible"] = item["disponible"] or bool(prod["existencia"])
        continue
    item = {
        "id": pid,
        "costco": code,
        "destacadas": f["destacadas"],
        "marca": f["marca"], "nombre": f["nombre"], "conc": f["conc"],
        "seccion": f["seccion"], "familia": f["familia"], "lema": f["lema"], "venta": f["venta"],
        "salida": f["salida"], "corazon": f["corazon"], "fondo": f["fondo"],
        "acordes": f["acordes"], "duracion": f["duracion"], "proyeccion": f["proyeccion"],
        "temporada": f["temporada"], "ocasion": f["ocasion"],
        "pres": [{"ml": prod["ml"], "precio": precio, "antes": antes}],
        "antes": antes,
        "disponible": bool(prod["existencia"]),
        "forma": f.get("forma", "cuadrado"), "liquido": f.get("liquido", "#C9A46A"),
        "img": f.get("img") or prod["foto"],
    }
    por_id[pid] = item
    salida.append(item)

orden = {s: i for i, s in enumerate(["Mujer", "Hombre"])}
salida.sort(key=lambda p: (orden.get(p["seccion"], 9), not p["disponible"], p["marca"], p["nombre"]))

lineas = []
for p in salida:
    campos = ", ".join(f"{k}: {js(v)}" for k, v in p.items())
    lineas.append("  { " + campos + " }")

cabecera = """/* =========================================================
   CATÁLOGO GENERADO AUTOMÁTICAMENTE DESDE COSTCO — NO EDITAR A MANO
   Se reconstruye con scripts/generar.py a partir de datos/costco.json,
   datos/fichas.json y datos/reglas.json.
   Para cambiar la descripción o notas de un perfume: datos/fichas.json.
   Para cambiar la ganancia o el descuento: datos/reglas.json.
   Para cambiar envíos o notas con foto: datos/base.js.
   Actualizado: %s
   ========================================================= */

const PERFUMES = [
""" % costco.get("actualizado", "")

open(os.path.join(RAIZ, "perfumes.js"), "w", encoding="utf-8").write(cabecera + ",\n".join(lineas) + "\n];\n\n" + base)

# notas destacadas que no existen en base.js: avisar
claves = set(re.findall(r"^\s{2}([a-z_]+):\s*\{", base, re.M))
huerfanas = sorted({k for p in salida for k in p["destacadas"] if k not in claves})

resumen = {
    "publicados": len(salida),
    "disponibles": sum(p["disponible"] for p in salida),
    "agotados": sum(not p["disponible"] for p in salida),
    "mujer": sum(p["seccion"] == "Mujer" for p in salida),
    "hombre": sum(p["seccion"] == "Hombre" for p in salida),
    "sin_margen": len(sin_margen),
    "faltan_ficha": faltan_ficha,
    "notas_sin_definir": huerfanas,
}
print(json.dumps(resumen, ensure_ascii=False, indent=1))
if huerfanas:
    sys.exit("ERROR: agregue estas notas a datos/base.js: " + ", ".join(huerfanas))
