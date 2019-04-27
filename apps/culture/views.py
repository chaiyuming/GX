from django.shortcuts import render
from django.views import View
from apps.product.models import Banner,ProductCategory

from apps.product import models
# Create your views here.

class CompanyIntroduceView(View):
    def get(self,request):
        banners = models.Banner.objects.only('id', 'image_url').filter(is_delete=False)
        top_categories = ProductCategory.objects.only('id', 'name').filter(is_delete=False, parent_id=None)
        context={
            'top_categories':top_categories,
            'banners':banners
        }
        return render(request, 'product/company_introduce.html',context=context)


class CompanyCultureView(View):
    def get(self,request):
        top_categories = ProductCategory.objects.only('id', 'name').filter(is_delete=False, parent_id=None)
        banners = models.Banner.objects.only('id', 'image_url').filter(is_delete=False)
        context = {
            'top_categories': top_categories,
            'banners': banners
        }
        return render(request, 'product/company_culture.html',context=context)

