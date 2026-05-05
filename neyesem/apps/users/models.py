from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(
        upload_to='avatars/',
        default='default_avatar.png',
        blank=True,
        null=True,
        verbose_name="Profil Fotoğrafı",
    )
    newsletter = models.BooleanField(default=True, verbose_name="Bülten Bildirimleri")
    favorites = models.ManyToManyField(
        'recipes.Recipe',
        related_name='favorited_by',
        blank=True,
    )

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profiller"

    def __str__(self):
        return f"{self.user.username} Profili"
