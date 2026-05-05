from django.shortcuts import get_object_or_404
from django.db import models as db_models
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse

from .models import Tarif, Malzeme, Kategori
from .forms import TarifForm
from .services import malzemeleri_guncelle


def malzeme_onerileri(request):
    q = request.GET.get('q', '').strip()
    if not q:
        results = list(
            Malzeme.objects
            .annotate(kullanim=db_models.Count('tarif_malzemeleri'))
            .order_by('-kullanim', 'ad')
            .values_list('ad', flat=True)[:8]
        )
        return JsonResponse({'results': results, 'popular': True})
    if len(q) < 2:
        return JsonResponse({'results': [], 'popular': False})
    results = list(
        Malzeme.objects
        .filter(ad__icontains=q)
        .order_by('ad')
        .values_list('ad', flat=True)[:12]
    )
    return JsonResponse({'results': results, 'popular': False})


class TarifListesiView(ListView):
    model = Tarif
    template_name = 'tarifler/liste.html'
    context_object_name = 'tarifler'
    paginate_by = 12

    def get_queryset(self):
        qs = (
            Tarif.objects
            .select_related('yazar', 'kategori')
            .prefetch_related('tarif_malzemeleri__malzeme')
        )
        q = self.request.GET.get('q', '').strip()
        if q:
            for parca in [p.strip() for p in q.split(',') if p.strip()]:
                qs = qs.filter(
                    db_models.Q(baslik__icontains=parca) |
                    db_models.Q(tarif_malzemeleri__malzeme__ad__icontains=parca) |
                    db_models.Q(kategori__ad__icontains=parca)
                )
            qs = qs.distinct()
        kategori = self.request.GET.get('kategori')
        if kategori:
            qs = qs.filter(kategori_id=kategori)
        zorluk = self.request.GET.get('zorluk')
        if zorluk:
            qs = qs.filter(zorluk=zorluk)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['kategoriler'] = Kategori.objects.all()
        ctx['arama'] = self.request.GET.get('q', '')
        ctx['secili_kategori'] = self.request.GET.get('kategori', '')
        ctx['secili_zorluk'] = self.request.GET.get('zorluk', '')
        ctx['toplam'] = self.get_queryset().count()
        return ctx


class TarifDetayView(DetailView):
    model = Tarif
    template_name = 'tarifler/detay.html'
    context_object_name = 'tarif'

    def get_queryset(self):
        return Tarif.objects.select_related('yazar', 'kategori').prefetch_related(
            'tarif_malzemeleri__malzeme'
        )


class TarifEkleView(LoginRequiredMixin, CreateView):
    model = Tarif
    form_class = TarifForm
    template_name = 'tarifler/form.html'
    login_url = 'users:login'

    def get_success_url(self):
        return reverse('tarifler:detay', kwargs={'pk': self.object.pk}) + '?saved=1'

    def form_valid(self, form):
        form.instance.yazar = self.request.user
        response = super().form_valid(form)
        malzemeleri_guncelle(
            tarif=self.object,
            adlar=self.request.POST.getlist('malzeme_ad[]'),
            miktarlar=self.request.POST.getlist('malzeme_miktar[]'),
        )
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Lütfen eksik veya hatalı alanları düzeltin.')
        return super().form_invalid(form)


class TarifDuzenleView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tarif
    form_class = TarifForm
    template_name = 'tarifler/form.html'
    login_url = 'users:login'

    def test_func(self):
        return self.get_object().yazar == self.request.user

    def get_success_url(self):
        return reverse('tarifler:detay', kwargs={'pk': self.object.pk}) + '?updated=1'

    def form_valid(self, form):
        response = super().form_valid(form)
        malzemeleri_guncelle(
            tarif=self.object,
            adlar=self.request.POST.getlist('malzeme_ad[]'),
            miktarlar=self.request.POST.getlist('malzeme_miktar[]'),
        )
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Lütfen eksik veya hatalı alanları düzeltin.')
        return super().form_invalid(form)


class TarifSilView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tarif
    template_name = 'tarifler/sil_onay.html'
    login_url = 'users:login'

    def test_func(self):
        return self.get_object().yazar == self.request.user

    def get_success_url(self):
        return reverse('tarifler:liste')

    def form_valid(self, form):
        messages.success(self.request, f'"{self.object.baslik}" tarifi silindi.')
        return super().form_valid(form)
