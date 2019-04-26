from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager as _UserManager,User

# Create your models here.
class UserManager(_UserManager):
    def create_superuser(self,username,password,email=None,**extra_fields):
        super().create_superuser(username=username,password=password,email=email,**extra_fields)
class Users(AbstractUser):
    '''
    add telephone,email_active fields to users models.
    '''
    telephone=models.CharField(max_length=11,unique=True,verbose_name='手机号码',help_text='手机号码',error_messages={
        'unique':'此手机号码已注册'
    })
    email_active =models.BooleanField(default=False,verbose_name='邮箱状态')

    REQUIRED_FIELDS = ['telephone']
    objects = UserManager()

    class Meta:
        db_table='tb_users'
        verbose_name='用户'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.username
