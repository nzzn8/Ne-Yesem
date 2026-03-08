from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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

def account(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    return render(request, "account.html")

def logout_view(request):
    logout(request)
    return redirect("/")

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