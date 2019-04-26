from django.shortcuts import render
from django.views import View

from . import models,forms
from apps.product.models import Banner,ProductCategory

# Create your views here.

class ClientWordsView(View):
    def get(self,request):
        banners = Banner.objects.only('id', 'image_url').filter(is_delete=False).order_by('priority', '-update_time',
                                                                                          '-id')
        top_categories = ProductCategory.objects.only('id', 'name').filter(is_delete=False, parent_id=None)
        return render(request, 'product/client_words.html', locals())


