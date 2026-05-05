from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('apps.users.urls', namespace='users')),
    path('', include('apps.recipes.urls', namespace='recipes')),
    path('', include('apps.contact.urls', namespace='contact')),
    path('yonetim/tarifler/', include('apps.tarifler.urls', namespace='tarifler')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
