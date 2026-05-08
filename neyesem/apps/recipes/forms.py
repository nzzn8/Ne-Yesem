from django import forms
from .models import Recipe, RecipeComment


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
            # Template pill butonlarıyla yönetildiği için hidden; sunucu tarafında choices doğrulaması aktif
            'difficulty': forms.HiddenInput(),
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

class RecipeCommentForm(forms.ModelForm):
    class Meta:
        model = RecipeComment
        fields = ['text', 'rating']
        labels = {
            'text': '',
            'rating': 'Puan (1-5)'
        }
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Bu tarif hakkında ne düşünüyorsunuz?', 'rows': 3, 'class': 'form-control', 'style': 'width: 100%; border-radius: 12px; padding: 15px; border: 1px solid #e2e8f0; margin-bottom: 15px;'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control', 'style': 'width: 100px; display: inline-block; border-radius: 8px; border: 1px solid #e2e8f0; padding: 8px; margin-left: 10px;'})
        }
