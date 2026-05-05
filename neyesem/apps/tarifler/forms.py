from django import forms
from .models import Tarif, Kategori


class TarifForm(forms.ModelForm):
    class Meta:
        model = Tarif
        fields = [
            'baslik', 'kategori', 'hazirlanma_suresi', 'zorluk',
            'porsiyon', 'aciklama', 'talimatlar', 'resim', 'resim_url',
        ]
        labels = {
            'baslik':            'Tarif Başlığı',
            'kategori':          'Kategori',
            'hazirlanma_suresi': 'Hazırlanma Süresi',
            'zorluk':            'Zorluk Derecesi',
            'porsiyon':          'Kaç Kişilik',
            'aciklama':          'Kısa Açıklama',
            'talimatlar':        'Hazırlanışı',
            'resim':             'Kapak Fotoğrafı',
            'resim_url':         'Resim URL',
        }
        widgets = {
            'zorluk':     forms.HiddenInput(),
            'aciklama':   forms.Textarea(attrs={
                'rows': 3, 'placeholder': 'Tarifinizi kısaca tanıtın...',
            }),
            'talimatlar': forms.Textarea(attrs={
                'rows': 6, 'placeholder': 'Adımları alt alta yazın...',
            }),
            'baslik':            forms.TextInput(attrs={'placeholder': 'Örn: Fırın Sütlaç'}),
            'hazirlanma_suresi': forms.TextInput(attrs={'placeholder': 'Örn: 45 dk'}),
            'porsiyon':          forms.TextInput(attrs={'placeholder': 'Örn: 4-6 Kişilik'}),
            'resim_url':         forms.URLInput(attrs={'placeholder': 'https://...'}),
        }
