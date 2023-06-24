from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Feedback(models.Model):
    title = models.CharField('反馈标题', max_length=200, blank=True, default='')
    description = models.TextField('反馈信息', blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    # META类选项
    class Meta:
        verbose_name = '反馈'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class NotesType(models.IntegerChoices):
    PRODUCT = 1, '版本发布说明'
    PROJECT = 2, '系统使用说明'


class Notes(models.Model):
    title = models.CharField('说明标题', max_length=200)
    type = models.IntegerField('说明类型', choices=NotesType.choices)
    description = models.TextField('说明内容', blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    # META类选项
    class Meta:
        verbose_name = '说明'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
