import json
import logging

from django.shortcuts import render,redirect,reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from . import models,forms
from apps.product.models import Banner,ProductCategory
from utils.json_fun import to_json_data
from utils.res_code import Code,error_map


# Create your views here.
logger=logging.getLogger('inter_log')

@method_decorator(cache_page(timeout=120, cache='page_cache'), name='dispatch')
class ClientWordsView(View):
    def get(self,request):
        banners = Banner.objects.only('id', 'image_url').filter(is_delete=False).order_by('priority', '-update_time',
                                                                                          '-id')
        top_categories = ProductCategory.objects.only('id', 'name').filter(is_delete=False, parent_id=None)
        return render(request, 'product/client_words.html', locals())
    def post(self,request):
        # 获取前端数据
        try:
            json_data = request.body
            # json.loads(a),将a转换成字典格式
            if not json_data:
                return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
            dict_data = json.loads(json_data.decode('utf8'))
        except Exception as e:
            logging.info("错误信息，\n{}".format(e))
            return to_json_data(errno=Code.UNKOWNERR,errmsg=error_map[Code.UNKOWNERR])
        form=forms.ClientWordsForm(data=dict_data)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            telephone=form.cleaned_data.get('telephone')
            content=form.cleaned_data.get('content')
            email=form.cleaned_data.get('email')
            models.ClientWords.objects.create(username=username, telephone=telephone, content=content, email=email)
            return to_json_data(errmsg='留言发布成功，稍后销售人员将会与您联系，谢谢！')
            # return redirect(reverse('word:client_words'))
        else:
            err_msg_list = []
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get('message'))
                # print(item[0].get('message'))   # for test
            err_msg_str = '/'.join(err_msg_list)  # 拼接错误信息为一个字符串
            return to_json_data(errno=Code.PARAMERR, errmsg=err_msg_str)





