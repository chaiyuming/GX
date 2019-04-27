import json
import logging
import qiniu

from datetime import datetime
from django.shortcuts import render,Http404
from django.views import View
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from urllib import parse
from collections import OrderedDict

from utils.json_fun import to_json_data
from utils.res_code import Code, error_map
from apps.product import models
from apps.news.models import News
from apps.word.models import ClientWords
from utils.fastdfs.fdfs import FDFS_Client
from . import forms,constants
from utils.paginator_script import get_paginator_data

# Create your views here.

logger = logging.getLogger('inter_log')

@method_decorator([staff_member_required(login_url='/')],name='dispatch')
class IndexView(View):
    def get(self, request):
        '''
        create admin index  view
        :param request:
        :return:
        '''
        return render(request, 'cms/index/index.html')
class ProductTopTagManageView(PermissionRequiredMixin, View):
    permission_required = ('product.add_productcategory', 'product.view_productcategory')
    # 如果raise_exception给出参数，则装饰器将引发 PermissionDenied，提示403（HTTP Forbidden）视图而不是重定向到登录页面
    raise_exception = True

    def handle_no_permission(self):
        if self.request.method.lower() != 'get':
            return to_json_data(errno=Code.ROLEERR, errmsg='没有操作权限')
        else:
            return super(ProductTopTagManageView, self).handle_no_permission()

    def get(self, request):
        '''
        create add product first category info views
        :param request:
        :return:
        '''
        # annotate()级联查询
        categories = models.ProductCategory.objects.only('parent__name','parent_id').annotate(num_products=Count('products')).filter(is_delete=False,parent_id=None).order_by('-num_products', '-update_time')
        # categories_list=[]
        # for category in categories:
        #     categories_list.append(category.to_dict_data())
        return render(request, 'cms/product/products_top_category.html', locals())
    def post(self, request):
        # 1、从前端获取数据
        json_data = request.body
        if not json_data:
            return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        dict_data = json.loads(json_data.decode('utf8'))
        tag_name = dict_data.get('name')
        # 2、校验
        if tag_name:
            tag_name = tag_name.strip()
            # get_or_create()如果没有就会自动创建，返回一个新的实列对象，以及True组成的元祖。
            # 如果查找到一个对象，get_or_create() 返回一个包含匹配到的对象以及False 组成的元组。
            # 3、保存到数据库
            tag_tuple, tag_boolean = models.ProductCategory.objects.get_or_create(name=tag_name)
            # news_tag_dict可以不写
            products_tag_dict = {
                'id': tag_tuple.id,
                'name': tag_tuple.name
            }
            # 4、返回执行结果
            return to_json_data(errmsg='产品一级分类创建成功！', data=products_tag_dict) if tag_boolean else to_json_data(errno=Code.DATAEXIST, errmsg='产品一级分类已存在，请重新输入！')
        else:
            return to_json_data(errno=Code.PARAMERR, errmsg='以及标签名不能为空！')
class ProductTopCategoryEditView(PermissionRequiredMixin,View):
    permission_required = ('product.change_productcategory', 'product.view_productcategory','product.delete_productcategory')
    # 如果raise_exception给出参数，则装饰器将引发 PermissionDenied，提示403（HTTP Forbidden）视图而不是重定向到登录页面
    raise_exception = True
    def handle_no_permission(self):
        return to_json_data(errno=Code.ROLEERR, errmsg='没有操作权限')
    def delete(self,request,top_tag_id):
        '''
        delete the top_category
        :param request:
        :param first_tag_id:
        :return:‘/cms/top_category/<int:first_tag_id>/’
        '''
        category=models.ProductCategory.objects.only('id').filter(is_delete=False,id=top_tag_id).first()
        if category:
            category.is_delete=True
            category.save(update_fields=['is_delete'])
            return to_json_data(errno=Code.OK, errmsg='标签删除成功')
        else:
            return to_json_data(errno=Code.PARAMERR, errmsg='您删除的标签不存在')
    def put(self,request,top_tag_id):
        category = models.ProductCategory.objects.only('id').filter(is_delete=False, id=top_tag_id).first()
        try:
            json_data=request.body
            if not json_data:
                return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
            dict_data = json.loads(json_data.decode('utf8'))
            tag_name=dict_data.get('name')
        except Exception as e:
            logger.error('错误信息：{}'.format(e))
            return to_json_data(errno=Code.UNKOWNERR, errmsg=error_map[Code.UNKOWNERR])
        if category:
            tag_name=tag_name.strip()
            if tag_name:
                exist=models.ProductCategory.objects.only('id').filter(is_delete=False,name=tag_name).exists()
                if not exist:
                    category.name=tag_name
                    category.save(update_fields=['name'])
                    return to_json_data(errmsg='标签更新成功！')
                else:
                    return to_json_data(errno=Code.PARAMERR, errmsg='标签已存在！')
            else:
                return to_json_data(errno=Code.PARAMERR, errmsg='标签名不能为空！')
        else:
            return to_json_data(errno=Code.NODATA, errmsg='标签不存在！')

