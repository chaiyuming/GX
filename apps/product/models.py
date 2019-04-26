
from django.db import models
from utils.models import ModelBase
from django.core.validators import MinLengthValidator
# Create your models here.

class ProductCategory(ModelBase):
    '''
        create product category
    '''
    name = models.CharField(max_length=100,verbose_name='产品分类')
    parent=models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,related_name='sub_category',verbose_name='一级分类')

    class Meta:
        ordering = ['-update_time', '-id']
        db_table='tb_category'
        verbose_name='产品分类'
        verbose_name_plural=verbose_name

    def to_dict_data(self):
        comment_dict = {
            'id': self.id,
            'name':self.name,
            'parent': self.parent.to_dict_data() if self.parent else None,
        }
        return comment_dict
    def __str__(self):
        return self.name
class Products(ModelBase):
    brand = models.CharField(max_length=100,verbose_name='产品品牌',validators=[MinLengthValidator(1),],help_text='产品品牌')
    thumbnail = models.URLField(default="",verbose_name='图片URL',help_text='图片URL')
    version = models.CharField(max_length=200,validators=[MinLengthValidator(1),],verbose_name='产品型号')
    describe = models.CharField(max_length=200,verbose_name='产品描述',validators=[MinLengthValidator(1),],help_text='产品描述')
    clicks = models.IntegerField(default=0, verbose_name='点击量', help_text='点击量')
    category = models.ForeignKey('ProductCategory', on_delete=models.SET_NULL,null=True,blank=True, related_name='products',verbose_name='产品分类')

    def __str__(self):
        return self.brand

    class Meta:
        ordering = ['-update_time', '-id']
        db_table='tb_products'
        verbose_name = '产品信息'
        verbose_name_plural = verbose_name

class Banner(ModelBase):
    '''
    the banner of the index of news
    '''
    PRI_CHOICE=[
        (1,'第一级'),
        (2,'第二级'),
        (3,'第三级'),
        (4,'第四级'),
        (5,'第五级'),
        (6,'第六级'),
    ]
    image_url=models.URLField(verbose_name='图片URL',help_text='图片URL')
    priority = models.IntegerField(choices=PRI_CHOICE,default=6,verbose_name='优先级', help_text='优先级')
    link_to=models.URLField(verbose_name='链接',help_text='链接')

    class Meta:
        ordering=['priority','-update_time','-id']
        db_table='tb_banner'
        verbose_name='轮播图'
        verbose_name_plural=verbose_name
