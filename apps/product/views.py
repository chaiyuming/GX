import logging
import random

from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


from . import models,constants
from utils.paginator_script import get_paginator_data
# Create your views here.
logger=logging.getLogger('inter_log')


@method_decorator(cache_page(timeout=120, cache='page_cache'), name='dispatch')
class IndexView(View):
    def get(self,request):
        banners=models.Banner.objects.only('id','image_url').filter(is_delete=False)
        products=models.Products.objects.only('id','brand','thumbnail','describe').filter(is_delete=False)
        top_categories=models.ProductCategory.objects.only('id','name').filter(is_delete=False,parent_id=None)
        try:
            page = int(request.GET.get('page', 1))
        except Exception as e:
            logger.info('新闻页数格式错误：{}'.format(e))
            page = 1
        # 创建对象
        paginator = Paginator(products, constants.ONE_PAGE__PRODUCTS_COUNT)
        # 某一页的数据
        try:
            page_object = paginator.page(page)
        except EmptyPage:
            # 若用户访问的页数大于实际页数，则返回最后一页数据
            logger.info('用户访问的页数大于总页数')
            page_object = paginator.page(paginator.num_pages)
        # 调用get_data_pagination函数
        data_pagination = get_paginator_data(paginator, page_object)
        context={
            'products':page_object.object_list,
            'page':page,
            'paginator':paginator,
            'pag_objects':page_object,
            'banners':banners,
            'top_categories':top_categories
        }
        context.update(data_pagination)
        return render(request, 'product/index.html',context=context)

@method_decorator(cache_page(timeout=120, cache='page_cache'), name='dispatch')
class ProductsView(View):
    '''
    the index of product view
    '''
    def get(self,request):
        banners=models.Banner.objects.only('id','image_url').filter(is_delete=False)
        top_categories=models.ProductCategory.objects.only('id','name').filter(is_delete=False,parent_id=None)
        try:
            top_tag_id = int(request.GET.get('top_tag_id', 0))
        except Exception as e:
            logger.info("一级级分类id错误：\n{}".format(e))
            top_tag_id=0
        try:
            sub_tag_id = int(request.GET.get('sub_tag_id', 0))
        except Exception as e:
            logger.info("一级级分类id错误：\n{}".format(e))
            sub_tag_id=0
        if top_tag_id == 0:
            top_category=models.ProductCategory.objects.only('id','name').filter(is_delete=False,parent_id=None)
        else:
            top_category=models.ProductCategory.objects.get(id=top_tag_id)
        if top_tag_id and top_tag_id != 0 and  sub_tag_id and sub_tag_id !=0:
            products=models.Products.objects.only('id', 'brand', 'thumbnail', 'describe').filter(is_delete=False,category_id=sub_tag_id,category__parent_id=top_tag_id)
        elif top_tag_id and top_tag_id != 0:
            products = models.Products.objects.only('id', 'brand', 'thumbnail', 'describe').filter(is_delete=False,category__parent_id=top_tag_id)
        else:
            products = models.Products.objects.only('id', 'brand', 'thumbnail', 'describe').filter(is_delete=False)

        try:
            page = int(request.GET.get('page', 1))
        except Exception as e:
            logger.info('新闻页数格式错误：{}'.format(e))
            page = 1
        # 创建对象
        paginator = Paginator(products, constants.ONE_PAGE__PRODUCTS_COUNT)
        # 某一页的数据
        try:
            page_object = paginator.page(page)
        except EmptyPage:
            # 若用户访问的页数大于实际页数，则返回最后一页数据
            logger.info('用户访问的页数大于总页数')
            page_object = paginator.page(paginator.num_pages)
        # 调用get_data_pagination函数
        data_pagination = get_paginator_data(paginator, page_object)
        context={
            'sub_tag_id':sub_tag_id,
            'top_tag_id':top_tag_id,
            'top_category':top_category,
            'products':page_object.object_list,
            'page':page,
            'paginator':paginator,
            'pag_objects':page_object,
            'banners':banners,
            'top_categories':top_categories
        }
        context.update(data_pagination)
        return render(request, 'product/products.html',context=context)

class ProductDetailView(View):
    '''
    the product detail view
    '''
    def get(self,request,p_id):
        banners = models.Banner.objects.only('id', 'image_url').filter(is_delete=False)
        top_categories = models.ProductCategory.objects.only('id', 'name').filter(is_delete=False, parent_id=None)
        products = models.Products.objects.only('id', 'brand', 'thumbnail', 'describe','version','update_time').filter(is_delete=False,id=p_id).first()
        random_products = list(models.Products.objects.only('brand','thumbnail','version','describe','id').filter(is_delete=False))
        if len(random_products) >=8:
            random_products=random.sample(random_products,8)
        else:
            random_products=random_products
        context = {
            'banners': banners,
            'top_categories': top_categories,
            'products': products,
            'random_products': random_products
        }
        return render(request,'product/product_detail.html',context=context)

@method_decorator(cache_page(timeout=120, cache='page_cache'), name='dispatch')
class ContactView(View):
    def get(self,request):
        top_categories = models.ProductCategory.objects.only('id', 'name').filter(is_delete=False, parent_id=None)
        banners = models.Banner.objects.only('id', 'image_url').filter(is_delete=False)
        return render(request,'product/contact.html',locals())