class ProductSubTagManageView(PermissionRequiredMixin,View):
    permission_required = ('product.add_productcategory', 'product.view_productcategory')
    # 如果raise_exception给出参数，则装饰器将引发 PermissionDenied，提示403（HTTP Forbidden）视图而不是重定向到登录页面
    raise_exception = True
    def handle_no_permission(self):
        if self.request.method.lower() != 'get':
            return to_json_data(errno=Code.ROLEERR, errmsg='没有操作权限')
        else:
            return super(ProductSubTagManageView, self).handle_no_permission()
    def get(self,request):
        category_list=models.ProductCategory.objects.select_related('parent').only('parent_id','parent__name','id','name').annotate(num_products=Count('products')).filter(is_delete=False,parent__isnull=False,parent__is_delete=False).order_by('-num_products', '-update_time')
        return render(request,'cms/product/products_sub_category.html',locals())
class AddSubCategoryView(PermissionRequiredMixin,View):
    '''
    add sub category view
    '''
    permission_required = ('product.add_productcategory', 'product.view_productcategory')
    # 如果raise_exception给出参数，则装饰器将引发 PermissionDenied，提示403（HTTP Forbidden）视图而不是重定向到登录页面
    raise_exception = True
    def handle_no_permission(self):
        if self.request.method.lower() != 'get':
            return to_json_data(errno=Code.ROLEERR, errmsg='没有操作权限')
        else:
            return super(AddSubCategoryView, self).handle_no_permission()
    def get(self,request):
        categories=models.ProductCategory.objects.select_related('parent').only('parent_id','parent__name','name','id').filter(is_delete=False,parent_id=None)
        return render(request,'cms/product/add_sub_category.html',locals())
    def post(self,request):
        try:
            json_data=request.body
            if not json_data:
                return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
            dict_data = json.loads(json_data.decode('utf8'))
            parent_id=dict_data.get('parent_id')
            sub_tag_name=dict_data.get('sub_tag_name')
        except Exception as e:
            logger.error('错误信息：{}'.format(e))
            return to_json_data(errno=Code.UNKOWNERR, errmsg=error_map[Code.UNKOWNERR])
        try:
            if parent_id:
                exist=models.ProductCategory.objects.only('id').filter(is_delete=False,id=parent_id).exists()
                if not exist:
                    return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        except Exception as e:
            logger.info('前端传来的parent_id有异常:{}'.format(e))
            return to_json_data(errno=Code.UNKOWNERR, errmsg=error_map[Code.UNKOWNERR])
        if sub_tag_name:
            sub_tag_name=sub_tag_name.strip()
            tag_tuple, tag_boolean = models.ProductCategory.objects.get_or_create(name=sub_tag_name,parent_id=parent_id)
            return to_json_data(errmsg='二级分类创建成功！') if tag_boolean else to_json_data(errno=Code.DATAEXIST, errmsg='标签已存在，请重新输入！')

