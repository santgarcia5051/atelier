#!/usr/bin/env python3
"""Descarga la foto de cada perfume publicado, le quita el fondo y la guarda como WebP transparente
en fotos/recortes/<id>.webp: 1200 x 1200 px, frasco centrado ocupando el 70 %.
La página la muestra sobre fondo beige #E9E1D5 (modo claro) o gris #292929 (modo oscuro).

Origen de la foto, en este orden:
  1) El Palacio de Hierro (datos/palacio.json: id del perfume -> pid de Palacio), 1200 px
  2) Liverpool (datos/liverpool_fotos.json: id del perfume -> URL de la foto)
  3) La foto de Costco (datos/costco.json)
Solo procesa los que aún no tienen recorte (use --todos para rehacerlos).

Uso: python3 scripts/fotos.py   (después: python3 scripts/generar.py)
     python3 scripts/fotos.py --local <id-del-perfume> <archivo>   normaliza una foto ya recortada (PNG/WebP transparente)
Antes de guardar una foto, verificar que sea la versión exacta (EDT/EDP/Parfum, flanker) del perfume.
Requiere: pip install "rembg[cpu]" pillow  y acceso a elpalaciodehierro.com, liverpool.com.mx y costco.com.mx
"""
import io, json, os, sys, urllib.request
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(RAIZ, "fotos", "recortes")
os.makedirs(DEST, exist_ok=True)
leer = lambda n: json.load(open(os.path.join(RAIZ, "datos", n), encoding="utf-8"))

PALACIO = "https://www.elpalaciodehierro.com/dw/image/v2/BDKB_PRD/on/demandware.static/-/Sites-palacio-master-catalog/default/images/{pid}/large/{pid}_x1.jpg?sw=1200&sh=1200&sm=fit&q=95"
LADO = 1200                      # lienzo final cuadrado
OCUPA = 0.70                     # el frasco ocupa el 70 % del lado más largo


def bajar(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Scantalia catalogo)", "Referer": "https://www.elpalaciodehierro.com/"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read()


def normalizar(sin):
    """Recorta el frasco (fondo transparente) y lo centra en un lienzo de 1200 x 1200 ocupando el 70 %."""
    caja = sin.getchannel("A").point(lambda a: 255 if a > 12 else 0).getbbox()
    if not caja:
        return None
    sin = sin.crop(caja)
    w, h = sin.size
    escala = LADO * OCUPA / max(w, h)
    sin = sin.resize((max(1, round(w * escala)), max(1, round(h * escala))), Image.LANCZOS)
    lienzo = Image.new("RGBA", (LADO, LADO), (0, 0, 0, 0))
    lienzo.paste(sin, ((LADO - sin.width) // 2, (LADO - sin.height) // 2), sin)
    return lienzo


def recortar(datos, sesion):
    from rembg import remove
    im = Image.open(io.BytesIO(datos)).convert("RGB")
    return normalizar(remove(im, session=sesion, post_process_mask=True))


def main():
    if sys.argv[1:2] == ["--local"]:
        pid_perf, archivo = sys.argv[2], sys.argv[3]
        img = normalizar(Image.open(archivo).convert("RGBA"))
        img.save(os.path.join(DEST, pid_perf + ".webp"), "WEBP", quality=90, method=6)
        print("ok local", pid_perf)
        return
    from rembg import new_session
    sesion = new_session("isnet-general-use")
    fichas, costco, palacio = leer("fichas.json"), leer("costco.json"), leer("palacio.json")
    liverpool = leer("liverpool_fotos.json")
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
        if pid_perf in liverpool:
            fuentes.append(("liverpool", liverpool[pid_perf]["img"]))
        fuentes.append(("costco", url_costco))
        for origen, url in fuentes:
            try:
                img = recortar(bajar(url), sesion)
                if img:
                    img.save(dst, "WEBP", quality=90, method=6)
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
