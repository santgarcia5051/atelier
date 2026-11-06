#!/usr/bin/env python3
"""Descarga la foto de cada perfume publicado, le quita el fondo y la guarda como WebP transparente
en fotos/recortes/<id>.webp. La página la muestra sobre fondo blanco (modo claro) o negro (modo oscuro).

Origen de la foto, en este orden:
  1) El Palacio de Hierro (datos/palacio.json: id del perfume -> pid de Palacio), 1200 px
  2) La foto de Costco (datos/costco.json)
Solo procesa los que aún no tienen recorte (use --todos para rehacerlos).

Uso: python3 scripts/fotos.py   (después: python3 scripts/generar.py)
Requiere: pip install "rembg[cpu]" pillow  y acceso a elpalaciodehierro.com y costco.com.mx
"""
import io, json, os, sys, urllib.request
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(RAIZ, "fotos", "recortes")
os.makedirs(DEST, exist_ok=True)
leer = lambda n: json.load(open(os.path.join(RAIZ, "datos", n), encoding="utf-8"))

PALACIO = "https://www.elpalaciodehierro.com/dw/image/v2/BDKB_PRD/on/demandware.static/-/Sites-palacio-master-catalog/default/images/{pid}/large/{pid}_x1.jpg?sw=1200&sh=1200&sm=fit&q=95"
ALTO, ANCHO = 1000, 800          # lienzo final (proporción de las tarjetas)
MARGEN = 0.06                    # aire alrededor del frasco


def bajar(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Scantalia catalogo)", "Referer": "https://www.elpalaciodehierro.com/"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read()


def recortar(datos, sesion):
    from rembg import remove
    im = Image.open(io.BytesIO(datos)).convert("RGB")
    sin = remove(im, session=sesion, post_process_mask=True)
    caja = sin.getchannel("A").point(lambda a: 255 if a > 12 else 0).getbbox()
    if not caja:
        return None
    sin = sin.crop(caja)
    w, h = sin.size
    escala = min(ANCHO * (1 - 2 * MARGEN) / w, ALTO * (1 - 2 * MARGEN) / h)
    sin = sin.resize((max(1, round(w * escala)), max(1, round(h * escala))), Image.LANCZOS)
    lienzo = Image.new("RGBA", (ANCHO, ALTO), (0, 0, 0, 0))
    lienzo.paste(sin, ((ANCHO - sin.width) // 2, ALTO - round(ALTO * MARGEN) - sin.height), sin)
    return lienzo


def main():
    from rembg import new_session
    sesion = new_session("isnet-general-use")
    fichas, costco, palacio = leer("fichas.json"), leer("costco.json"), leer("palacio.json")
    foto_costco = {}
    for p in costco["productos"]:
        f = fichas.get(p["codigo"])
        if f and p.get("foto"):
            foto_costco.setdefault(f.get("id") or p["codigo"], p["foto"])
    todos = "--todos" in sys.argv
    hechos, fallas = 0, []
    for pid_perf, url_costco in sorted(foto_costco.items()):
        dst = os.path.join(DEST, pid_perf + ".webp")
        if os.path.exists(dst) and not todos:
            continue
        fuentes = []
        if pid_perf in palacio:
            fuentes.append(("palacio", PALACIO.format(pid=palacio[pid_perf]["pid"])))
        fuentes.append(("costco", url_costco))
        for origen, url in fuentes:
            try:
                img = recortar(bajar(url), sesion)
                if img:
                    img.save(dst, "WEBP", quality=88, method=6)
                    hechos += 1
                    print(f"ok {origen:7} {pid_perf}", flush=True)
                    break
            except Exception as e:
                print(f"x  {origen:7} {pid_perf}: {e}", flush=True)
        else:
            fallas.append(pid_perf)
    print(json.dumps({"recortes_nuevos": hechos, "fallas": fallas}, ensure_ascii=False))


if __name__ == "__main__":
    main()
