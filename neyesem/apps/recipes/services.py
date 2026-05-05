from .models import Ingredient, RecipeIngredient


def sync_recipe_ingredients(recipe, names: list, quantities: list) -> None:
    """
    Tarifin malzemelerini sıfırdan yazar.
    Hem create hem update akışlarından çağrılır — DRY prensibi.
    """
    recipe.recipe_ingredients.all().delete()
    pairs = [
        (name.strip(), qty.strip())
        for name, qty in zip(names, quantities)
        if name.strip()
    ]
    for name, qty in pairs:
        ingredient, _ = Ingredient.objects.get_or_create(name=name)
        RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            quantity_text=qty,
        )
