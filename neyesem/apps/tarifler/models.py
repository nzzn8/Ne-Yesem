from django.db import models
from django.contrib.auth.models import User


class Kategori(models.Model):
    ad = models.CharField(max_length=100, unique=True, verbose_name="Kategori Adı")

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ['ad']

    def __str__(self):
        return self.ad


class Malzeme(models.Model):
    ad = models.CharField(max_length=100, unique=True, verbose_name="Malzeme Adı")

    class Meta:
        verbose_name = "Malzeme"
        verbose_name_plural = "Malzemeler"
        ordering = ['ad']

    def __str__(self):
        return self.ad


class Tarif(models.Model):
    class Zorluk(models.TextChoices):
        KOLAY = 'Kolay', 'Kolay'
        ORTA  = 'Orta',  'Orta'
        ZOR   = 'Zor',   'Zor'

    baslik            = models.CharField(max_length=200, verbose_name="Başlık")
    aciklama          = models.TextField(verbose_name="Kısa Açıklama")
    hazirlanma_suresi = models.CharField(max_length=50, verbose_name="Hazırlanma Süresi")
    zorluk            = models.CharField(
        max_length=10, choices=Zorluk.choices, verbose_name="Zorluk"
    )
    porsiyon          = models.CharField(max_length=50, blank=True, verbose_name="Porsiyon")
    talimatlar        = models.TextField(blank=True, verbose_name="Talimatlar")
    resim             = models.ImageField(
        upload_to='tarifler/', blank=True, null=True, verbose_name="Resim"
    )
    resim_url         = models.URLField(blank=True, null=True, verbose_name="Resim URL")
    kategori          = models.ForeignKey(
        Kategori, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='tarifler', verbose_name="Kategori",
    )
    yazar             = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='tarifler_yonetim', verbose_name="Yazar",
    )
    olusturulma       = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma")
    guncelleme        = models.DateTimeField(auto_now=True, verbose_name="Güncelleme")

    class Meta:
        verbose_name = "Tarif"
        verbose_name_plural = "Tarifler"
        ordering = ['-olusturulma']
        indexes = [
            models.Index(fields=['yazar', '-olusturulma']),
            models.Index(fields=['kategori']),
        ]

    def __str__(self):
        return self.baslik


class TarifMalzeme(models.Model):
    tarif   = models.ForeignKey(
        Tarif, on_delete=models.CASCADE, related_name='tarif_malzemeleri'
    )
    malzeme = models.ForeignKey(
        Malzeme, on_delete=models.CASCADE, related_name='tarif_malzemeleri'
    )
    miktar  = models.CharField(max_length=100, blank=True, verbose_name="Miktar/Birim")

    class Meta:
        verbose_name = "Tarif Malzemesi"
        verbose_name_plural = "Tarif Malzemeleri"
        unique_together = [('tarif', 'malzeme')]

    def __str__(self):
        return f"{self.miktar} {self.malzeme.ad}".strip()
