from django import forms

from apps.product.models import Products,ProductCategory
from apps.news.models import News

class AddProductForm(forms.ModelForm):
    thumbnail=forms.URLField(label='产品图片url',error_messages={"required": "产品图片url不能为空"})
    top_tag_id=forms.IntegerField(label='产品一级分类',error_messages={"required": "产品一级分类id不能为空"})
    sub_tag_id=forms.IntegerField(label='产品二级分类',error_messages={"required": "产品二级分类id不能为空"})
    class Meta:
        model=Products
        fields=['brand','thumbnail','version','describe']
        error_messages = {
            'brand': {
                'max_length': "产品品牌长度不能超过100",
                'min_length': "产品品牌长度大于1",
                'required': '产品品牌不能为空',
            },
            'version': {
                'max_length': "产品型号长度不能超过200",
                'min_length': "产品型号长度大于1",
                'required': '产品型号不能为空',
            },
            'describe': {
                'max_length': "产品描述长度不能超过200",
                'min_length': "产品描述长度大于1",
                'required': '产品描述不能为空',
            },
        }

class PubNewsForm(forms.ModelForm):
    class Meta:
        model=News
        fields=['title','content']
        error_messages={
            'title': {
                'max_length': "文章标题长度不能超过200",
                'min_length': "文章标题长度大于1",
                'required': '文章标题不能为空',
            },
            'content': {
                'required': '文章内容不能为空',
            },
        }