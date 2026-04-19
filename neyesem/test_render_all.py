import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "neyesem.settings")
django.setup()
from django.conf import settings
settings.ALLOWED_HOSTS = ['*']
from django.test import Client
from django.contrib.auth.models import User
from core.models import Recipe

c = Client()
try:
    user, _ = User.objects.get_or_create(username='testuser')
    c.force_login(user)
    urls = ['/', '/tarifler/', '/account/favorites/', '/account/my-recipes/', '/tarif/ekle/']
    
    recipe = Recipe.objects.first()
    if recipe:
        urls.append(f'/tarif/{recipe.id}/')
        urls.append(f'/tarif/{recipe.id}/duzenle/')
        urls.append(f'/tarif/{recipe.id}/sil/')
        
    for url in urls:
        response = c.get(url)
        if response.status_code not in [200, 302]:
            print(f"FAILED {url} - Status: {response.status_code}")
        else:
            print(f"SUCCESS {url} - Status: {response.status_code}")
except Exception as e:
    import traceback
    traceback.print_exc()
