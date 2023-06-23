from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Feedback(models.Model):
    title = models.CharField('标题', max_length=200, blank=True, default='')
    description = models.TextField('详细描述', blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    title = models.CharField('标题', max_length=200)
    type = models.IntegerField('类型', choices=NotesType.choices)
    description = models.TextField('内容', blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # META类选项
    class Meta:
        verbose_name = '说明'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