class ProductSubCategoryEditView(PermissionRequiredMixin,View):
    '''
    edit the sub category
    :return:‘/cms/sub_category/<int:sub_tag_id>/’
    '''
    permission_required = ('product.change_productcategory', 'product.view_productcategory','product.delete_productcategory')
    # 如果raise_exception给出参数，则装饰器将引发 PermissionDenied，提示403（HTTP Forbidden）视图而不是重定向到登录页面
    raise_exception = True
    def handle_no_permission(self):
        if self.request.method.lower() != 'get':
            return to_json_data(errno=Code.ROLEERR, errmsg='没有操作权限')
        else:
            return super(ProductSubCategoryEditView, self).handle_no_permission()
    def get(self,request,sub_tag_id):
        categories = models.ProductCategory.objects.select_related('parent').only('parent_id','id').filter(is_delete=False,parent_id=None)
        sub_category=models.ProductCategory.objects.only('parent_id').select_related('parent').filter(is_delete=False,id=sub_tag_id).first()
        if sub_category:
            return render(request,'cms/product/add_sub_category.html',locals())
        else:
            raise Http404('您访问的产品分类不存在！')
    def delete(self,request,sub_tag_id):
        sub_category = models.ProductCategory.objects.only('id', 'parent_id').select_related('parent').filter(
            is_delete=False,id=sub_tag_id,parent__is_delete=False).first()
        if sub_category:
            sub_category.is_delete=True
            # sub_category.parent.is_delete=True
            sub_category.save(update_fields=['is_delete'])
            return to_json_data(errmsg='该分类删除成功！')
        else:
            return to_json_data(errno=Code.PARAMERR, errmsg='您要删除的分类不存在！')
    def put(self,request,sub_tag_id):
        sub_category = models.ProductCategory.objects.only('id', 'parent_id').select_related('parent').filter(
            is_delete=False, id=sub_tag_id,parent__is_delete=False).first()
        if not sub_category:
            return to_json_data(errno=Code.PARAMERR,errmsg="需要更新的的产品分类不存在")
        json_data = request.body
        if not json_data:
            return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        dict_data = json.loads(json_data.decode('utf8'))
        try:
            parent_id=int(dict_data.get('parent_id'))
        except Exception as e:
            logger.info('产品分类一级id参数错误:{}'.format(e))
            return to_json_data(errno=Code.PARAMERR, errmsg='参数错误')
        if parent_id == 0:
            return to_json_data(errno=Code.PARAMERR,errmsg='请选择一级分类')
        sub_tag_name=dict_data.get('sub_tag_name')
        sub_tag_name=sub_tag_name.strip()
        if not sub_tag_name:
            return to_json_data(errno=Code.PARAMERR,errmsg='二级分类名不能为空！')
        if sub_tag_name == sub_category.name and parent_id == sub_category.parent_id:
            return to_json_data(errno=Code.PARAMERR,errmsg='产品一级分类和二级分类均未改变！')
        else:
            sub_category.name=sub_tag_name
            sub_category.parent_id=parent_id
            sub_category.save(update_fields=['name','parent_id'])
            return to_json_data(errmsg="产品二级分类更新成功")

class AddProductView(PermissionRequiredMixin,View):
    permission_required = ('product.view_products','product.add_products')
    # 如果raise_exception给出参数，则装饰器将引发 PermissionDenied，提示403（HTTP Forbidden）视图而不是重定向到登录页面
    raise_exception = True
    def handle_no_permission(self):
        if self.request.method.lower() != 'get':
            return to_json_data(errno=Code.ROLEERR, errmsg='没有操作权限')
        else:
            return super(AddProductView, self).handle_no_permission()
    def get(self,request):
        top_categories=models.ProductCategory.objects.only('id','name').filter(parent_id=None,is_delete=False)
        sub_categories=models.ProductCategory.objects.only('id','name').filter(parent_id__isnull=False,is_delete=False)
        return render(request,'cms/product/pub_products.html',locals())
    def post(self,request):
        '''
        add products view
        :param request:
        :return:
        '''
        # 1、从前端获取参数
        json_data = request.body
        if not json_data:
            return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        # 将json转化为dict
        dict_data = json.loads(json_data.decode('utf8'))
        # 2、校验
        form=forms.AddProductForm(data=dict_data)
        if form.is_valid():
            top_tag_id=form.cleaned_data.get('top_tag_id')
            sub_tag_id=form.cleaned_data.get('sub_tag_id')
            category=models.ProductCategory.objects.get(id=sub_tag_id,parent_id=top_tag_id)
            product_instance=form.save(commit=False)
            product_instance.category=category
            product_instance.save()
            return to_json_data(errmsg='产品添加成功')
        else:
            err_msg_list=[]
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get('message'))
            err_msg_str='/'.join(err_msg_list)
            return to_json_data(errno=Code.PARAMERR,errmsg=err_msg_str)
