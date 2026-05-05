from django import forms


class ContactForm(forms.Form):
    ad = forms.CharField(
        label='Ad Soyad',
        widget=forms.TextInput(attrs={'placeholder': 'Örn: Ahmet Yılmaz'}),
    )
    email = forms.EmailField(
        label='E-posta',
        widget=forms.EmailInput(attrs={'placeholder': 'Örn: ahmet@ornek.com'}),
    )
    mesaj = forms.CharField(
        label='Mesaj',
        widget=forms.Textarea(attrs={'rows': 6, 'placeholder': 'Mesajınızı buraya yazın...'}),
    )
