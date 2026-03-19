from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("account/", views.AccountProfileView.as_view(), name="account_profile"),
    path("account/security/", views.AccountSecurityView.as_view(), name="account_security"),
    path("account/favorites/", views.AccountFavoritesView.as_view(), name="account_favorites"),
    path("account/my-recipes/", views.AccountMyRecipesView.as_view(), name="account_my_recipes"),
    path("logout/", views.logout_view, name="logout"),
    path("iletisim/", views.iletisim, name="iletisim"),
    path("tarifler/", views.tarifler, name="tarifler"),

    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset.html",
            email_template_name="password_reset_email.html",
            extra_email_context={'domain': '127.0.0.1:8000', 'site_name': 'Ne Yesem'}
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]