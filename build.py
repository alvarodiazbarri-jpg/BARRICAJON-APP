"""Genera la app a partir de src/app.html (el contenido) y assets/ (logo e iconos).

- index.html          → una sola página con todo dentro (la que se publica como enlace de prueba).
- docs/               → la app instalable (PWA): página, manifiesto, service worker e iconos.
                        Es la carpeta que publica GitHub Pages (o Netlify, ver netlify.toml).
"""
import base64
import json
import shutil
from pathlib import Path

raiz = Path(__file__).parent
cuerpo = (raiz / "src" / "app.html").read_text(encoding="utf-8")


def dato(nombre, tipo):
    return f"data:{tipo};base64," + base64.b64encode((raiz / "assets" / nombre).read_bytes()).decode()


def pagina(c):
    # todo lo que va antes del primer <style> (título, iconos, manifiesto…) va en la cabecera
    i = c.index("<style>")
    return ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + c[:i] + '</head>\n<body>\n' + c[i:] + '\n</body>\n</html>\n')


# el logo y los iconos van dentro de la página para que sea un solo archivo
cuerpo = cuerpo.replace("{{logo}}", dato("logo.jpg", "image/jpeg"))
# en la cabecera, el icono como archivo en la app instalable y dentro de la página en la versión de un solo archivo
cuerpo_web = cuerpo.replace("{{icono180}}", "icono-180.png").replace("{{icono64}}", "icono-192.png")
for marca, nombre, tipo in [("{{icono180}}", "icono-180.png", "image/png"), ("{{icono64}}", "icono-64.png", "image/png")]:
    cuerpo = cuerpo.replace(marca, dato(nombre, tipo))

# 1) página única
(raiz / "index.html").write_text(pagina(cuerpo.replace("{{pwa_head}}", "")), encoding="utf-8")

# 2) app instalable
web = raiz / "docs"
web.mkdir(exist_ok=True)
pwa = ('<link rel="manifest" href="manifest.webmanifest">\n'
       '<meta name="mobile-web-app-capable" content="yes">\n'
       '<meta name="apple-mobile-web-app-capable" content="yes">\n'
       '<meta name="apple-mobile-web-app-status-bar-style" content="black">\n'
       "<script>if ('serviceWorker' in navigator) addEventListener('load', () => "
       "navigator.serviceWorker.register('sw.js').catch(() => {}));</script>")
(web / "index.html").write_text(pagina(cuerpo_web.replace("{{pwa_head}}", pwa)), encoding="utf-8")
for f in ["icono-192.png", "icono-512.png", "icono-180.png", "icono-mask-192.png", "icono-mask-512.png"]:
    shutil.copy(raiz / "assets" / f, web / f)
manifiesto = {
    "id": "./",
    "name": "El Barri · Cajón flamenco",
    "short_name": "El Barri",
    "description": "Cuaderno de ejercicios de cajón flamenco: partitura, sonido, tapa animada y metrónomo.",
    "lang": "es",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "background_color": "#000000",
    "theme_color": "#000000",
    "icons": [
        {"src": "icono-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icono-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icono-mask-192.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
        {"src": "icono-mask-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}
(web / "manifest.webmanifest").write_text(json.dumps(manifiesto, ensure_ascii=False, indent=2), encoding="utf-8")
# service worker: siempre intenta bajar la versión nueva; si no hay internet, usa la guardada
(web / "sw.js").write_text("""const CACHE = 'el-barri-v2';
self.addEventListener('install', e => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(fetch(e.request).then(r => {
    const copia = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copia)).catch(() => {});
    return r;
  }).catch(() => caches.match(e.request)));
});
""", encoding="utf-8")
print("index.html y docs/ generados")