class ProductManageView(PermissionRequiredMixin,View):
    permission_required = ('product.view_products','product.change_products','product.delete_products')
    # 如果raise_exception给出参数，则装饰器将引发 PermissionDenied，提示403（HTTP Forbidden）视图而不是重定向到登录页面
    raise_exception = True
    def get(self,request):
        products=models.Products.objects.only('brand','describe','version','category__name','category__parent__name','thumbnail').filter(is_delete=False)
        top_categories=models.ProductCategory.objects.only('id','name').filter(is_delete=False,parent_id=None)
        sub_categories=models.ProductCategory.objects.only('id','name','parent_id','parent__name').filter(is_delete=False,parent_id__isnull=False)
        title=request.GET.get('title','')
        if title:
            products=products.filter(Q(brand__contains=title) | Q(version__contains=title) | Q(describe__contains=title) | Q(category__name__contains=title) | Q(category__parent__name=title))
        try:
            top_category_id=int(request.GET.get('top_category',0))
        except Exception as e:
            logger.info("一级分类id错误：\n{}".format(e))
            top_category_id=0
        if top_category_id !=0:
            products=products.filter(category__parent_id=top_category_id)
        try:
            sub_category_id=int(request.GET.get('sub_category',0))
        except Exception as e:
            logger.info("二级分类id错误：\n{}".format(e))
            sub_category_id=0
        if sub_category_id !=0:
            products=products.filter(category_id=sub_category_id)
        try:
            page=request.GET.get('page',1)
        except Exception as e:
            logger.info('产品页数格式错误：{}'.format(e))
            page = 1
        # 创建对象
        paginator = Paginator(products,constants.PER_PAGE_PRODUCT_COUNT)
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
            'paginator': paginator,
            'title': title,
            'sub_categories':sub_categories,
            'top_categories':top_categories,
            'top_category_id':top_category_id,
            'sub_category_id':sub_category_id,
            'page_object': page_object,
            'products': page_object.object_list,
            'url_paramter': parse.urlencode({
                'title': title,
                'top_category_id':top_category_id,
                'sub_category_id':sub_category_id,
            })
        }
        context.update(data_pagination)
        return render(request, 'cms/product/products_manage.html', context=context)
