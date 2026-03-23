from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from .models import Profile, Recipe
from .forms import UserUpdateForm, ProfileUpdateForm

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

def tarifler(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = list(request.user.profile.favorites.values_list('id', flat=True))
    return render(request, "tarifler.html", {"recipes": recipes, "user_favorites": user_favorites})

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