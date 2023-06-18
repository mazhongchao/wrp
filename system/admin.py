from django.contrib import admin
from .models import Feedback, Notes


# Register your models here.
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'description', 'updated_at')
    search_fields = ('title', 'type')
    radio_fields = {'type': admin.HORIZONTAL}


admin.site.register(Notes, NoteAdmin)
admin.site.register(Feedback, FeedbackAdmin)


apps_index = ["kanban", "work", "conf", "system", "auth"]
models_index = {'kanban': ["TeamSta", "Report"], 'work': ["Log", "Plan"], 'conf': ["Zone", "Nature", "Way"],
                'system': ["Notes", "Feedback"], 'auth': ["User", "Group"]}


def index_decorator(func):
    def inner(*args, **kwargs):
        template_response = func(*args, **kwargs)
        app_list = template_response.context_data['app_list']
        new_sorted_app = []
        for app in app_list:
            app_name = app['app_label']
            pos = apps_index.index(app_name)
            new_sorted_app.append({"pos": pos, "app": app})

            new_sorted_models = []
            models = app["models"]
            for model in models:
                model_name = model["object_name"]
                idx = models_index[app_name].index(model_name)
                new_sorted_models.append({"pos": idx, "model": model})

            new_sorted_models.sort(key=lambda s: s["pos"])
            models = [x["model"] for x in new_sorted_models]
            app["models"] = models

        new_sorted_app.sort(key=lambda x: x["pos"])
        app_list = [a["app"] for a in new_sorted_app]
        template_response.context_data['app_list'] = app_list

        return template_response

    return inner


admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)

admin.site.site_title = 'WRP系统'
admin.site.site_header = 'WRP(0.2)'
admin.site.index_title = 'WRP'

