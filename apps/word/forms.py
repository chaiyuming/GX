import logging
import re

from django import forms
from django_redis import get_redis_connection
from django.db.models import Q
from . import models


class ClientWordsForm(forms.Form):
    '''
    Verfily client word form
    '''
    telephone = forms.CharField(min_length=11, max_length=11, required=True, error_messages={
        'required': '请输入正确的手机号码^_^',
        'min_length': '手机号码必须为11位',
        'max_length': '手机号码必须为11位',
    })
    username = forms.CharField(required=True, error_messages={
        'required': '请输入姓名^_^',
    })
    content = forms.CharField(required=True, error_messages={
        'required': '请输入内容^_^',
    })
    email=forms.EmailField()
    def clean_username(self):
        '''
        check username
        :return:
        '''
        username=self.cleaned_data.get('username')
        exists=models.ClientWords.objects.filter(username=username).exists()
        if exists:
            raise forms.ValidationError('该用户名已注册，请重新输入')
        return username
    def clean_telephone(self):
        '''
        check telephone
        :return:
        '''
        tel=self.cleaned_data.get('telephone')
        if not re.match(r"^1[3-9]\d{9}$",tel):
            raise forms.ValidationError('手机号码格式不正确')
        exists=models.ClientWords.objects.filter(telephone=tel).exists()
        if exists:
            raise forms.ValidationError('该手机号已注册，请重新输入')
        return tel
