from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('tarifler/', views.RecipeListView.as_view(), name='list'),
    path('malzeme/<str:ingredient_name>/', views.RecipeListView.as_view(), name='by_ingredient'),
    path('tarif/ekle/', views.RecipeCreateView.as_view(), name='create'),
    path('tarif/<int:pk>/', views.RecipeDetailView.as_view(), name='detail'),
    path('tarif/<int:pk>/duzenle/', views.RecipeUpdateView.as_view(), name='update'),
    path('tarif/<int:pk>/sil/', views.RecipeDeleteView.as_view(), name='delete'),
    path('tarif/<int:recipe_id>/favori/', views.toggle_favorite, name='toggle_favorite'),
]
