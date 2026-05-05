from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Malzeme Adı")

    class Meta:
        verbose_name = "Malzeme"
        verbose_name_plural = "Malzemeler"
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tarif Adı")
    prep_time = models.CharField(max_length=50, verbose_name="Hazırlanma Süresi")
    difficulty = models.CharField(max_length=50, verbose_name="Zorluk Derecesi")
    description = models.TextField(verbose_name="Kısa Açıklama")
    ingredient_list = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        blank=True,
        verbose_name="Malzemeler",
    )
    instructions = models.TextField(
        verbose_name="Hazırlanışı",
        help_text="Adımları sırasıyla alt alta yazın.",
        blank=True,
        null=True,
    )
    servings = models.CharField(max_length=50, verbose_name="Kaç Kişilik", blank=True, null=True)
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True,
        verbose_name="Kapak Fotoğrafı",
    )
    image_url = models.URLField(blank=True, null=True, verbose_name="Resim URL")
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name="Yazar",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tarif"
        verbose_name_plural = "Tarifler"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', '-created_at']),
        ]

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recipe_ingredients')
    quantity_text = models.CharField(
        max_length=100,
        verbose_name="Miktar/Birim",
        blank=True,
        null=True,
        help_text="Örn: 2 diş, 500 gram, 1 yemek kaşığı",
    )

    class Meta:
        verbose_name = "Tarif Malzemesi"
        verbose_name_plural = "Tarif Malzemeleri"

    def __str__(self):
        if self.quantity_text:
            return f"{self.quantity_text} {self.ingredient.name}"
        return self.ingredient.name
