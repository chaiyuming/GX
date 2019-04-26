import logging

from django.shortcuts import render,Http404
from django.views import View
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from . import models,constants
from apps.product.models import Banner,ProductCategory
from utils.paginator_script import get_paginator_data

# Create your views here.
logger=logging.getLogger('inter_log')
class NewsView(View):
    def get(self,request):
        top_categories = ProductCategory.objects.only('id', 'name').filter(is_delete=False, parent_id=None)
        newses=models.News.objects.only('id','title','update_time').filter(is_delete=False).order_by('-update_time','id')
        banners=Banner.objects.only('id','image_url').filter(is_delete=False).order_by('priority','-update_time','-id')
        try:
            page = int(request.GET.get('page', 1))
        except Exception as e:
            logger.info('新闻页数格式错误：{}'.format(e))
            page = 1
        # 创建对象
        paginator = Paginator(newses,constants.ONE_PAGE__NEWS_COUNT)
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
            'top_categories':top_categories,
            'newses':page_object.object_list,
            'page':page,
            'paginator':paginator,
            'pag_objects':page_object,
            'banners':banners
        }
        context.update(data_pagination)
        return render(request,'news/news.html',context=context)

class NewsDetailView(View):
    def get(self,request,news_id):
        news=models.News.objects.only('id','title','content','update_time').filter(is_delete=False,id=news_id).first()
        top_categories = ProductCategory.objects.only('id', 'name').filter(is_delete=False, parent_id=None)
        banners = Banner.objects.only('id', 'image_url').filter(is_delete=False).order_by('priority', '-update_time',
                                                                                          '-id')
        if not news:
            raise Http404('您访问的新闻不存在！')
        else:
            context={
                'news':news,
                'top_categories':top_categories,
                'banners': banners
            }
            return render(request,'news/news_detail.html',context=context)
