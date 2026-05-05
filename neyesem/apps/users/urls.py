from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('giris/', views.login_view, name='login'),
    path('kayit/', views.register_view, name='register'),
    path('cikis/', views.logout_view, name='logout'),
    path('account/', views.AccountProfileView.as_view(), name='account_profile'),
    path('account/guvenlik/', views.AccountSecurityView.as_view(), name='account_security'),
    path('account/favoriler/', views.AccountFavoritesView.as_view(), name='account_favorites'),
    path('account/tariflerim/', views.AccountMyRecipesView.as_view(), name='account_my_recipes'),

    path(
        'sifre-sifirla/',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html',
            email_template_name='users/password_reset_email.html',
        ),
        name='password_reset',
    ),
    path(
        'sifre-sifirla/gonderildi/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'sifre-sifirla/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
        ),
        name='password_reset_confirm',
    ),
    path(
        'sifre-sifirla/tamamlandi/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]
