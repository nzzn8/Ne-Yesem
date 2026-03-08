from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("account/", views.account, name="account"),
    path("logout/", views.logout_view, name="logout"),
    path("iletisim/", views.iletisim, name="iletisim"),
    ]

