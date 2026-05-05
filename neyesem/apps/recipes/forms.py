from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'prep_time', 'difficulty', 'servings', 'description', 'instructions', 'image', 'image_url']
        labels = {
            'title': 'Tarif Adı',
            'prep_time': 'Hazırlanma Süresi',
            'difficulty': 'Zorluk Derecesi',
            'servings': 'Kaç Kişilik',
            'description': 'Kısa Açıklama',
            'instructions': 'Hazırlanışı',
            'image': 'Kapak Fotoğrafı (Dosya Seçin)',
            'image_url': 'Veya Resim Bağlantısı (URL)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Örn: Fırın Sütlaç'}),
            'prep_time': forms.TextInput(attrs={'placeholder': 'Örn: 45 dk'}),
            'difficulty': forms.TextInput(attrs={'placeholder': 'Örn: Orta'}),
            'servings': forms.TextInput(attrs={'placeholder': 'Örn: 4-6 Kişilik'}),
            'description': forms.Textarea(attrs={
                'placeholder': 'Tarifinizin püf noktalarını kısaca anlatın...',
                'rows': 3,
            }),
            'instructions': forms.Textarea(attrs={
                'placeholder': 'Adımları alt alta yazın.\nÖrn:\n1. Pirinçleri yıkayın.\n2. Tereyağını eritin.',
                'rows': 6,
            }),
            'image_url': forms.URLInput(attrs={'placeholder': 'https://...'}),
        }
