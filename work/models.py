from django.db import models
from django.contrib.auth.models import User

from conf.models import Zone, Nature, Way


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='姓名')
    is_plan = models.IntegerField('是否上周计划', default=0)
    title = models.CharField('工作事项', max_length=200)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, verbose_name='工作域')
    nature = models.ForeignKey(Nature, on_delete=models.CASCADE, verbose_name='工作性质')
    way = models.ForeignKey(Way, on_delete=models.CASCADE, verbose_name='工作形式')
    expected_start_time = models.DateTimeField('预计开始时间')
    expected_end_time = models.DateTimeField('预计完成时间', null=True)
    start_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('完成时间', blank=True, null=True)
    for_who = models.CharField('提出人(对于非主线工作)', max_length=100, default='', blank=True)
    detail = models.TextField('详细记录', blank=True, default='')

    # META类选项
    class Meta:
        verbose_name = '本周工作'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Plan(Log):
    # META类选项
    class Meta:
        verbose_name = '下周计划'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Review:
    class Meta:
        verbose_name = '上周回顾'
        verbose_name_plural = verbose_name
