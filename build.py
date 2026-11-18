"""Genera index.html (la página completa) a partir de src/app.html (el contenido)."""
from pathlib import Path

raiz = Path(__file__).parent
import base64
cuerpo = (raiz / "src" / "app.html").read_text(encoding="utf-8")

def dato(nombre, tipo):
    return f"data:{tipo};base64," + base64.b64encode((raiz / "assets" / nombre).read_bytes()).decode()

# el logo y los iconos van dentro de la página para que sea un solo archivo
for marca, nombre, tipo in [("{{logo}}", "logo.jpg", "image/jpeg"), ("{{icono180}}", "icono-180.png", "image/png"),
                            ("{{icono64}}", "icono-64.png", "image/png")]:
    cuerpo = cuerpo.replace(marca, dato(nombre, tipo))
html = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '</head>\n<body>\n' + cuerpo + '\n</body>\n</html>\n')
(raiz / "index.html").write_text(html, encoding="utf-8")
print("index.html generado")
