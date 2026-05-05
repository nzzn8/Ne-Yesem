from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.recipes.models import Recipe, Ingredient, RecipeIngredient


RECIPES = [
    {
        'title': 'Fırın Sütlaç',
        'prep_time': '50 dk',
        'difficulty': 'Kolay',
        'servings': '6 Kişilik',
        'description': 'Fırında kızarmış klasik Türk sütlacı. Kremsi dokusu ve enfes aromasıyla sofraların vazgeçilmezi.',
        'instructions': (
            'Pirinçleri yıkayıp 30 dakika suda bekletin.\n'
            'Süt ile pirinçleri orta ateşte, sürekli karıştırarak pişirin.\n'
            'Pirinçler yumuşayınca şeker ve vanilyayı ekleyin.\n'
            'Koyulaşan karışımı fırın kaplarına dökün.\n'
            'Önceden ısıtılmış 200°C fırında üzeri kızarana kadar pişirin.'
        ),
        'image_url': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=800&q=80',
        'ingredients': [
            ('Pirinç', '1 su bardağı'),
            ('Süt', '1 litre'),
            ('Şeker', '1 su bardağı'),
            ('Vanilya', '1 paket'),
            ('Nişasta', '2 yemek kaşığı'),
        ],
    },
    {
        'title': 'Mercimek Çorbası',
        'prep_time': '35 dk',
        'difficulty': 'Kolay',
        'servings': '4 Kişilik',
        'description': 'Sıcacık ve doyurucu kırmızı mercimek çorbası. Limon ve kırmızı biberle servis edilir.',
        'instructions': (
            'Soğan ve havucu yağda kavurun.\n'
            'Yıkanan mercimekleri ve sıcak suyu ekleyin.\n'
            'Tuz, kimyon ve zerdeçalı ilave edip 25 dakika pişirin.\n'
            'Blender ile pürüzsüz hale getirin.\n'
            'Tereyağında kırmızı biber ve nane kavurarak üzerine dökün.'
        ),
        'image_url': 'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=800&q=80',
        'ingredients': [
            ('Kırmızı Mercimek', '2 su bardağı'),
            ('Soğan', '1 adet'),
            ('Havuç', '1 adet'),
            ('Tereyağı', '2 yemek kaşığı'),
            ('Kimyon', '1 tatlı kaşığı'),
            ('Kırmızı Biber', '1 tatlı kaşığı'),
        ],
    },
    {
        'title': 'Karnıyarık',
        'prep_time': '60 dk',
        'difficulty': 'Orta',
        'servings': '4 Kişilik',
        'description': 'Kıymalı iç harcıyla doldurulmuş, fırında pişirilmiş geleneksel patlıcan yemeği.',
        'instructions': (
            'Patlıcanları soyup tuzlu suda 20 dakika bekletin.\n'
            'Yağda kızartıp kağıt havlu üzerinde yağını alın.\n'
            'Soğan ve kıymayı kavurun, domates ve biber ekleyin.\n'
            'Patlıcanları ortadan yarıp iç harcı doldurun.\n'
            'Üzerine domates dilimleri koyup 180°C fırında 30 dakika pişirin.'
        ),
        'image_url': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80',
        'ingredients': [
            ('Patlıcan', '4 adet'),
            ('Kıyma', '300 gram'),
            ('Soğan', '2 adet'),
            ('Domates', '3 adet'),
            ('Yeşil Biber', '2 adet'),
            ('Sarımsak', '3 diş'),
            ('Sıvıyağ', '1/2 su bardağı'),
        ],
    },
    {
        'title': 'Çikolatalı Sufle',
        'prep_time': '25 dk',
        'difficulty': 'Zor',
        'servings': '4 Kişilik',
        'description': 'Dışı çıtır içi sıvı akan fondant sufle. Sıcak servis edildiğinde mükemmel bir lezzet.',
        'instructions': (
            'Çikolata ve tereyağını benmari usulü eritin.\n'
            'Yumurta ve şekeri çırpın, eriyen çikolatayı ekleyin.\n'
            'Unu eleyin ve hafifçe karıştırın.\n'
            'Yağlanmış kaplara dökün ve buzdolabında 30 dakika bekletin.\n'
            '200°C fırında tam 12 dakika pişirip hemen servis yapın.'
        ),
        'image_url': 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=800&q=80',
        'ingredients': [
            ('Bitter Çikolata', '150 gram'),
            ('Tereyağı', '100 gram'),
            ('Yumurta', '3 adet'),
            ('Şeker', '80 gram'),
            ('Un', '2 yemek kaşığı'),
        ],
    },
    {
        'title': 'İmam Bayıldı',
        'prep_time': '55 dk',
        'difficulty': 'Orta',
        'servings': '4 Kişilik',
        'description': 'Soğan ve sarımsaklı zeytinyağlı dolma patlıcan. Soğuk servis edildiğinde daha lezzetlidir.',
        'instructions': (
            'Patlıcanları tuzlu suda bekletip süzün.\n'
            'Zeytinyağında soğan ve sarımsağı kavurun.\n'
            'Domates, maydanoz ve baharatları ekleyin.\n'
            'Patlıcanları yağda hafifçe kavurun.\n'
            'Harcı doldurun ve düşük ateşte 30 dakika pişirin.'
        ),
        'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=80',
        'ingredients': [
            ('Patlıcan', '3 adet'),
            ('Soğan', '3 adet'),
            ('Sarımsak', '5 diş'),
            ('Domates', '4 adet'),
            ('Zeytinyağı', '1/2 su bardağı'),
            ('Maydanoz', '1 demet'),
        ],
    },
    {
        'title': 'Tavuk Şiş',
        'prep_time': '40 dk',
        'difficulty': 'Kolay',
        'servings': '4 Kişilik',
        'description': 'Marine edilmiş tavuk parçalarından hazırlanan ızgara şiş. Sebzelerle birlikte servis edilir.',
        'instructions': (
            'Tavukları küp küp kesin.\n'
            'Yoğurt, zeytinyağı, sarımsak ve baharatlarla marine edin.\n'
            'En az 2 saat buzdolabında bekletin.\n'
            'Şişlere geçirip ızgarada veya mangalda pişirin.\n'
            'Yanında lavaş, soğan ve mevsim salatasıyla servis edin.'
        ),
        'image_url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=800&q=80',
        'ingredients': [
            ('Tavuk Göğsü', '600 gram'),
            ('Yoğurt', '3 yemek kaşığı'),
            ('Zeytinyağı', '2 yemek kaşığı'),
            ('Sarımsak', '3 diş'),
            ('Kırmızı Biber', '1 tatlı kaşığı'),
            ('Kimyon', '1 tatlı kaşığı'),
        ],
    },
    {
        'title': 'Lahmacun',
        'prep_time': '50 dk',
        'difficulty': 'Orta',
        'servings': '6 Kişilik',
        'description': 'İnce hamur üzerine baharatlı kıyma harcıyla hazırlanan Türk pizzası. Limon ve maydanozla servis edilir.',
        'instructions': (
            'Un, tuz, su ve mayayı yoğurup 30 dakika dinlendirin.\n'
            'Kıyma, soğan, domates, biber ve baharatları karıştırın.\n'
            'Hamuru ince açın, üzerine harcı yayın.\n'
            '250°C fırında 8-10 dakika pişirin.\n'
            'Üzerine limon sıkıp maydanoz ve soğanla servis edin.'
        ),
        'image_url': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=800&q=80',
        'ingredients': [
            ('Un', '3 su bardağı'),
            ('Kıyma', '400 gram'),
            ('Soğan', '2 adet'),
            ('Domates', '2 adet'),
            ('Kırmızı Biber Salçası', '1 yemek kaşığı'),
            ('Maydanoz', '1 demet'),
            ('İnce Kırmızı Biber', '1 tatlı kaşığı'),
        ],
    },
    {
        'title': 'Baklava',
        'prep_time': '90 dk',
        'difficulty': 'Zor',
        'servings': '12 Kişilik',
        'description': 'Tereyağlı yufkalar arasında antep fıstığı ile hazırlanan şerbetli Türk tatlısı.',
        'instructions': (
            'Şerbeti hazırlayıp soğumaya bırakın.\n'
            'Yufkaları eritilmiş tereyağıyla yağlayarak tepsiye dizin.\n'
            'Ortasına öğütülmüş fıstık yayın, kalan yufkaları üstüne dizin.\n'
            'Dilimleyip 180°C fırında altın rengi alana kadar pişirin.\n'
            'Fırından çıkınca soğuk şerbeti sıcak baklavaya dökün.'
        ),
        'image_url': 'https://images.unsplash.com/photo-1519676867240-f03562e64548?auto=format&fit=crop&w=800&q=80',
        'ingredients': [
            ('Yufka', '500 gram'),
            ('Antep Fıstığı', '300 gram'),
            ('Tereyağı', '250 gram'),
            ('Şeker', '2 su bardağı'),
            ('Su', '2 su bardağı'),
            ('Limon Suyu', '1 yemek kaşığı'),
        ],
    },
    {
        'title': 'Menemen',
        'prep_time': '20 dk',
        'difficulty': 'Kolay',
        'servings': '2 Kişilik',
        'description': 'Domates, biber ve yumurtadan oluşan klasik Türk kahvaltısı. Sucuklu veya sade yapılabilir.',
        'instructions': (
            'Zeytinyağında doğranmış soğanı kavurun.\n'
            'Biber ve domatesleri ekleyip suyunu çekene kadar pişirin.\n'
            'Tuz ve karabiber ekleyin.\n'
            'Yumurtaları kırıp karıştırın.\n'
            'Yumurtalar pişince ocaktan alın, sıcak servis edin.'
        ),
        'image_url': 'https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=800&q=80',
        'ingredients': [
            ('Yumurta', '3 adet'),
            ('Domates', '2 adet'),
            ('Yeşil Biber', '2 adet'),
            ('Soğan', '1 adet'),
            ('Zeytinyağı', '2 yemek kaşığı'),
            ('Tuz', 'Tatmak için'),
        ],
    },
    {
        'title': 'Künefe',
        'prep_time': '30 dk',
        'difficulty': 'Orta',
        'servings': '4 Kişilik',
        'description': 'Kadayıf ve tuzlu peynirden yapılan, şerbetli geleneksel Türk tatlısı.',
        'instructions': (
            'Şerbeti hazırlayıp soğumaya bırakın.\n'
            'Kadayıfı eritilmiş tereyağıyla yoğurun.\n'
            'Yarısını tepsiye basın, üzerine rendelenmiş peynir yayın.\n'
            'Kalan kadayıfı üstüne koyup bastırın.\n'
            'Orta ateşte her iki tarafı altın rengi alana kadar pişirin, şerbet dökün.'
        ),
        'image_url': 'https://images.unsplash.com/photo-1571167530149-c1105da4d61a?auto=format&fit=crop&w=800&q=80',
        'ingredients': [
            ('Tel Kadayıf', '400 gram'),
            ('Tuzlu Peynir', '300 gram'),
            ('Tereyağı', '150 gram'),
            ('Şeker', '1.5 su bardağı'),
            ('Su', '1.5 su bardağı'),
            ('Antep Fıstığı', '50 gram'),
        ],
    },
]


class Command(BaseCommand):
    help = '10 örnek tarif ekler'

    def handle(self, *args, **options):
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            user = User.objects.first()
        if not user:
            self.stderr.write('Önce bir kullanıcı oluşturun: python3 manage.py createsuperuser')
            return

        created = 0
        for data in RECIPES:
            if Recipe.objects.filter(title=data['title']).exists():
                self.stdout.write(f'  zaten var: {data["title"]}')
                continue

            recipe = Recipe.objects.create(
                title=data['title'],
                prep_time=data['prep_time'],
                difficulty=data['difficulty'],
                servings=data['servings'],
                description=data['description'],
                instructions=data['instructions'],
                image_url=data['image_url'],
                author=user,
            )

            for ing_name, qty in data['ingredients']:
                ingredient, _ = Ingredient.objects.get_or_create(name=ing_name)
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity_text=qty,
                )

            created += 1
            self.stdout.write(self.style.SUCCESS(f'  ✓ {recipe.title}'))

        self.stdout.write(self.style.SUCCESS(f'\n{created} tarif eklendi.'))
