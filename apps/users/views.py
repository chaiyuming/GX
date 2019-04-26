import json
import logging

from django.shortcuts import render,reverse,redirect
from django.views import View
from django.contrib.auth import login,logout

from utils.json_fun import to_json_data
from utils.res_code import Code,error_map
from .forms import LoginForm
# Create your views here.

logger=logging.getLogger('inter_log')

class LoginView(View):
    '''
    login view
    '''
    def get(self,request):
        return render(request, 'users/login.html')
    def post(self,request):
        json_data=request.body
        if not json_data:
            return to_json_data(errno=Code.PARAMERR,errmsg='参数为空，请重新输入！')
        dict_data=json.loads(json_data.decode('utf8'))
        form=LoginForm(data=dict_data,request=request)
        if form.is_valid():
            print('username:',form.cleaned_data.get('user_account'))
            print('password:',form.cleaned_data.get('password'))
            return to_json_data(errmsg='登录成功!')
        else:
            err_msg_list=[]
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get('message'))
            err_msg_str='/'.join(err_msg_list)
            return to_json_data(errno=Code.PARAMERR,errmsg=err_msg_str)

class LogoutView(View):
    '''
    logout view
    '''
    def get(self,request):
        logout(request)
        return redirect('/')