class ProductEditView(ProductManageView,View):
    permission_required = ('product.view_products','product.change_products','product.delete_products')
    # 如果raise_exception给出参数，则装饰器将引发 PermissionDenied，提示403（HTTP Forbidden）视图而不是重定向到登录页面
    raise_exception = True
    def handle_no_permission(self):
        if self.request.method.lower() != 'get':
            return to_json_data(errno=Code.ROLEERR, errmsg='没有操作权限')
        else:
            return super(ProductEditView, self).handle_no_permission()

    def get(self, request, product_id):
        '''
        get to the product of product_id
        :param request:
        :param product_id:
        :return:
        '''
        product = models.Products.objects.only('id', 'brand', 'version', 'thumbnail', 'describe', 'category_id',
                                               'category__parent_id').filter(is_delete=False, id=product_id).first()
        # product = models.Products.objects.only('id').filter(is_delete=False,id=product_id).first()
        if product:
            sub_categories = models.ProductCategory.objects.only('id', 'name').filter(parent_id__isnull=False,
                                                                                    is_delete=False)
            top_categories = models.ProductCategory.objects.only('id', 'name').filter(parent_id=None, is_delete=False)
            context = {
                'product': product,
                'top_categories': top_categories,
                'sub_categories': sub_categories
            }
            return render(request, 'cms/product/pub_products.html',context=context)
        else:
            raise Http404('您访问的产品不存在！')
    def delete(self,request,product_id):
        '''
            delete the product
        :param request:
        :param product_id:
        :return: '/cms/product/edit/<int:product_id>/'
        '''
        product = models.Products.objects.only('id').filter(is_delete=False, id=product_id).first()
        if not product:
            return to_json_data(errno=Code.PARAMERR,errmsg='需要删除的产品不存在！')
        else:
            product.is_delete=True
            product.save(update_fields=['is_delete'])
            return to_json_data(errmsg='产品删除成功！')
    def put(self,request,product_id):

        product = models.Products.objects.only('id').filter(is_delete=False, id=product_id).first()
        if not product:
            return to_json_data(errno=Code.PARAMERR, errmsg='需要更新的产品不存在！')
        # 1、从前端获取参数
        json_data = request.body
        if not json_data:
            return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        # 将json转化为dict
        dict_data = json.loads(json_data.decode('utf8'))
        form=forms.AddProductForm(data=dict_data)
        if form.is_valid():
            top_tag_id = form.cleaned_data.get('top_tag_id')
            sub_tag_id = form.cleaned_data.get('sub_tag_id')
            category = models.ProductCategory.objects.get(id=sub_tag_id, parent_id=top_tag_id)
            product.brand=form.cleaned_data.get('brand')
            product.version=form.cleaned_data.get('version')
            product.describe=form.cleaned_data.get('describe')
            product.describe=form.cleaned_data.get('describe')
            product.thumbnail=form.cleaned_data.get('thumbnail')
            product.category=category
            product.save()
            return to_json_data(errmsg='产品信息更新成功！')
        else:
            error_msg_list = []
            for item in form.errors.get_json_data().values():
                error_msg_list.append(item[0].get('message'))
            error_msg_str = '/'.join(error_msg_list)
            return to_json_data(errno=Code.PARAMERR, errmsg=error_msg_str)

class SubByTopView(PermissionRequiredMixin,View):
    '''
    通过一级分类获取二级分类
    '''
    permission_required = ('product.add_productcategory', 'product.view_productcategory')
    raise_exception = True

    def handle_no_permission(self):
        return to_json_data(errno=Code.ROLEERR, errmsg='没有操作权限')
    def get(self,request,top_tag_id):
        tags=models.ProductCategory.objects.values('id','name').filter(is_delete=False,parent_id=top_tag_id)
        tags_list=[i for i in tags]
        return to_json_data(data={'sub_tags':tags_list})
class QiqiuToken(View):
    '''
    image upload to qiniu
    '''

    def get(self, request):
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY

        q = qiniu.Auth(access_key, secret_key)

        bucket_name = settings.QINIU_BUCKET_NAME
        token = q.upload_token(bucket_name)
        # 这里返回一个原声的json数据，不要用自定义的to_json_data，否则可能会有问题。
        return JsonResponse({'uptoken': token})
class UploadFdfs(PermissionRequiredMixin, View):
    '''
    upload image file to fdfs server
    '''
    permission_required = ('product.add_products',)
    def handle_no_permission(self):
        return to_json_data(errno=Code.ROLEERR, errmsg='没有上传图片的权限')

    def post(self, request):
        # 从前端获取图片文件对象
        image_file = request.FILES.get('image_file')
        if not image_file:
            logger.info('从前端获取图片失败')
            return to_json_data(errno=Code.NODATA, errmsg='从前端获取图片失败！')
        if image_file.content_type not in ('image/jpeg', 'image/png', 'image/gif','image/jpg'):
            logger.info('文件格式错误！')
            return to_json_data(errno=Code.DATAERR, errmsg='不能上传非图片文件')
        # 获取图片文件后缀名 jpg
        try:
            image_ext_name = image_file.name.split('.')[-1]
        except Exception as e:
            logger.info('图片拓展名错误：{}'.format(e))
            image_ext_name = 'jpg'
        try:
            # filename.read()读取文件内容，image_ext_name获取文件后缀名
            upload_res = FDFS_Client.upload_by_buffer(image_file.read(), file_ext_name=image_ext_name)
        except Exception as e:
            logger.error('图片上传出现异常：{}'.format(e))
            return to_json_data(errno=Code.UNKOWNERR, errmsg='图片上传异常')
        else:
            if upload_res.get('Status') != 'Upload successed.':
                logger.info('图片上传到FASTDFS服务器失败')
                return to_json_data(errno=Code.UNKOWNERR, errmsg='图片上传到服务器失败')
            else:
                image_name = upload_res.get('Remote file_id')
                image_url = settings.FASTDFS_SERVER_DOMAIN + image_name
                return to_json_data(data={'image_url': image_url}, errmsg='图片上传成功！')

