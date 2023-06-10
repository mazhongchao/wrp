from django.db import models
from django.contrib.auth.models import User


class ZoneType(models.IntegerChoices):
    PRODUCT = 1, '产品'
    PROJECT = 2, '项目'
    SERVICE = 3, '服务'


class Zone(models.Model):
    name = models.CharField('工作域', max_length=100)
    type = models.IntegerField('工作域类型', choices=ZoneType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # META类选项
    class Meta:
        verbose_name = '工作域'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Nature(models.Model):
    name = models.CharField('工作性质', max_length=10)
    description = models.CharField('说明', max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # META类选项
    class Meta:
        verbose_name = '工作性质'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Way(models.Model):
    name = models.CharField('工作形式', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # META类选项
    class Meta:
        verbose_name = '工作形式'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

