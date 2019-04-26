from django.db import models
from  utils.models import ModelBase
from django.core.validators import MinLengthValidator
# Create your models here.

class News(ModelBase):
    title=models.CharField(max_length=200,validators=[MinLengthValidator(1),],verbose_name='新闻标题')
    content = models.TextField(verbose_name='内容', help_text='内容')

    author = models.ForeignKey('users.Users', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-update_time', '-id']
        db_table='tb_news'
        verbose_name='新闻咨询'
        verbose_name_plural=verbose_name



