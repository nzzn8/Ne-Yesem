import os
import re
import unicodedata
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.recipes.models import Recipe

class Command(BaseCommand):
    help = 'Eşleşen dosya isimlerine göre media/recipes/ klasöründeki fotoğrafları tariflere bağlar'

    def normalize_string(self, text):
        if not text:
            return ""
        
        # Türkçe karakterleri manuel olarak dönüştür
        replacements = {
            'ı': 'i', 'I': 'i', 'İ': 'i',
            'ş': 's', 'Ş': 's',
            'ğ': 'g', 'Ğ': 'g',
            'ü': 'u', 'Ü': 'u',
            'ö': 'o', 'Ö': 'o',
            'ç': 'c', 'Ç': 'c',
        }
        for search, replace in replacements.items():
            text = text.replace(search, replace)
        
        # Sadece alfanumerik karakterleri bırak (boşluk, tire, alt çizgi vs. yok et)
        text = text.lower()
        text = re.sub(r'[^a-z0-9]', '', text)
        return text

    def handle(self, *args, **kwargs):
        media_recipes_dir = os.path.join(settings.MEDIA_ROOT, 'recipes')
        
        if not os.path.exists(media_recipes_dir):
            self.stdout.write(self.style.ERROR(f"Klasör bulunamadı: {media_recipes_dir}"))
            return

        # 1. Tüm dosyaları oku ve normalize et
        files = os.listdir(media_recipes_dir)
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        
        normalized_files = {}
        for file in image_files:
            filename_without_ext = os.path.splitext(file)[0]
            norm_name = self.normalize_string(filename_without_ext)
            normalized_files[norm_name] = file

        # 2. Tüm tarifleri al
        recipes = Recipe.objects.all()
        
        match_count = 0
        unmatched_recipes = []
        
        for recipe in recipes:
            norm_title = self.normalize_string(recipe.title)
            
            # 3. Eşleşme kontrolü
            if norm_title in normalized_files:
                matched_file = normalized_files[norm_title]
                recipe.image.name = f"recipes/{matched_file}"
                recipe.image_url = ""  # URL'i temizle, güvenli tarafta kal
                recipe.save(update_fields=['image', 'image_url'])
                
                # Eşleşen dosyayı sözlükten çıkar ki geriye sadece tariflerle eşleşmeyen dosyalar kalsın
                del normalized_files[norm_title]
                match_count += 1
            else:
                unmatched_recipes.append(recipe.title)

        # 4. Sonuçları Raporla
        self.stdout.write(self.style.SUCCESS(f"\nBaşarıyla eşleşen ve güncellenen tarif sayısı: {match_count}"))
        
        if unmatched_recipes:
            self.stdout.write(self.style.WARNING(f"\n--- Eşleşmeyen Tarifler ({len(unmatched_recipes)}) ---"))
            for t in unmatched_recipes:
                self.stdout.write(f"- {t}")

        if normalized_files:
            self.stdout.write(self.style.WARNING(f"\n--- Tarife Bağlanamayan Boşta Kalan Görseller ({len(normalized_files)}) ---"))
            for f in normalized_files.values():
                self.stdout.write(f"- {f}")
