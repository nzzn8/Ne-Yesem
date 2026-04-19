from core.models import Recipe, Ingredient

recipes = Recipe.objects.all()
for recipe in recipes:
    if recipe.ingredients:
        lines = recipe.ingredients.splitlines()
        for line in lines:
            name = line.strip()
            # Basic cleanup: if they used dashes or stars
            if name.startswith('-'):
                name = name[1:].strip()
            if name.startswith('*'):
                name = name[1:].strip()
                
            if name:
                # lowercase for consistency, but keep first letter capital maybe? Let's just use exact or title
                name = name.title()
                ing, created = Ingredient.objects.get_or_create(name=name)
                recipe.ingredient_list.add(ing)
        print(f"Migrated ingredients for {recipe.title}")
print("Done!")
