from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import Zone, Nature, Way


class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'updated_at')
    # search_fields = ('name', 'type')
    radio_fields = {'type': admin.HORIZONTAL}


class NatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'updated_at')


class WayAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_at')


admin.site.register(Zone, ZoneAdmin)
admin.site.register(Nature)
admin.site.register(Way)

admin.site.site_title = 'WRP系统'
admin.site.site_header = 'WRP(0.1)'
admin.site.index_title = 'WRP'
