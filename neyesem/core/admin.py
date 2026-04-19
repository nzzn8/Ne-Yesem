from django.contrib import admin
from .models import Recipe, Profile, Ingredient, RecipeIngredient

admin.site.register(Ingredient)
admin.site.register(Profile)

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    inlines = [RecipeIngredientInline]
