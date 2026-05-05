from django.contrib import admin
from .models import Tarif, Malzeme, TarifMalzeme, Kategori


class TarifMalzemeInline(admin.TabularInline):
    model = TarifMalzeme
    extra = 1
    autocomplete_fields = ['malzeme']


@admin.register(Tarif)
class TarifAdmin(admin.ModelAdmin):
    list_display  = ['baslik', 'yazar', 'kategori', 'zorluk', 'olusturulma']
    list_filter   = ['zorluk', 'kategori']
    search_fields = ['baslik', 'aciklama']
    inlines       = [TarifMalzemeInline]
    readonly_fields = ['olusturulma', 'guncelleme']


@admin.register(Malzeme)
class MalzemeAdmin(admin.ModelAdmin):
    search_fields = ['ad']


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    search_fields = ['ad']


@admin.register(TarifMalzeme)
class TarifMalzemeAdmin(admin.ModelAdmin):
    list_display  = ['tarif', 'malzeme', 'miktar']
    list_filter   = ['malzeme']
    search_fields = ['tarif__baslik', 'malzeme__ad']
