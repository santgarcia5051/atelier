#!/usr/bin/env python3
"""Cambia la versión de perfumes.js en index.html (para que los navegadores carguen el catálogo nuevo)
y reconstruye nuevo.html. Uso: python3 scripts/actualizar_version.py"""
import os, re, subprocess, sys, datetime
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(RAIZ, "index.html")
s = open(p, encoding="utf-8").read()
v = datetime.datetime.utcnow().strftime("%Y%m%d%H%M")
s2 = re.sub(r"perfumes\.js\?v=[0-9a-z]+", "perfumes.js?v=" + v, s)
open(p, "w", encoding="utf-8").write(s2)
subprocess.run([sys.executable, os.path.join(RAIZ, "scripts", "construir_nuevo.py")], check=True)
print("versión", v)
