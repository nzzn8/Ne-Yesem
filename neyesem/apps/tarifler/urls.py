from django.urls import path
from . import views

app_name = 'tarifler'

urlpatterns = [
    path('',                         views.TarifListesiView.as_view(),  name='liste'),
    path('ekle/',                    views.TarifEkleView.as_view(),     name='ekle'),
    path('<int:pk>/',                views.TarifDetayView.as_view(),    name='detay'),
    path('<int:pk>/duzenle/',        views.TarifDuzenleView.as_view(),  name='duzenle'),
    path('<int:pk>/sil/',            views.TarifSilView.as_view(),      name='sil'),
    path('api/malzeme-onerileri/',   views.malzeme_onerileri,           name='malzeme_onerileri'),
]