class PubNewsView(PermissionRequiredMixin,View):
    permission_required = ('news.view_news','news.add_news')
    # 如果raise_exception给出参数，则装饰器将引发 PermissionDenied，提示403（HTTP Forbidden）视图而不是重定向到登录页面
    raise_exception = True
    def handle_no_permission(self):
        if self.request.method.lower() != 'get':
            return to_json_data(errno=Code.ROLEERR, errmsg='没有操作权限')
        else:
            return super(PubNewsView, self).handle_no_permission()
    def get(self,request):
        return render(request,'cms/news/news.html')
    def post(self,request):
        try:
            json_data=request.body
            if not json_data:
                return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
            dict_data = json.loads(json_data.decode('utf8'))
        except Exception as e:
            logger.error('错误信息：{}'.format(e))
            return to_json_data(errno=Code.UNKOWNERR, errmsg=error_map[Code.UNKOWNERR])
        form=forms.PubNewsForm(data=dict_data)
        if form.is_valid():
            news_instance=form.save(commit=False)
            news_instance.author=request.user
            news_instance.save()
            return to_json_data(errmsg='新闻创建成功！')
        else:
            err_msg_list = []
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get('message'))
            err_msg_str = '/'.join(err_msg_list)  # 拼接错误信息为一个字符串

            return to_json_data(errno=Code.PARAMERR, errmsg=err_msg_str)
class NewsManageView(PermissionRequiredMixin,View):
    '''
    create news list manage View
    route:/cms/news_manage
    '''
    permission_required = ('news.add_news', 'news.view_news')
    raise_exception = True

    def get(self,request):
        newses=News.objects.only('id','title','content','update_time','author__username').select_related('author').filter(is_delete=False)
        try:
            start=request.GET.get('start','')
            start=datetime.strptime(start,'%Y/%m/%d') if start else ''
            end=request.GET.get('end','')
            end=datetime.strptime(end,'%Y/%m/%d') if end else ''
        except Exception as e:
            logger.info('时间格式错误{}'.format(e))
            start=end=''
        if start and not end:
            newses = newses.filter(update_time__lte=start)
        if end and not start:
            newses = newses.filter(update_time__gte=end)
        if end and start:
            newses = newses.filter(update_time__range=(end, start))

        title = request.GET.get('title', '')
        if title:
            newses = newses.filter(Q(title__contains=title) | Q(author__username__icontains=title))
        try:
            page = int(request.GET.get('page', 1))
        except Exception as e:
            logger.info('新闻页数格式错误：{}'.format(e))
            page = 1
        # 创建对象
        paginator = Paginator(newses, constants.PER_PAGE_NEWS_COUNT)
        # 某一页的数据
        try:
            page_object = paginator.page(page)
        except EmptyPage:
            # 若用户访问的页数大于实际页数，则返回最后一页数据
            logger.info('用户访问的页数大于总页数')
            page_object = paginator.page(paginator.num_pages)
        # 调用get_data_pagination函数
        data_pagination = get_paginator_data(paginator, page_object)
        # 转换成字符串格式
        start = start.strftime('%Y/%m/%d') if start else ''
        end = end.strftime('%Y/%m/%d') if end else ''
        context = {
            'start': start,
            'end': end,
            'paginator': paginator,
            'title': title,
            'page_object': page_object,
            'newses': page_object.object_list,
            'url_paramter': parse.urlencode({
                'start': start,
                'end': end,
                'title': title,
            })
        }
        context.update(data_pagination)
        return render(request,'cms/news/news_manage.html',context=context)

