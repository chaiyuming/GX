import re
import logging

from django import forms
from django_redis import get_redis_connection
from django.db.models import Q
from django.contrib.auth import login,logout,authenticate

from .models import Users

class LoginForm(forms.Form):
    '''
    user login verfication from
    '''
    user_account=forms.CharField()
    password=forms.CharField(label='用户密码',max_length=20,min_length=6,error_messages={
        'required': '必须填入密码',
        'min_length': '密码长度不能少于6位',
        'max_length': '密码长度不能大于20位',
    })
    # remember=forms.BooleanField(required=False)
    def __init__(self,*args,**kwargs):
        '''
        recive  request form views
        :param args:
        :param kwargs:
        '''
        self.request=kwargs.pop('request',None)
        super().__init__(*args,**kwargs)
    def clean_user_account(self):
        '''
        check user_account
        :return:
        '''
        user_info=self.cleaned_data.get('user_account')
        if not user_info:
            raise forms.ValidationError('用户账号不能为空!')
        if not re.match(r"^1[3-9]]\d{9}$",user_info) and (len(user_info)<6 or len(user_info)>20):
            raise forms.ValidationError('用户账号格式不正确！')
        return user_info
    def clean(self):
        '''
        check username,telephone,password,remember
        :return:
        '''
        cleaned_data=super().clean()
        user_info=cleaned_data.get('user_account')
        pwd=cleaned_data.get('password')
        # remember=cleaned_data.get('remember')

        user_query=Users.objects.filter(Q(username=user_info) | Q(telephone=user_info))
        if user_query:
            user=user_query.first()
            if user.check_password(pwd):
                # if remember:
                #     self.request.sesson.set_expiry(None)
                # else:
                #     self.request.sesson.set_expiry(0)
                login(self.request,user)
            else:
                raise forms.ValidationError('密码有误请重新输入!')
        else:
            raise forms.ValidationError('用户账号格式错误，请检查！')

