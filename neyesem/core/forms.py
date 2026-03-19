from django import forms
from django.contrib.auth.models import User
from .models import Profile, Recipe

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Adınız',
            'last_name': 'Soyadınız',
            'email': 'E-posta Adresiniz'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Örn: Ahmet'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Örn: Yılmaz'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Örn: ahmet@ornek.com'})
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'newsletter']
        labels = {
            'avatar': 'Profil Fotoğrafı',
            'newsletter': 'Bülten ve bildirimleri almak istiyorum'
        }

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'prep_time', 'difficulty', 'description', 'image_url']
        labels = {
            'title': 'Tarif Adı',
            'prep_time': 'Hazırlanma Süresi',
            'difficulty': 'Zorluk Derecesi',
            'description': 'Kısa Açıklama',
            'image_url': 'Resim Bağlantısı (URL)'
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Örn: Fırın Sütlaç'}),
            'prep_time': forms.TextInput(attrs={'placeholder': 'Örn: 45 dk'}),
            'difficulty': forms.TextInput(attrs={'placeholder': 'Örn: Orta'}),
            'description': forms.Textarea(attrs={'placeholder': 'Tarifinizin püf noktalarını kısaca anlatın...', 'rows': 4}),
            'image_url': forms.URLInput(attrs={'placeholder': 'https://unsplash.com/...' })
        }
