"""Genera index.html (la página completa) a partir de src/app.html (el contenido)."""
from pathlib import Path

raiz = Path(__file__).parent
cuerpo = (raiz / "src" / "app.html").read_text(encoding="utf-8")
html = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '</head>\n<body>\n' + cuerpo + '\n</body>\n</html>\n')
(raiz / "index.html").write_text(html, encoding="utf-8")
print("index.html generado")
