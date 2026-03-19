from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tarif Adı")
    prep_time = models.CharField(max_length=50, verbose_name="Hazırlanma Süresi")
    difficulty = models.CharField(max_length=50, verbose_name="Zorluk Derecesi")
    description = models.TextField(verbose_name="Kısa Açıklama")
    image_url = models.URLField(blank=True, null=True, verbose_name="Resim URL")
    author = models.ForeignKey(User, related_name='recipes', on_delete=models.CASCADE, verbose_name="Yazar", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', default='default_avatar.png', blank=True, null=True, verbose_name="Profil Fotoğrafı")
    newsletter = models.BooleanField(default=True, verbose_name="Bülten Bildirimleri")
    favorites = models.ManyToManyField(Recipe, related_name='favorited_by', blank=True)

    def __str__(self):
        return f"{self.user.username} Profili"

# Signaller sayesinde yeni User kaydedildiğinde otomatik Profile oluşturulur
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
