# Generated by Django 4.2.1 on 2023-06-10 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('description', models.IntegerField(blank=True, default='', verbose_name='详细描述')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '反馈',
                'verbose_name_plural': '反馈',
            },
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('type', models.IntegerField(choices=[(1, '版本发布'), (2, '使用说明')], verbose_name='类型')),
                ('description', models.IntegerField(blank=True, default='', verbose_name='内容')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '说明',
                'verbose_name_plural': '说明',
            },
        ),
    ]