class NewsEditView(PermissionRequiredMixin,View):
    '''
    edit the news view
    '''
    permission_required = ('news.delete_news','news.change_news','news.view_news')
    raise_exception = True
    def handle_no_permission(self):
        if self.request.method.lower() != 'get':
            return to_json_data(errno=Code.ROLEERR, errmsg='没有操作权限')
        else:
            return super(NewsEditView, self).handle_no_permission()
    def get(self,request,news_id):
        news=News.objects.only('id','title','content').filter(is_delete=False,id=news_id).first()
        if not news:
            raise Http404('您访问的新闻不存在！')
        else:
            context={
                'news':news
            }
            return render(request,'cms/news/news.html',context=context)
    def delete(self,request,news_id):
        '''
        delete the news
        :param request:
        :param news_id:
        :return: '/cms/news/<int:news_id>/
        '''
        news = News.objects.only('id', 'title', 'content').filter(is_delete=False, id=news_id).first()
        if not news:
            return to_json_data(errno=Code.PARAMERR, errmsg='你要删除的新闻不存在！')
        else:
            news.is_delete=True
            news.save(update_fields=['is_delete'])
            return to_json_data(errmsg='新闻删除成功！')
    def put(self,request,news_id):
        '''
        update the news view
        :param request:
        :param news_id:
        :return:
        '''
        news = News.objects.only('id', 'title', 'content').filter(is_delete=False, id=news_id).first()
        if not news:
            return to_json_data(errno=Code.PARAMERR, errmsg='您要更新的新闻不存在！')
        json_data=request.body
        if not json_data:
            return to_json_data(errno=Code.PARAMERR,errmsg=error_map[Code.PARAMERR])
        dict_data=json.loads(json_data.decode('utf8'))
        form=forms.PubNewsForm(data=dict_data)
        if form.is_valid():
            news.title=form.cleaned_data.get('title')
            news.content=form.cleaned_data.get('content')
            news.save()
            return to_json_data(errmsg='文章更新成功！')
        else:
            error_msg_list = []
            for item in form.errors.get_json_data().values():
                error_msg_list.append(item[0].get('message'))
            error_msg_str = '/'.join(error_msg_list)
            return to_json_data(errno=Code.PARAMERR, errmsg=error_msg_str)

class WordsView(PermissionRequiredMixin,View):
    permission_required = ('word.view_clientwords',)
    raise_exception = True
    def get(self,request):
        client_words=ClientWords.objects.only('username','telephone','email','update_time','content').filter(is_delete=False)
        return render(request,'cms/word/words.html',locals())

class BannerManageView(PermissionRequiredMixin,View):
    '''
    the banners  view
    '''
    permission_required = ('product.view_banner',)
    raise_exception = True
    def get(self,request):
        banners=models.Banner.objects.only('id','image_url','priority','link_to').filter(is_delete=False)
        priority_dict=OrderedDict(models.Banner.PRI_CHOICE)
        return render(request,'cms/product/banners.html',locals())
