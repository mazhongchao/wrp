from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from .models import Feedback, Notes


# Register your models here.
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'description', 'updated_at')
    search_fields = ('title', 'type')
    radio_fields = {'type': admin.HORIZONTAL}


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'staff_name', 'updated_at')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("user",)
        form = super(FeedbackAdmin, self).get_form(request, obj, **kwargs)
        return form

    def staff_name(self, obj):
        user_name = f'{obj.user.first_name} {obj.user.last_name}'
        return format_html('<span>{}<span>', user_name)

    staff_name.short_description = '反馈人'

    def get_readonly_fields(self, request, obj):
        # view and change
        if obj:
            if obj.user.username != request.user.username:
                self.readonly_fields = ('title', 'description', 'staff_name')
            else:
                self.readonly_fields = ()
        else:
            self.readonly_fields = ()

        return self.readonly_fields

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if obj:
            if obj.user.username != request.user.username:
                context.update({
                    'show_save': False,
                    'show_save_and_add_another': False,
                    'show_save_and_continue': False,
                    'show_delete': False
                })
        # else:
        #     pass

        return super().render_change_form(request, context, add, change, form_url, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = get_user_model().objects.filter(
                username=request.user.username
            )
        return super(FeedbackAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def add_view(self, request, form_url="", extra_context=None):
        data = request.GET.copy()
        data["user"] = request.user
        request.GET = data
        return super(FeedbackAdmin, self).add_view(
            request, form_url="", extra_context=extra_context
        )


admin.site.register(Notes, NoteAdmin)
admin.site.register(Feedback, FeedbackAdmin)
