from django.contrib.admin.apps import AdminConfig


class WrpAdminConfig(AdminConfig):
    default_site = "wrp.admin.WrpAdminSite"
