from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('account/', views.account, name='account'),
    path('iletisim/', views.iletisim, name='iletisim'),
    path('logout/', views.logout_view, name='logout'),
]


