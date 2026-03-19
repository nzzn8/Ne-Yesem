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

def tarifler(request):
    recipes = [
        {"ad": "Mercimek Çorbası", "sure": "30 dk", "zorluk": "Kolay", "aciklama": "Az malzemeyle hazırlayabileceğiniz içinizi ısıtacak klasik lezzet. Havuç, soğan ve mercimeğin mükemmel uyumu.", "resim": "https://images.unsplash.com/photo-1547592180-85f1ddce0939?auto=format&fit=crop&w=600&q=80"},
        {"ad": "Karnıyarık", "sure": "60 dk", "zorluk": "Orta", "aciklama": "Patlıcan ve kıymanın nefis birlikteliği. Özel akşam yemekleri için sofranın yıldızı.", "resim": "https://images.unsplash.com/photo-1565557612-402c481d6f21?auto=format&fit=crop&w=600&q=80"},
        {"ad": "Zeytinyağlı Taze Fasulye", "sure": "45 dk", "zorluk": "Kolay", "aciklama": "Hafif ve sağlıklı, yaz sofralarının vazgeçilmez zeytinyağlı klasiği.", "resim": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&q=80"},
        {"ad": "Kuru Fasulye & Pilav", "sure": "90 dk", "zorluk": "Orta", "aciklama": "Geleneksel Türk mutfağının ayrılmaz ikilisi, tam bir protein deposu ev yemeği.", "resim": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=600&q=80"},
        {"ad": "Tavuklu Sebzeli Erişte", "sure": "25 dk", "zorluk": "Kolay", "aciklama": "Evinizdeki mevsim sebzeleriyle rahatça zenginleştirebileceğiniz, hızlı ve doyurucu bir öğün.", "resim": "https://images.unsplash.com/photo-1612929633738-8fe44f73c9ee?auto=format&fit=crop&w=600&q=80"},
        {"ad": "Zerdeçallı Pirinç Pilavı", "sure": "30 dk", "zorluk": "Kolay", "aciklama": "Hem rengiyle göze, hem aromasıyla damağa hitap eden, farklılık arayanlara şık pilav.", "resim": "https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?auto=format&fit=crop&w=600&q=80"},
        {"ad": "Pratik Bezelye Yemeği", "sure": "35 dk", "zorluk": "Kolay", "aciklama": "Havuç ve patatesle zenginleşen, ev malzemeleriyle şipşak hazırlanan sulu yemek.", "resim": "https://images.unsplash.com/photo-1534422298391-e4f8c871ce52?auto=format&fit=crop&w=600&q=80"},
        {"ad": "Şakşuka", "sure": "40 dk", "zorluk": "Orta", "aciklama": "Küçük doğranıp kızarmış sebzelerin nefis domates sosuyla buluştuğu meze veya garnitür.", "resim": "https://images.unsplash.com/photo-1560684352-84978115bd6f?auto=format&fit=crop&w=600&q=80"},
        {"ad": "Ev Yapımı Çıtır Patates", "sure": "45 dk", "zorluk": "Kolay", "aciklama": "Fırında az yağ ile hazırlanan, dışı çıtır içi yumuşacık sağlıklı atıştırmalık.", "resim": "https://images.unsplash.com/photo-1576107232684-1279f390859f?auto=format&fit=crop&w=600&q=80"},
        {"ad": "Humuslu Tavuk Köftesi", "sure": "40 dk", "zorluk": "Orta", "aciklama": "Yüksek proteinli, nohut ezmesi ve tavuğun bir araya geldiği yenilikçi fit tarif.", "resim": "https://images.unsplash.com/photo-1529042410756-b186b86b4f74?auto=format&fit=crop&w=600&q=80"}
    ]
    return render(request, "tarifler.html", {"recipes": recipes})

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