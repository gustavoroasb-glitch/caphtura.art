"""Crea portafolio-archivo-unico.html: una sola página con todas las imágenes incrustadas.

Sirve para abrir el portafolio sin carpeta de imágenes (adjunto en correo, USB, WhatsApp).
Uso, desde esta carpeta:  python crear-archivo-unico.py
"""
import base64, json, pathlib, re

base = pathlib.Path(__file__).parent
html = (base / "index.html").read_text(encoding="utf-8")

def data_uri(path):
    return "data:image/webp;base64," + base64.b64encode(path.read_bytes()).decode()

imgs = {p.stem: data_uri(p) for p in sorted((base / "img").glob("*.webp"))}

# Imágenes fijas del HTML (inicio y retrato)
html = re.sub(r'src="img/([\w-]+)\.webp"', lambda m: f'src="{imgs[m.group(1)]}"', html)
# Quitar la precarga, que apunta a un archivo externo
html = re.sub(r'<link rel="preload" as="image"[^>]*>\n?', "", html)
# Imágenes de proyectos: mapa que usa la función src() del script
html = html.replace("<script>\n{", "<script>window.IMG=" + json.dumps(imgs) + ";</script>\n<script>\n{", 1)

out = base / "portafolio-archivo-unico.html"
out.write_text(html, encoding="utf-8")
print(f"Listo: {out.name} ({out.stat().st_size / 1024 / 1024:.1f} MB)")
