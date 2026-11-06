#!/usr/bin/env python3
"""Escribe automáticamente la ficha (notas, descripción, acordes) de cada perfume de Costco
que se va a publicar y todavía no tiene ficha, a partir de la descripción de Costco.

- No toca las fichas que ya existen (las escritas a mano se respetan).
- Solo crea ficha si Costco trae al menos 3 notas; si no, el perfume no se publica.
- Marca las fichas creadas con "auto": true.

Uso: python3 scripts/fichas_auto.py
"""
import json, os, re, sys, unicodedata, zlib

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from precios import precio

costco = json.load(open(os.path.join(RAIZ, "datos", "costco.json"), encoding="utf-8"))
ruta_f = os.path.join(RAIZ, "datos", "fichas.json")
fichas = json.load(open(ruta_f, encoding="utf-8"))
ruta_base = os.path.join(RAIZ, "datos", "base.js")
base = open(ruta_base, encoding="utf-8").read()
claves_notas = set(re.findall(r"^\s{2}([a-z_]+):\s*\{", base, re.M))


def sin_acentos(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn").lower()


def semilla(t):
    return zlib.crc32(t.encode("utf-8"))


# ---------- marca y nombre ----------
MARCAS = ["Jean Paul Gaultier", "Carolina Herrera", "Dolce & Gabbana", "Dolce&Gabbana", "Giorgio Armani", "Emporio Armani",
          "Calvin Klein", "Hugo Boss", "Paco Rabanne", "Yves Saint Laurent", "Parfums De Marly", "Parfums de Marly",
          "Tommy Hilfiger", "Ralph Lauren", "Viktor & Rolf", "Viktor&Rolf", "Salvatore Ferragamo", "Elizabeth Arden",
          "Adolfo Dominguez", "Adolfo Domínguez", "Jesus Del Pozo", "Jesús del Pozo", "Perry Ellis", "Ariana Grande",
          "Jimmy Choo", "Michael Kors", "Marc Jacobs", "Kenneth Cole", "Maison Alhambra", "Al Haramain", "Swiss Arabian",
          "French Avenue", "Paris Corner", "Jo Milano", "Antonio Banderas", "Issey Miyake", "Nina Ricci", "Oscar de la Renta",
          "Tom Ford", "Banana Republic", "Abercrombie & Fitch", "Abercrombie&Fitch", "Mont Blanc", "Hermes", "Hermès",
          "Lancome", "Lancôme", "Elie Saab", "Juliette Has A Gun", "Maison Margiela", "Narciso Rodriguez", "Bvlgari",
          "Bulgari", "Paris Hilton", "Britney Spears", "Penhaligon's", "Kilian", "Initio", "Xerjoff", "Nishane", "Mancera",
          "Montale", "Armaf", "Lattafa", "Orientica", "Afnan", "Rasasi", "Ajmal", "Rabanne", "Montblanc",
          "Versace", "Guerlain", "Givenchy", "Burberry", "Prada", "Valentino", "Coach", "DKNY", "Cacharel", "Lacoste",
          "Azzaro", "Chloé", "Chloe", "Dior", "Chanel", "Gucci", "Creed", "Mugler", "Kenzo", "Davidoff", "Moschino",
          "Ferragamo", "Boss", "Hugo", "Shakira", "Halloween", "Lalique", "Loewe", "Ph", "Vichy", "Tous", "Benetton",
          "Clinique", "Estée Lauder", "Estee Lauder", "Cartier", "Chopard", "Police", "Diesel", "Guess", "Replay", "Zara"]
MARCAS.sort(key=len, reverse=True)
BONITA = {"Dolce&Gabbana": "Dolce & Gabbana", "Parfums De Marly": "Parfums de Marly", "Viktor&Rolf": "Viktor & Rolf",
          "Abercrombie&Fitch": "Abercrombie & Fitch", "Mont Blanc": "Montblanc", "Lancome": "Lancôme", "Hermes": "Hermès",
          "Chloe": "Chloé", "Estee Lauder": "Estée Lauder", "Bulgari": "Bvlgari", "Adolfo Domínguez": "Adolfo Domínguez",
          "Adolfo Dominguez": "Adolfo Domínguez", "Jesus Del Pozo": "Jesús del Pozo", "Ph": "PH"}


def marca_nombre(nombre):
    n = re.sub(r"\s+", " ", nombre).strip()
    n = re.sub(r"\b\d+(?:[.,]\d+)?\s*ml\b", "", n, flags=re.I)
    n = re.sub(r"\b(edp|edt|eau de parfum|eau de toilette|spray|vaporizador|refillable|recargable|para dama|para caballero|para hombre|para mujer)\b", "", n, flags=re.I)
    n = re.sub(r"\s*,\s*", " ", n).strip(" ,-")
    marca = None
    for m in MARCAS:
        if sin_acentos(n).startswith(sin_acentos(m) + " ") or sin_acentos(n) == sin_acentos(m):
            marca, resto = m, n[len(m):].strip()
            break
    if not marca:
        partes = n.split(" ", 1)
        marca, resto = partes[0], (partes[1] if len(partes) > 1 else partes[0])
    marca = BONITA.get(marca, marca)
    if marca == "Hugo Boss" and resto.lower().startswith("boss "):
        pass
    resto = re.sub(r"\s+", " ", resto).strip() or marca
    # Títulos: respetar mayúsculas existentes salvo TODO EN MAYÚSCULAS
    if resto.isupper() and len(resto) > 4:
        resto = resto.title()
    return marca, resto


# ---------- notas ----------
def limpiar_nota(t):
    t = re.sub(r"\([^)]*\)", "", t)
    t = re.sub(r"\b(notas?|de salida|de coraz[oó]n|de fondo|son|es|la|las|el|los|y unas?)\b\s*$", "", t, flags=re.I)
    t = t.strip(" .:;•-*•")
    t = re.sub(r"^(un|una|unas|unos|toque de|acorde de|acordes de)\s+", lambda m: "Acorde de " if "acorde" in m.group(0).lower() else "", t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip()
    if not t or len(t) > 40 or len(t) < 2:
        return None
    return t[0].upper() + t[1:]


def partir(txt):
    txt = re.sub(r"\([^)]*\)", "", txt)
    piezas = re.split(r",|;|•|•|\s+y\s+|\s+e\s+(?=[a-záéíóú])|\.\s|\s+&\s+", txt)
    out = []
    for p in piezas:
        c = limpiar_nota(p)
        if c and sin_acentos(c) not in [sin_acentos(x) for x in out]:
            out.append(c)
    return out[:5]


ETIQ = [("salida", r"salida|apertura|inicio|top"), ("corazon", r"coraz[oó]n|centro|medio"), ("fondo", r"fondo|base|estela")]


def notas_de(desc):
    if not desc:
        return None
    d = desc.replace("•", "•")
    # posiciones de cada capa
    marcas = []
    for capa, pat in ETIQ:
        m = re.search(r"(?:nota|notas)\s+(?:de\s+)?(?:" + pat + r")[^:;.]{0,40}?(?::|\bson\b|\bes\b)|\b(?:" + pat + r")\s*:", d, flags=re.I)
        if m:
            marcas.append((m.start(), m.end(), capa))
    if len(marcas) < 2:
        return None
    marcas.sort()
    res = {}
    for i, (ini, fin, capa) in enumerate(marcas):
        hasta = marcas[i + 1][0] if i + 1 < len(marcas) else len(d)
        trozo = d[fin:hasta]
        trozo = re.split(r"\.\s+[A-ZÁÉÍÓÚ][a-záéíóú]+\s+(?!y\b)|Disfruta", trozo)[0]
        res[capa] = partir(trozo)
    if sum(len(v) for v in res.values()) < 3:
        return None
    for c in ("salida", "corazon", "fondo"):
        res.setdefault(c, [])
    # si falta una capa, repartir
    if not res["corazon"] and len(res["salida"]) > 2:
        res["corazon"] = [res["salida"].pop()]
    if not res["fondo"] and len(res["corazon"]) > 2:
        res["fondo"] = [res["corazon"].pop()]
    if not all(res.values()):
        return None
    return res


def familia_de(desc):
    m = re.search(r"familia\s+(?:olfativa\s+)?([a-záéíóúñü ]{4,40}?)(?:\s+para|\s+lanzad|\s+creada|,|\.|\s+de\s+|\s+y\s+fue)", desc or "", flags=re.I)
    if not m:
        return None
    f = m.group(1).strip().lower()
    f = re.sub(r"^(de\s+la\s+|la\s+)", "", f)
    return f[0].upper() + f[1:] if f else None


def anio_de(desc):
    m = re.search(r"\b(?:en el|en)\s+(19[5-9]\d|20[0-2]\d)\b", desc or "")
    return m.group(1) if m else None


def conc_de(nombre, desc):
    t = sin_acentos(nombre + " " + (desc or ""))
    if "eau de toilette" in t or re.search(r"\bedt\b", t):
        return "EDT"
    if "extrait" in t or re.search(r"\belixir\b", t) or re.search(r"\bparfum\b(?! de)", sin_acentos(nombre)):
        return "Parfum"
    if "eau de parfum" in t or re.search(r"\bedp\b", t):
        return "EDP"
    if "colonia" in t or "cologne" in t:
        return "EDC"
    return "EDP"


# ---------- acordes ----------
CAT = {
    "Cítrico": "limon lima bergamota mandarina naranja toronja pomelo yuzu cidra citric neroli",
    "Floral": "rosa jazmin iris peonia flor azahar tuberosa orquidea violeta lirio magnolia gardenia fresia ylang heliotropo muguete geranio hibisco loto mimosa azucena camelia osmanto lila jacinto clavel",
    "Afrutado": "pera manzana fruta frutos bayas cereza pina durazno melocoton frambuesa fresa casis grosella lichi mango coco granada ciruela datil maracuya granadilla melon sandia higo arandano mora",
    "Avainillado": "vainilla tonka benjui",
    "Amaderado": "cedro sandalo vetiver madera guayaco cachemira palo oud agar abedul ciprés cipres",
    "Ambarado": "ambar ambroxan ladano incienso mirra resina balsamo styrax opopo elemi",
    "Cálido especiado": "pimienta canela cardamomo azafran clavo jengibre nuez moscada comino especia anis",
    "Aromático": "lavanda salvia romero menta tomillo albahaca estragon cilantro esclarea enebro hierba verde artemisa",
    "Gourmand": "caramelo chocolate cacao cafe praline miel almendra avellana tofe toffee azucar regaliz merengue malvavisco crema leche ron",
    "Almizclado": "almizcle musk",
    "Cuero": "cuero gamuza tabaco",
    "Fresco": "marina mar acuatic ozon agua te sorbete",
}
CAT_K = {k: v.split() for k, v in CAT.items()}
CALIDOS = {"Avainillado", "Ambarado", "Cálido especiado", "Gourmand", "Cuero", "Amaderado"}
FRESCOS = {"Cítrico", "Fresco", "Aromático"}
COLOR = {"Cítrico": "#E8C25A", "Floral": "#E9A9BC", "Afrutado": "#E57A8A", "Avainillado": "#D9A35E", "Amaderado": "#8A6A48",
         "Ambarado": "#C47A2C", "Cálido especiado": "#9E4A2A", "Aromático": "#7E9A7A", "Gourmand": "#A0673A",
         "Almizclado": "#E8E0D6", "Cuero": "#5A3A2A", "Fresco": "#8EC3D6"}


def acordes_de(n):
    puntos = {}
    for capa, peso in (("salida", 1.0), ("corazon", 1.3), ("fondo", 1.5)):
        for nota in n[capa]:
            s = sin_acentos(nota)
            for cat, ks in CAT_K.items():
                if any(k in s for k in ks):
                    puntos[cat] = puntos.get(cat, 0) + peso
    if not puntos:
        puntos = {"Floral": 1}
    orden = sorted(puntos.items(), key=lambda x: -x[1])[:4]
    top = orden[0][1]
    return [[c, int(round(50 + 40 * v / top))] for c, v in orden]


# ---------- notas destacadas ----------
CLAVE = [("limon", "limon lima"), ("bergamota", "bergamota"), ("mandarina", "mandarina naranja"), ("toronja", "toronja pomelo"),
         ("neroli", "neroli"), ("rosa", "rosa"), ("jazmin", "jazmin"), ("iris", "iris"), ("peonia", "peonia"), ("azahar", "azahar"),
         ("tuberosa", "tuberosa"), ("violeta", "violeta"), ("gardenia", "gardenia"), ("azucena", "azucena lirio muguete"),
         ("fresia", "fresia"), ("loto", "loto"), ("mimosa", "mimosa"), ("vainilla", "vainilla"), ("haba", "tonka"),
         ("ambar", "ambar ambroxan"), ("sandalo", "sandalo"), ("cedro", "cedro"), ("vetiver", "vetiver"), ("pachuli", "pachuli"),
         ("oud", "oud agar"), ("maderas", "madera guayaco cachemira"), ("cuero", "cuero gamuza"), ("tabaco", "tabaco"),
         ("lavanda", "lavanda"), ("menta", "menta"), ("salvia", "salvia esclarea"), ("cardamomo", "cardamomo"), ("canela", "canela"),
         ("pimienta", "pimienta"), ("caramelo", "caramelo tofe toffee azucar"), ("cacao", "cacao chocolate"), ("miel", "miel"),
         ("almendra", "almendra"), ("avellana", "avellana"), ("coco", "coco"), ("pina", "pina"), ("pera", "pera"),
         ("manzana", "manzana"), ("frambuesa", "frambuesa"), ("fresa", "fresa"), ("grosella", "grosella casis"), ("lichi", "lichi"),
         ("mango", "mango"), ("durazno", "durazno melocoton"), ("granada", "granada"), ("mar", "marina mar acuatic"),
         ("castana", "castana"), ("laurel", "laurel"), ("champana", "champan"), ("merengue", "merengue"), ("caramelo", "praline")]


def clave_de(nota):
    s = sin_acentos(nota)
    for k, ws in CLAVE:
        if any(re.search(r"\b" + w, s) for w in ws.split()) and k in claves_notas:
            return k
    return None


def destacadas_de(n, seccion):
    out = []
    respaldo = {"salida": ["bergamota", "mandarina", "limon"], "corazon": ["rosa", "jazmin", "lavanda"] if seccion == "Mujer" else ["lavanda", "salvia", "rosa"], "fondo": ["maderas", "ambar", "vainilla"]}
    for capa in ("salida", "corazon", "fondo"):
        k = next((clave_de(x) for x in n[capa] if clave_de(x) and clave_de(x) not in out), None)
        if not k:
            k = next(x for x in respaldo[capa] if x not in out)
        out.append(k)
    return out


# ---------- textos ----------
def lista(xs):
    xs = [x if x[:2].isupper() else x[0].lower() + x[1:] for x in xs]
    xs = ["notas verdes" if x in ("verdes", "verde") else x for x in xs]
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " y " + xs[-1]


LEMAS = {
    "Cítrico": ["Frescura luminosa.", "Energía cítrica para todo el día.", "Ligereza y elegancia.", "Brillo fresco y limpio."],
    "Floral": ["Un ramo elegante.", "Feminidad luminosa.", "Flores con carácter.", "Delicadeza que se recuerda."],
    "Afrutado": ["Jugosa y alegre.", "Dulzura vibrante.", "Un toque frutal irresistible.", "Alegría en cada aplicación."],
    "Avainillado": ["Calidez que envuelve.", "Dulce y sensual.", "Una caricia de vainilla.", "Suavidad adictiva."],
    "Amaderado": ["Elegancia con carácter.", "Profundidad natural.", "Sobriedad sofisticada.", "Maderas con presencia."],
    "Ambarado": ["Misterio cálido.", "Sensualidad oriental.", "Una estela inolvidable.", "Calidez profunda."],
    "Cálido especiado": ["Especias con actitud.", "Intensidad magnética.", "Calor y seducción.", "Carácter especiado."],
    "Aromático": ["Frescura con distinción.", "Clásico y versátil.", "Aromático y elegante.", "Limpio y seguro."],
    "Gourmand": ["Una tentación dulce.", "Golosa y envolvente.", "Dulzura irresistible.", "Para quien ama lo dulce."],
    "Almizclado": ["Suavidad que se queda.", "Limpio y sensual.", "Una segunda piel.", "Delicadeza duradera."],
    "Cuero": ["Intenso y refinado.", "Carácter con elegancia.", "Fuerza sofisticada.", "Lujo con actitud."],
    "Fresco": ["Frescura de mar.", "Ligero y vibrante.", "Aire fresco todo el día.", "Limpio y moderno."],
}
CIERRE = {
    "Día · Oficina": ["Ideal para el día y la oficina.", "Una elección versátil para todos los días.", "Perfecto para el día a día."],
    "Noche · Citas": ["Ideal para la noche y las citas.", "Perfecto para ocasiones especiales y noches frías.", "Para dejar huella en la noche."],
    "Día · Noche": ["Versátil para el día y la noche.", "Funciona tanto de día como de noche.", "Un perfume para cualquier ocasión."],
}
PUBLICO = {"Mujer": "para ella", "Hombre": "para él", "Unisex": "unisex"}


def textos(marca, nombre, seccion, fam, anio, n, acordes, ocasion, sem):
    v = sem % 3
    top = acordes[0][0]
    fam_txt = (fam or (top + " " + (acordes[1][0] if len(acordes) > 1 else ""))).strip().lower()
    a1 = f"{nombre} de {marca} es una fragancia {fam_txt} {PUBLICO[seccion]}" + (f", lanzada en {anio}." if anio else ".")
    s, c, f = lista(n["salida"]), lista(n["corazon"]), lista(n["fondo"])
    if v == 0:
        a2 = f"Abre con {s}; en el corazón aparecen {c}, y un fondo de {f} le da carácter y duración."
    elif v == 1:
        a2 = f"Su salida de {s} da paso a un corazón de {c}, que descansa sobre un fondo de {f}."
    else:
        a2 = f"Las notas de {s} abren con personalidad; {c} forman su corazón, y {f} dejan una estela memorable."
    a3 = CIERRE[ocasion][sem % len(CIERRE[ocasion])]
    lema = LEMAS.get(top, LEMAS["Floral"])[sem % 4]
    return lema, " ".join([a1, a2, a3])


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", sin_acentos(t)).strip("-")[:60]


def seccion_de(p, nombre):
    if p.get("dama") and not p.get("caballero"):
        return "Mujer"
    if p.get("caballero") and not p.get("dama"):
        return "Hombre"
    s = sin_acentos(nombre)
    if re.search(r"\b(femme|woman|women|her|mujer|dama|lady|girl|donna|pour elle)\b", s):
        return "Mujer"
    if re.search(r"\b(homme|man|men|him|hombre|caballero|uomo|boy|pour lui)\b", s):
        return "Hombre"
    return "Unisex"


creadas, sin_notas = 0, []
existentes_id = {f.get("id") for f in fichas.values()}
for p in costco["productos"]:
    if p["codigo"] in fichas or precio(p) is None:
        continue
    n = notas_de(p.get("desc", ""))
    if not n:
        sin_notas.append(p["nombre"])
        continue
    marca, nombre = marca_nombre(p["nombre"])
    seccion = seccion_de(p, p["nombre"])
    conc = conc_de(p["nombre"], p.get("desc", ""))
    acordes = acordes_de(n)
    cats = [a[0] for a in acordes[:2]]
    if any(c in CALIDOS for c in cats[:1]) and not any(c in FRESCOS for c in cats[:1]):
        temporada, ocasion = "Otoño · Invierno", "Noche · Citas"
    elif cats[0] in FRESCOS:
        temporada, ocasion = "Primavera · Verano", "Día · Oficina"
    else:
        temporada, ocasion = "Todo el año", "Día · Noche"
    dur, proy = {"EDT": ("5–7 h", 3), "EDC": ("3–5 h", 2), "Parfum": ("9–11 h", 4)}.get(conc, ("7–9 h", 3 if ocasion != "Noche · Citas" else 4))
    sem = semilla(p["codigo"])
    fam = familia_de(p.get("desc", ""))
    lema, venta = textos(marca, nombre, seccion, fam, anio_de(p.get("desc", "")), n, acordes, ocasion, sem)
    pid = slug(f"{marca} {nombre} {conc} {seccion}")
    fichas[p["codigo"]] = {
        "id": pid, "auto": True, "destacadas": destacadas_de(n, seccion), "marca": marca, "nombre": nombre, "conc": conc,
        "seccion": seccion, "familia": fam or (acordes[0][0] + (" " + acordes[1][0].lower() if len(acordes) > 1 else "")),
        "lema": lema, "venta": venta, "salida": n["salida"], "corazon": n["corazon"], "fondo": n["fondo"], "acordes": acordes,
        "duracion": dur, "proyeccion": proy, "temporada": temporada, "ocasion": ocasion,
        "forma": ["cuadrado", "alto", "redondo", "facetado"][sem % 4], "liquido": COLOR.get(acordes[0][0], "#C9A46A"),
    }
    creadas += 1

json.dump(fichas, open(ruta_f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"fichas_creadas": creadas, "sin_notas_en_costco": len(sin_notas), "ejemplos_sin_notas": sin_notas[:15]}, ensure_ascii=False, indent=1))
