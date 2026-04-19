import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neyesem.settings')
django.setup()

from core.models import Recipe, Ingredient, RecipeIngredient

def parse_advanced(line):
    line = line.strip()
    if line.startswith('-') or line.startswith('*'):
         line = line[1:].strip()
         
    # 1. Virgül, "ve", "ile", " / " bağlaçlarından böl
    # Sadece etrafında boşluk olan " / " işaretinden böl ki "1/2" gibi kesirler bozulmasın
    parts_raw = re.split(r',|\s+ve\s+|\s+ile\s+|\s+/\s+', line)
    
    results = []
    
    adjectives = [
        "orta boy", "küçük boy", "büyük boy", "ince doğranmış", 
        "yemeklik doğranmış", "rendelenmiş", "ezilmiş", "haşlanmış", 
        "doğranmış", "kıyılmış", "süzülmüş", "eritilmiş", "oda sıcaklığında",
        "ayıklanmış", "kabuğu soyulmuş", "dilimlenmiş", "iri kıyım", "taze çekilmiş",
        "sıcak", "soğuk", "ılık", "kavrulmuş", "çekilmiş", "dövülmüş"
    ]
    
    unit_keywords = [
        "gram", "gr", "kg", "kilogram", "diş", "demet", "adet", "paket", 
        "tatlı", "yemek", "çay", "su", "bardak", "bardağı", "kaşık", "kaşığı", 
        "litre", "ml", "avuç", "tutam", "dilim", "yarım", "çeyrek", "tepeleme",
        "fincan", "fincanı", "kutu", "kase", "baş"
    ]
    
    for part in parts_raw:
        part = part.strip()
        if not part: continue
        
        words = part.split()
        quantity_words = []
        name_words = []
        
        parsing_qty = True
        
        # Miktar ve birimleri isimden ayır
        for w in words:
            lower_w = w.lower()
            has_digit = any(char.isdigit() for char in w)
            is_unit_word = lower_w in unit_keywords
            
            if parsing_qty and (has_digit or is_unit_word):
                quantity_words.append(w)
            else:
                parsing_qty = False
                name_words.append(w)
                
        qty_text = " ".join(quantity_words)
        name_text = " ".join(name_words)
        
        if not name_text:
            name_text = qty_text
            qty_text = ""
            
        # Sıfatları temizle
        lower_name = name_text.lower()
        for adj in adjectives:
            if adj in lower_name:
                pattern = re.compile(re.escape(adj), re.IGNORECASE)
                name_text = pattern.sub("", name_text).strip()
                lower_name = name_text.lower()
                
        name_text = name_text.strip()
        name_text = re.sub(r'\s+', ' ', name_text) # Fazla boşlukları temizle
        
        if name_text:
            # Baş harflerini büyüt
            results.append((qty_text, name_text.title()))
            
    return results

if __name__ == "__main__":
    print("Mevcut malzemeler temizleniyor...")
    RecipeIngredient.objects.all().delete()
    
    print("Tarifler yeniden, akıllı ayrıştırma ile taranıyor...")
    count = 0
    for recipe in Recipe.objects.all():
        if recipe.ingredients:
            for line in recipe.ingredients.splitlines():
                if not line.strip(): continue
                parsed_items = parse_advanced(line)
                
                for qty, name in parsed_items:
                    if not name: continue
                    ing, _ = Ingredient.objects.get_or_create(name=name)
                    RecipeIngredient.objects.create(recipe=recipe, ingredient=ing, quantity_text=qty)
                    count += 1

    print("Kullanılmayan eski kirli malzemeler veritabanından siliniyor...")
    deleted_count, _ = Ingredient.objects.filter(recipe_ingredients__isnull=True).delete()
    
    print(f"Bitti! Toplam {count} adet yeni, tertemiz malzeme ayrıştırıldı ve bağlandı.")
    print(f"Temizlenen eski kirli malzeme sayısı: {deleted_count}")
