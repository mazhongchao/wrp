from django.db import models

# Create your models here.


class TeamSta(models.Model):
    class Meta:
        verbose_name = '团队汇总'
        verbose_name_plural = verbose_name


class Report(models.Model):
    class Meta:
        verbose_name = '本周报告'
        verbose_name_plural = verbose_name
