import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neyesem.settings')
django.setup()

from core.models import Recipe, Ingredient, RecipeIngredient

# Clear existing intermediate relationships just in case
RecipeIngredient.objects.all().delete()

def parse_ingredient_line(line):
    line = line.strip()
    if line.startswith('-') or line.startswith('*'):
         line = line[1:].strip()
         
    units = ["gram", "gr", "kg", "kilogram", "diş", "demet", "adet", "paket", "tatlı", "yemek", "çay", "su", "bardak", "bardağı", "kaşık", "kaşığı", "litre", "ml", "avuç", "tutam", "dilim", "yarım", "çeyrek"]
    
    parts = line.split()
    quantity_parts = []
    name_parts = []
    
    parsing_qty = True
    for part in parts:
        lower_part = part.lower()
        has_digit = any(char.isdigit() for char in part)
        is_unit = lower_part in units
        
        # If it's a number, or a recognized unit, and we're still parsing the beginning of the string
        if parsing_qty and (has_digit or is_unit):
            quantity_parts.append(part)
        else:
            parsing_qty = False
            name_parts.append(part)
            
    quantity = " ".join(quantity_parts)
    name = " ".join(name_parts)
    
    # Fallback if no text is found after parsing quantity
    if not name:
        name = quantity
        quantity = ""
        
    return quantity, name.title()

count = 0
for recipe in Recipe.objects.all():
    if recipe.ingredients:
        for line in recipe.ingredients.splitlines():
            if not line.strip(): continue
            qty, name = parse_ingredient_line(line)
            
            # Create or get ingredient
            ing, _ = Ingredient.objects.get_or_create(name=name)
            
            # Create through model
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ing, quantity_text=qty)
            count += 1

print(f"Migrated {count} ingredients into RecipeIngredient model successfully!")
