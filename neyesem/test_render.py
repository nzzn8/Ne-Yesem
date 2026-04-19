import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "neyesem.settings")
django.setup()
from django.conf import settings
settings.ALLOWED_HOSTS = ['*']
from django.test import Client
from django.contrib.auth.models import User
c = Client()
try:
    user, _ = User.objects.get_or_create(username='testuser')
    c.force_login(user)
    print("FAVORITES:", c.get('/account/favorites/').status_code)
    print("MY_RECIPES:", c.get('/account/my-recipes/').status_code)
except Exception as e:
    import traceback
    traceback.print_exc()
