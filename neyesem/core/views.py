from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from .models import Profile, Recipe, Ingredient, RecipeIngredient
from .forms import UserUpdateForm, ProfileUpdateForm, RecipeForm

def home(request):
    return render(request, "home.html")

def login_view(request):
    hata = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/account/")
        else:
            hata = "Kullanıcı adı veya şifre yanlış."

    return render(request, "login.html", {"hata": hata})

def register_view(request):
    hata = ""

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            hata = "Şifreler eşleşmiyor."
        elif User.objects.filter(username=username).exists():
            hata = "Bu kullanıcı adı zaten alınmış."
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            login(request, user)
            return redirect("/account/")

    return render(request, "register.html", {"hata": hata})

class AccountProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['u_form'] = UserUpdateForm(instance=self.request.user)
        context['p_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        context['active_tab'] = 'profile'
        return context

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # Using request.FILES to capture uploaded avatars
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profiliniz başarıyla güncellendi!')
            return redirect('account_profile')
        
        context = self.get_context_data()
        context.update({'u_form': u_form, 'p_form': p_form})
        return self.render_to_response(context)

class AccountSecurityView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'account/security.html'
    success_url = reverse_lazy('account_security')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'security'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Şifreniz başarıyla değiştirildi! Yeni şifrenizle devam edebilirsiniz.')
        return super().form_valid(form)

class AccountFavoritesView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'account/favorites.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return self.request.user.profile.favorites.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'favorites'
        return context

class AccountMyRecipesView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'account/my_recipes.html'
    context_object_name = 'my_recipes'

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'my_recipes'
        return context

def logout_view(request):
    logout(request)
    return redirect("/")

def tarifler(request, ingredient_name=None):
    recipes = Recipe.objects.all().order_by('-created_at')
    
    query = request.GET.get('q')
    if query:
        # Virgülle ayrılmış çoklu malzeme veya tek arama için (örn: "tavuk, mantar")
        query_parts = [part.strip() for part in query.split(',') if part.strip()]
        
        for part in query_parts:
            recipes = recipes.filter(
                models.Q(title__icontains=part) | 
                models.Q(recipe_ingredients__ingredient__name__icontains=part)
            )
        recipes = recipes.distinct()

    if ingredient_name:
        recipes = recipes.filter(recipe_ingredients__ingredient__name__iexact=ingredient_name)

    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = list(request.user.profile.favorites.values_list('id', flat=True))
        
    return render(request, "tarifler.html", {
        "recipes": recipes, 
        "user_favorites": user_favorites,
        "search_query": query,
        "selected_ingredient": ingredient_name
    })

@login_required
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

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_favorited = False
        if self.request.user.is_authenticated:
            is_favorited = self.object in self.request.user.profile.favorites.all()
        context['is_favorited'] = is_favorited
        return context

def iletisim(request):
    basarili = False

    if request.method == "POST":
        ad = request.POST.get("ad")
        email = request.POST.get("email")
        mesaj = request.POST.get("mesaj")

        print("Ad:", ad)
        print("Email:", email)
        print("Mesaj:", mesaj)

        basarili = True

    return render(request, "iletisim.html", {"basarili": basarili})

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe_form.html'
    success_url = reverse_lazy('account_my_recipes')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        
        ingredient_names = self.request.POST.getlist('ingredient_name[]')
        ingredient_quantities = self.request.POST.getlist('ingredient_quantity[]')
        
        for name, quantity in zip(ingredient_names, ingredient_quantities):
            name = name.strip()
            if name:
                ingredient, _ = Ingredient.objects.get_or_create(name=name)
                RecipeIngredient.objects.create(
                    recipe=self.object,
                    ingredient=ingredient,
                    quantity_text=quantity.strip()
                )
        messages.success(self.request, 'Tarifiniz başarıyla eklendi!')
        return response

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe_form.html'
    success_url = reverse_lazy('account_my_recipes')

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        
        self.object.recipe_ingredients.all().delete()
        
        ingredient_names = self.request.POST.getlist('ingredient_name[]')
        ingredient_quantities = self.request.POST.getlist('ingredient_quantity[]')
        
        for name, quantity in zip(ingredient_names, ingredient_quantities):
            name = name.strip()
            if name:
                ingredient, _ = Ingredient.objects.get_or_create(name=name)
                RecipeIngredient.objects.create(
                    recipe=self.object,
                    ingredient=ingredient,
                    quantity_text=quantity.strip()
                )
        messages.success(self.request, 'Tarifiniz başarıyla güncellendi!')
        return response

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'recipe_confirm_delete.html'
    success_url = reverse_lazy('account_my_recipes')

    def test_func(self):
        return self.get_object().author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Tarifiniz silindi.')
        return super().delete(request, *args, **kwargs)