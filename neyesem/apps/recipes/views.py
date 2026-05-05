from django.shortcuts import render, get_object_or_404
from django.db import models as db_models
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Recipe, Ingredient
from .forms import RecipeForm
from .services import sync_recipe_ingredients


def ingredient_autocomplete(request):
    q = request.GET.get('q', '').strip()
    if not q:
        # Fokus anında en çok kullanılan 8 malzemeyi döndür
        results = list(
            Ingredient.objects
            .annotate(usage=db_models.Count('recipe_ingredients'))
            .order_by('-usage', 'name')
            .values_list('name', flat=True)[:8]
        )
        return JsonResponse({'results': results, 'popular': True})
    if len(q) < 2:
        return JsonResponse({'results': [], 'popular': False})
    results = list(
        Ingredient.objects
        .filter(name__icontains=q)
        .order_by('name')
        .values_list('name', flat=True)[:12]
    )
    return JsonResponse({'results': results, 'popular': False})


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        qs = (
            Recipe.objects
            .select_related('author')
            .prefetch_related('recipe_ingredients__ingredient')
        )

        ingredient_name = self.kwargs.get('ingredient_name')
        if ingredient_name:
            qs = qs.filter(recipe_ingredients__ingredient__name__iexact=ingredient_name)

        query = self.request.GET.get('q')
        if query:
            parts = [p.strip() for p in query.split(',') if p.strip()]
            for part in parts:
                qs = qs.filter(
                    db_models.Q(title__icontains=part) |
                    db_models.Q(recipe_ingredients__ingredient__name__icontains=part)
                )
            qs = qs.distinct()

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_ingredient'] = self.kwargs.get('ingredient_name')
        context['user_favorites'] = []
        if self.request.user.is_authenticated:
            context['user_favorites'] = list(
                self.request.user.profile.favorites.values_list('id', flat=True)
            )
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        return Recipe.objects.prefetch_related('recipe_ingredients__ingredient')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_favorited = False
        if self.request.user.is_authenticated:
            is_favorited = self.object in self.request.user.profile.favorites.all()
        context['is_favorited'] = is_favorited
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/form.html'
    success_url = reverse_lazy('users:account_my_recipes')
    login_url = 'users:login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        sync_recipe_ingredients(
            recipe=self.object,
            names=self.request.POST.getlist('ingredient_name[]'),
            quantities=self.request.POST.getlist('ingredient_quantity[]'),
        )
        messages.success(self.request, 'Tarifiniz başarıyla eklendi!')
        return response


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/form.html'
    success_url = reverse_lazy('users:account_my_recipes')
    login_url = 'users:login'

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        sync_recipe_ingredients(
            recipe=self.object,
            names=self.request.POST.getlist('ingredient_name[]'),
            quantities=self.request.POST.getlist('ingredient_quantity[]'),
        )
        messages.success(self.request, 'Tarifiniz başarıyla güncellendi!')
        return response


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/confirm_delete.html'
    success_url = reverse_lazy('users:account_my_recipes')
    login_url = 'users:login'

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Tarifiniz silindi.')
        return super().form_valid(form)


@login_required(login_url='users:login')
@require_POST
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    profile = request.user.profile
    if recipe in profile.favorites.all():
        profile.favorites.remove(recipe)
        is_favorited = False
    else:
        profile.favorites.add(recipe)
        is_favorited = True
    return JsonResponse({'is_favorited': is_favorited})
