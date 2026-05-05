from .models import Malzeme, TarifMalzeme


def malzemeleri_guncelle(tarif, adlar: list, miktarlar: list) -> None:
    """Tarifte kayıtlı malzemeleri sıfırdan yazar (ekle & düzenle için ortak)."""
    tarif.tarif_malzemeleri.all().delete()
    for ad, miktar in zip(adlar, miktarlar):
        ad = ad.strip()
        if not ad:
            continue
        malzeme, _ = Malzeme.objects.get_or_create(ad=ad)
        TarifMalzeme.objects.create(tarif=tarif, malzeme=malzeme, miktar=miktar.strip())
