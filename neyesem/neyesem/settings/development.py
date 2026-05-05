from .base import *

DEBUG = True

SECRET_KEY = 'django-insecure-dev-only-key-degistir'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Geliştirme ortamında e-postalar terminale yazdırılır
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'Ne Yesem <noreply@neyesem.local>'
