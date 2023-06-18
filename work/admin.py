from django import forms
from django.apps import apps
from django.contrib import admin
from django.utils.html import format_html
from .models import Log, Plan
from wrp import utils


# Register your models here.
class LogForm(forms.ModelForm):
    def clean(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']

        t_delta = end_time - start_time
        if t_delta.days < 1 and t_delta.seconds < 1800:
            raise forms.ValidationError({'end_time': "开始时间和完成时间差过小"})


class LogAdmin(admin.ModelAdmin):
    form = LogForm
    list_display = ('title', 'plan_text', 'zone', 'nature',  'way', 'start_time', 'end_time')
    fields = ('plan_status', 'title', 'zone', 'nature', 'way', 'start_time', 'end_time')
    radio_fields = {'nature': admin.HORIZONTAL}
    readonly_fields = ('plan_status',)
    # autocomplete_fields = ('zone',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.expected_start_time = obj.start_time
        obj.expected_end_time = None
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("user", "expected_start_time", "expected_end_time")
        form = super(LogAdmin, self).get_form(request, obj, **kwargs)
        return form

    def plan_text(self, obj):
        if obj.is_plan == 1:
            return format_html('<span style="color:#{};font-weight:bold">{}<span>', "f25d25", "是")
        return format_html('<span style="color:#{}">{}<span>', "9c9c9c", "否")

    plan_text.short_description = "上周计划"

    def plan_status(self, obj):
        if obj.is_plan == 1:
            return format_html('<span style="color:#{};font-weight:bold">{}<span>', "f25d25", "是上周计划的工作")
        return format_html('<span style="color:#{};">{}<span>', "9c9c9c", "非上周计划的工作")

    plan_status.short_description = '计划情况'

    def get_queryset(self, request):
        this_week_start, this_week_end = utils.this_week_range()

        qs = super(LogAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(start_time__range=(this_week_start, this_week_end))
        return qs.filter(user=request.user, start_time__range=(this_week_start, this_week_end))


class PlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'zone', 'nature', 'expected_start_time', 'expected_end_time')
    # list_editable = ['title']
    radio_fields = {'nature': admin.HORIZONTAL}

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.is_plan = 1
        obj.start_time = obj.expected_start_time
        obj.end_time = None
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("user", "is_plan", "start_time", "end_time", "detail")
        form = super(PlanAdmin, self).get_form(request, obj, **kwargs)
        return form

    def get_queryset(self, request):
        last_week_start, last_week_end = utils.next_week_range()

        qs = super(PlanAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(start_time__range=(last_week_start, last_week_end))
        return qs.filter(user=request.user, start_time__range=(last_week_start, last_week_end))


admin.site.register(Log, LogAdmin)
admin.site.register(Plan, PlanAdmin)

