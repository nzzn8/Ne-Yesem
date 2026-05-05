from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Kullanıcı Adı',
        widget=forms.TextInput(attrs={'placeholder': 'Örn: ahmet_chef'}),
    )
    password = forms.CharField(
        label='Şifre',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='Kullanıcı Adı',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Örn: yemekavcisi'}),
    )
    email = forms.EmailField(
        label='E-posta Adresi',
        widget=forms.EmailInput(attrs={'placeholder': 'Örn: ahmet@ornek.com'}),
    )
    password = forms.CharField(
        label='Şifre',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
    )
    password2 = forms.CharField(
        label='Şifre Tekrar',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Bu kullanıcı adı zaten alınmış.')
        return username

    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('password2'):
            raise forms.ValidationError('Şifreler eşleşmiyor.')
        return data


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Adınız',
            'last_name': 'Soyadınız',
            'email': 'E-posta Adresiniz',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Örn: Ahmet'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Örn: Yılmaz'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Örn: ahmet@ornek.com'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'newsletter']
        labels = {
            'avatar': 'Profil Fotoğrafı',
            'newsletter': 'Bülten ve bildirimleri almak istiyorum',
        }
