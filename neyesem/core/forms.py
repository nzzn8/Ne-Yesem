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
        fields = ['title', 'prep_time', 'difficulty', 'servings', 'description', 'ingredients', 'instructions', 'image_url']
        labels = {
            'title': 'Tarif Adı',
            'prep_time': 'Hazırlanma Süresi',
            'difficulty': 'Zorluk Derecesi',
            'servings': 'Kaç Kişilik',
            'description': 'Kısa Açıklama',
            'ingredients': 'Malzemeler',
            'instructions': 'Hazırlanışı',
            'image_url': 'Resim Bağlantısı (URL)'
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Örn: Fırın Sütlaç'}),
            'prep_time': forms.TextInput(attrs={'placeholder': 'Örn: 45 dk'}),
            'difficulty': forms.TextInput(attrs={'placeholder': 'Örn: Orta'}),
            'servings': forms.TextInput(attrs={'placeholder': 'Örn: 4-6 Kişilik'}),
            'description': forms.Textarea(attrs={'placeholder': 'Tarifinizin püf noktalarını kısaca anlatın...', 'rows': 3}),
            'ingredients': forms.Textarea(attrs={'placeholder': 'Malzemeleri alt alta yazın.\nÖrn:\n2 su bardağı pirinç\n3 yemek kaşığı tereyağı', 'rows': 5}),
            'instructions': forms.Textarea(attrs={'placeholder': 'Adımları alt alta yazın.\nÖrn:\n1. Pirinçleri yıkayın.\n2. Tereyağını eritin.', 'rows': 6}),
            'image_url': forms.URLInput(attrs={'placeholder': 'https://unsplash.com/...' })
        }
