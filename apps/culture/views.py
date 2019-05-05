from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from apps.product.models import Banner,ProductCategory
from apps.product import models
# Create your views here.

@method_decorator(cache_page(timeout=120, cache='page_cache'), name='dispatch')
class CompanyIntroduceView(View):
    def get(self,request):
        banners = models.Banner.objects.only('id', 'image_url').filter(is_delete=False)
        top_categories = ProductCategory.objects.only('id', 'name').filter(is_delete=False, parent_id=None)
        context={
            'top_categories':top_categories,
            'banners':banners
        }
        return render(request, 'product/company_introduce.html',context=context)

@method_decorator(cache_page(timeout=120, cache='page_cache'), name='dispatch')
class CompanyCultureView(View):
    def get(self,request):
        top_categories = ProductCategory.objects.only('id', 'name').filter(is_delete=False, parent_id=None)
        banners = models.Banner.objects.only('id', 'image_url').filter(is_delete=False)
        context = {
            'top_categories': top_categories,
            'banners': banners
        }
        return render(request, 'product/company_culture.html',context=context)

