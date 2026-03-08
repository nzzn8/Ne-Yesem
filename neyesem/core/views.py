from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(username, password)

        return redirect("/account/")

    return render(request, "login.html")

def account(request):
    return render(request, "account.html")

from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(username, password)

        return redirect("/account/")

    return render(request, "login.html")

def account(request):
    return render(request, "account.html")

def iletisim(request):
    if request.method == "POST":
        ad = request.POST.get("ad")
        email = request.POST.get("email")
        mesaj = request.POST.get("mesaj")

        print("Ad:", ad)
        print("Email:", email)
        print("Mesaj:", mesaj)

        return render(request, "iletisim.html", {"basarili": True})

    return render(request, "iletisim.html")

from django.shortcuts import redirect

def logout_view(request):
    return redirect("/")