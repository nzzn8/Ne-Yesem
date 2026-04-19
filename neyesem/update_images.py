import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neyesem.settings')
django.setup()

from core.models import Recipe

images_map = {
    "Kuru Fasulye & Pilav": "https://images.unsplash.com/photo-1548943487-a2e4d43b4853?auto=format&fit=crop&w=800&q=80",
    "Zerdeçallı Pirinç Pilavı": "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=800&q=80",
    "Ev Yapımı Çıtır Patates": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=800&q=80",
    "Şakşuka": "https://images.unsplash.com/photo-1572695157366-5e585ab2b69f?auto=format&fit=crop&w=800&q=80",
    "Mercimek Çorbası": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=800&q=80",
    "Karnıyarık": "https://images.unsplash.com/photo-1615486171448-4df2b1ff9ee5?auto=format&fit=crop&w=800&q=80",
    "Zeytinyağlı Taze Fasulye": "https://images.unsplash.com/photo-1533758349520-217838dd6657?auto=format&fit=crop&w=800&q=80",
    "Tavuklu Sebzeli Erişte": "https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=800&q=80",
    "Pratik Bezelye Yemeği": "https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?auto=format&fit=crop&w=800&q=80",
    "Humuslu Tavuk Köftesi": "https://images.unsplash.com/photo-1529042410759-befb1204b468?auto=format&fit=crop&w=800&q=80"
}

for title, url in images_map.items():
    Recipe.objects.filter(title=title).update(image_url=url)

print("Görseller başarıyla güncellendi!")
