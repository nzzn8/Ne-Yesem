from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from django.contrib import messages

from apps.recipes.models import Recipe
from .forms import LoginForm, RegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', 'users:account_profile'))
        form.add_error(None, 'Kullanıcı adı veya şifre yanlış.')
    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        from django.contrib.auth.models import User
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )
        login(request, user)
        return redirect('users:account_profile')
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


class AccountProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/account/profile.html'
    login_url = 'users:login'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            Profile.objects.get_or_create(user=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['u_form'] = UserUpdateForm(instance=self.request.user)
        context['p_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        context['active_tab'] = 'profile'
        return context

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profiliniz başarıyla güncellendi!')
            return redirect('users:account_profile')
        context = self.get_context_data()
        context.update({'u_form': u_form, 'p_form': p_form})
        return self.render_to_response(context)


class AccountSecurityView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/account/security.html'
    success_url = reverse_lazy('users:account_security')
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'security'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Şifreniz başarıyla değiştirildi!')
        return super().form_valid(form)


class AccountFavoritesView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'users/account/favorites.html'
    context_object_name = 'favorites'
    login_url = 'users:login'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            Profile.objects.get_or_create(user=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return (
            self.request.user.profile.favorites
            .select_related('author')
            .order_by('-created_at')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'favorites'
        return context


class AccountMyRecipesView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'users/account/my_recipes.html'
    context_object_name = 'my_recipes'
    login_url = 'users:login'

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'my_recipes'
        return context
