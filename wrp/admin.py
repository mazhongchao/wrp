from django.contrib import admin


apps_index = ["kanban", "work", "conf", "system", "auth"]
models_index = {'kanban': ["TeamSta", "Report"], 'work': ["Log", "Plan"], 'conf': ["Zone", "Nature", "Way"],
                'system': ["Notes", "Feedback"], 'auth': ["User", "Group"]}


class WrpAdminSite(admin.AdminSite):
    site_title = 'WRP系统'
    site_header = 'WRP(0.2)'
    index_title = 'WRP'

    # apps_order_list = ["kanban", "work", "conf", "system", "auth"]
    # apps_order_dict = {app: index for index, app in enumerate(apps_order_list)}

    def get_app_list(self, request, app_label=None):
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

        new_sorted_apps = []
        for app in app_list:
            app_name = app['app_label']
            pos = apps_index.index(app_name)
            new_sorted_apps.append({"pos": pos, "app": app})

            new_sorted_models = []
            models = app["models"]
            for model in models:
                model_name = model["object_name"]
                idx = models_index[app_name].index(model_name)
                new_sorted_models.append({"pos": idx, "model": model})

            new_sorted_models.sort(key=lambda s: s["pos"])
            models = [x["model"] for x in new_sorted_models]
            app["models"] = models
        print(new_sorted_models)
        new_sorted_apps.sort(key=lambda x: x["pos"])
        print(new_sorted_apps)
        app_list = [a["app"] for a in new_sorted_apps]
        print(app_list)

        return app_list
