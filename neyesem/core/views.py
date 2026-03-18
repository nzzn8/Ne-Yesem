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
        {"ad": "Mercimek Çorbası", "sure": "30 dk", "zorluk": "Kolay", "aciklama": "Az malzemeyle hazırlayabileceğiniz içinizi ısıtacak klasik lezzet. Havuç, soğan ve mercimeğin mükemmel uyumu."},
        {"ad": "Karnıyarık", "sure": "60 dk", "zorluk": "Orta", "aciklama": "Patlıcan ve kıymanın nefis birlikteliği. Özel akşam yemekleri için sofranın yıldızı."},
        {"ad": "Zeytinyağlı Taze Fasulye", "sure": "45 dk", "zorluk": "Kolay", "aciklama": "Hafif ve sağlıklı, yaz sofralarının vazgeçilmez zeytinyağlı klasiği."},
        {"ad": "Kuru Fasulye & Pilav", "sure": "90 dk", "zorluk": "Orta", "aciklama": "Geleneksel Türk mutfağının ayrılmaz ikilisi, tam bir protein deposu ev yemeği."},
        {"ad": "Tavuklu Sebzeli Erişte", "sure": "25 dk", "zorluk": "Kolay", "aciklama": "Evinizdeki mevsim sebzeleriyle rahatça zenginleştirebileceğiniz, hızlı ve doyurucu bir öğün."},
        {"ad": "Zerdeçallı Pirinç Pilavı", "sure": "30 dk", "zorluk": "Kolay", "aciklama": "Hem rengiyle göze, hem aromasıyla damağa hitap eden, farklılık arayanlara şık pilav."},
        {"ad": "Pratik Bezelye Yemeği", "sure": "35 dk", "zorluk": "Kolay", "aciklama": "Havuç ve patatesle zenginleşen, ev malzemeleriyle şipşak hazırlanan sulu yemek."},
        {"ad": "Şakşuka", "sure": "40 dk", "zorluk": "Orta", "aciklama": "Küçük doğranıp kızarmış sebzelerin nefis domates sosuyla buluştuğu meze veya garnitür."},
        {"ad": "Ev Yapımı Çıtır Patates", "sure": "45 dk", "zorluk": "Kolay", "aciklama": "Fırında az yağ ile hazırlanan, dışı çıtır içi yumuşacık sağlıklı atıştırmalık."},
        {"ad": "Humuslu Tavuk Köftesi", "sure": "40 dk", "zorluk": "Orta", "aciklama": "Yüksek proteinli, nohut ezmesi ve tavuğun bir araya geldiği yenilikçi fit tarif."}
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