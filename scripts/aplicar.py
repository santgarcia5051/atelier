#!/usr/bin/env python3
"""Aplica el paquete del navegador (paso 2) a datos/costco.json.
Uso: python3 scripts/aplicar.py paquete.txt
paquete.txt = el texto de window.__P (base64url de JSON comprimido con gzip), en una o varias líneas.
Imprime los códigos nuevos que ya cumplen la regla de precio y todavía no tienen ficha."""
import base64, gzip, json, math, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta = os.path.join(RAIZ, "datos", "costco.json")
txt = "".join(open(sys.argv[1]).read().split())
txt += "=" * (-len(txt) % 4)
D = json.loads(gzip.decompress(base64.urlsafe_b64decode(txt)))

actual = json.load(open(ruta, encoding="utf-8")) if os.path.exists(ruta) else {"productos": []}
por = {p["codigo"]: p for p in actual["productos"]}
presentes = set(D["presentes"])

if len(presentes) < 50:
    sys.exit("ERROR: el paquete trae muy pocos perfumes; no se cambia nada.")

for c in D.get("quitados", []):
    por.pop(c, None)
for c in list(por):
    if c not in presentes:
        por.pop(c)
for ch in D.get("cambios", []):
    if ch["codigo"] in por:
        # Costco muestra precio 0 cuando un producto está agotado: se conserva el último costo conocido
        por[ch["codigo"]].update({k: v for k, v in ch.items() if k != "codigo" and not (k == "costo" and not v)})
refs = D.get("refs", {})
for p in D.get("nuevos", []):
    por[p["codigo"]] = dict(p)
for c, r in refs.items():
    if c in por and r and r.get("antes"):
        por[c]["antes"] = r["antes"]
        por[c]["liverpool"] = r.get("liverpool", "")
        por[c]["ref_fecha"] = D["fecha"][:10]

actual["productos"] = sorted(por.values(), key=lambda p: p["nombre"])
actual["actualizado"] = D["fecha"]
json.dump(actual, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from precios import precio
fichas = json.load(open(os.path.join(RAIZ, "datos", "fichas.json"), encoding="utf-8")) if os.path.exists(os.path.join(RAIZ, "datos", "fichas.json")) else {}
califica = lambda p: precio(p) is not None
faltan = [p for p in actual["productos"] if califica(p) and p["codigo"] not in fichas]
print(json.dumps({
    "productos": len(actual["productos"]), "nuevos": len(D.get("nuevos", [])), "cambios": len(D.get("cambios", [])),
    "quitados": len(D.get("quitados", [])),
    "faltan_ficha": [{"codigo": p["codigo"], "nombre": p["nombre"], "dama": p.get("dama"), "caballero": p.get("caballero"), "liverpool": p.get("liverpool")} for p in faltan],
}, ensure_ascii=False, indent=1))
