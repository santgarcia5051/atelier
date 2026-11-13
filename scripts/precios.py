"""Regla de precio compartida por generar.py y aplicar.py."""
import json, math, os
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = json.load(open(os.path.join(RAIZ, "datos", "reglas.json"), encoding="utf-8"))

def pct_total():
    """Porcentaje del precio de venta que se descuenta: Mercado Pago + impuestos + comisión extra."""
    return R["comision_pct"] + R.get("impuestos_pct", 0) + R.get("comision_extra_pct", 0)

def comision(p):
    return pct_total() / 100 * p + R["comision_fija"]

def abajo_99(x):
    return int(math.floor((x + 1) / 100) * 100 - 1)

def arriba_99(x):
    return int(math.ceil((x + 1) / 100) * 100 - 1)

def precio(prod):
    """(precio, ganancia, antes o None) o None si no se publica."""
    costo = prod["costo"]
    ref = prod.get("antes")
    if ref:
        cr = R["con_referencia"]
        for d in cr["descuentos_pct"]:
            p = abajo_99(ref * (1 - d / 100))
            g = p - costo - comision(p)
            if g >= cr["ganancia_minima"]:
                return p, round(g), ref
        return None
    sr = R["sin_referencia"]
    minimo = (costo + sr["ganancia_minima"] + R["comision_fija"]) / (1 - pct_total() / 100)
    p = arriba_99(max(costo * (1 + sr["margen_pct"] / 100), minimo))
    return p, round(p - costo - comision(p)), None
