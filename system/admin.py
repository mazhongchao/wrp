from django.contrib import admin
from .models import Feedback, Notes


# Register your models here.
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'description', 'updated_at')
    search_fields = ('title', 'type')
    radio_fields = {'type': admin.HORIZONTAL}


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Notes, NoteAdmin)
