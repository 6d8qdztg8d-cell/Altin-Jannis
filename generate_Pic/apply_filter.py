import sys, os, numpy as np
from PIL import Image, ImageFilter, ImageEnhance

def apply_realistic_filter(path):
    img = Image.open(path).convert("RGB")

    # 1. Leicht reduzierte Schärfe (Unsharpness)
    img = img.filter(ImageFilter.GaussianBlur(radius=0.55))

    # 2. Kontrast minimal senken
    img = ImageEnhance.Contrast(img).enhance(0.92)

    # 3. Sättigung leicht senken
    img = ImageEnhance.Color(img).enhance(0.88)

    # 4. Helligkeit minimal senken
    img = ImageEnhance.Brightness(img).enhance(0.97)

    # 5. Leichtes Rauschen (Filmkorn-Effekt)
    arr = np.array(img, dtype=np.int16)
    noise = np.random.normal(0, 6, arr.shape).astype(np.int16)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr)

    # 6. JPEG-Qualität leicht senken beim Speichern (simuliert Handy-Kompression)
    img.save(path, "JPEG", quality=82, optimize=True)
    print(f"  filtered: {os.path.basename(path)}")

images = [
    "vorher-rasen.jpg", "nachher-rasen.jpg",
    "vorher-hecke.jpg", "nachher-hecke.jpg",
    "vorher-beet.jpg",  "nachher-beet.jpg",
    "vorher-platten.jpg","nachher-platten.jpg",
    "vorher-aufraeum.jpg","nachher-aufraeum.jpg",
]

base = os.path.join(os.path.dirname(__file__), "..", "images")
for name in images:
    apply_realistic_filter(os.path.join(base, name))

print("Alle Filter angewendet.")
