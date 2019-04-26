from django.db import models
from utils.models import ModelBase
from django.core.validators import MinLengthValidator

# Create your models here.
class ClientWords(ModelBase):
    username=models.CharField(max_length=100,verbose_name='客户姓名',help_text='客户姓名')
    email=models.EmailField(null=True,verbose_name='客户邮箱',help_text='客户邮箱')
    telephone=models.CharField(max_length=11,unique=True,help_text='客户手机号码',verbose_name='客户手机号码',
                               error_messages={
                                   'unique':'此手机号码已经注册'
                               })
    content=models.TextField(verbose_name='留言内容',help_text='留言内容')
    class Meta:
        ordering=['-create_time','-id']
        db_table='tb_client_word'
        verbose_name='客户留言'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.title