class AddBannerView(PermissionRequiredMixin,View):
    '''
    add the banner view
    '''
    permission_required = ('product.add_banner','product.view_banner')
    raise_exception = True
    def handle_no_permission(self):
        if self.request.method.lower() != 'get':
            return to_json_data(errno=Code.ROLEERR, errmsg='没有操作权限')
        else:
            return super(AddBannerView, self).handle_no_permission()
    def get(self,request):
        priority_dict = OrderedDict(models.Banner.PRI_CHOICE)
        return render(request, 'cms/product/add_banner.html', locals())
    def post(self,request):
        json_data=request.body
        if not json_data:
            return to_json_data(errno=Code.PARAMERR,errmsg=error_map([Code.PARAMERR]))
        dict_data=json.loads(json_data.decode('utf8'))
        try:
            priority=int(dict_data.get('priority'))
            priority_list=[i for i,_ in models.Banner.PRI_CHOICE]
            if priority not in priority_list:
                return to_json_data(errno=Code.PARAMERR, errmsg='优先级设置错误')
        except Exception as e:
            logger.error('优先级设置错误：{}'.format(e))
            return  to_json_data(errno=Code.PARAMERR, errmsg='优先级设置错误')
        image_url=dict_data.get('image_url')
        if not image_url:
            return to_json_data(errno=Code.PARAMERR,errmsg='轮播图url不能为空')
        try:
            link_to=dict_data.get('link_to')
            if not link_to:
                return to_json_data(errno=Code.PARAMERR, errmsg='跳转链接不能为空')
        except Exception as e:
            logger.error('跳转链接格式错误：{}'.format(e))
            return  to_json_data(errno=Code.PARAMERR, errmsg='跳转链接格式错误')

        banner,banner_boolean=models.Banner.objects.get_or_create(priority=priority,link_to=link_to,image_url=image_url)
        if banner_boolean:
            return to_json_data(errmsg='轮播图创建成功！')
        else:
            return to_json_data(errno=Code.PARAMERR,errmsg='轮播图已存在，请重新输入')
class BannerEditView(PermissionRequiredMixin,View):
    '''
    delete and update the banner view
    '''
    permission_required = ('product.change_banner', 'product.delete_banner')
    raise_exception = True

    def handle_no_permission(self):
        if self.request.method.lower() != 'get':
            return to_json_data(errno=Code.ROLEERR, errmsg='没有操作权限')
        else:
            return super(BannerEditView, self).handle_no_permission()
    def delete(self,request,banner_id):
        '''
        delete the banner
        :param request:
        :param banner_id:
        :return: '/cms/banner/<int:banner_id>/'
        '''
        banner=models.Banner.objects.only('id').filter(is_delete=False,id=banner_id).first()
        if not banner:
            return to_json_data(errno=Code.PARAMERR,errmsg='您要删除的轮播图不存在！')
        else:
            banner.is_delete=True
            banner.save(update_fields=['is_delete'])
            return to_json_data(errmsg='轮播图删除成功')
    def put(self,request,banner_id):
        banner = models.Banner.objects.only('id').filter(is_delete=False, id=banner_id).first()
        if not banner:
            return to_json_data(errno=Code.PARAMERR, errmsg='您要删除的轮播图不存在！')
        json_data=request.body
        if not json_data:
            return to_json_data(errno=Code.PARAMERR,errmsg=error_map([Code.PARAMERR]))
        dict_data=json.loads(json_data.decode('utf8'))
        image_url=dict_data.get('image_url')
        if not image_url:
            return to_json_data(errno=Code.PARAMERR,errmsg='轮播图url不能为空')
        try:
            link_to=dict_data.get('link_to')
            if not link_to:
                return to_json_data(errno=Code.PARAMERR, errmsg='跳转链接不能为空')
        except Exception as e:
            logger.error('轮播图url参数错误：{}'.format(e))
            return to_json_data(errno=Code.PARAMERR,errmsg='轮播图url参数错误')
        try:
            priority=int(dict_data.get('priority'))
            priority_list=[i for i ,_ in models.Banner.PRI_CHOICE]
            if priority not in priority_list:
                return to_json_data(errno=Code.PARAMERR, errmsg='优先级设置错误')
        except Exception as e:
            logger.error('优先级设置错误{}'.format(e))
            return to_json_data(errno=Code.PARAMERR, errmsg='优先级设置错误')
        if banner.image_url==image_url and banner.priority==priority and banner.link_to==link_to:
            return to_json_data(errno=Code.PARAMERR, errmsg='未修改任何值,请确认!')
        banner.link_to=link_to
        banner.priority=priority
        banner.image_url=image_url
        banner.save(update_fields=['priority', 'image_url','link_to'])
        return to_json_data(errmsg="轮播图更新成功")






















