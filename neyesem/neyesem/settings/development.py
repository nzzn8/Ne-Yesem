from .base import *

DEBUG = True

SECRET_KEY = 'django-insecure-dev-only-key-degistir'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Safari dahil tüm tarayıcılarda localhost CSRF sorununu önler (Django 4.0+)
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://localhost:8000']

# Geliştirme ortamında e-postalar terminale yazdırılır
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'Ne Yesem <noreply@neyesem.local>'
