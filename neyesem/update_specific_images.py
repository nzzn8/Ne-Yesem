import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neyesem.settings')
django.setup()

from core.models import Recipe

images_map = {
    "Şakşuka": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/%C5%9Eak%C5%9Fuka.JPG/800px-%C5%9Eak%C5%9Fuka.JPG",
    "Pratik Bezelye Yemeği": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Etli_bezelye.jpg/800px-Etli_bezelye.jpg",
    "Mercimek Çorbası": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Mercimek_%C3%A7orbas%C4%B1_with_butter.jpg/800px-Mercimek_%C3%A7orbas%C4%B1_with_butter.jpg",
    "Kuru Fasulye & Pilav": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Kuru_Fas%C3%BClye_-_Turkish_dish_with_white_beans_and_stewed_beef.jpg/800px-Kuru_Fas%C3%BClye_-_Turkish_dish_with_white_beans_and_stewed_beef.jpg",
    "Zeytinyağlı Taze Fasulye": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Taze_fasulye.jpg/800px-Taze_fasulye.jpg",
    "Karnıyarık": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Karn%C4%B1yar%C4%B1k_2016.jpg/800px-Karn%C4%B1yar%C4%B1k_2016.jpg"
}

for title, url in images_map.items():
    recipes_updated = Recipe.objects.filter(title=title).update(image_url=url)
    print(f"Updated {recipes_updated} recipes for '{title}'")

print("Belirtilen yemek görselleri başarıyla daha otantik fotoğraflarla güncellendi!")
