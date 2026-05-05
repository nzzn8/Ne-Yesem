from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .forms import ContactForm


def iletisim(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        send_mail(
            subject=f"Ne Yesem İletişim: {form.cleaned_data['ad']}",
            message=form.cleaned_data['mesaj'],
            from_email=form.cleaned_data['email'],
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        messages.success(request, 'Mesajınız iletildi, teşekkürler!')
        return redirect('contact:iletisim')
    return render(request, 'contact/iletisim.html', {'form': form})
