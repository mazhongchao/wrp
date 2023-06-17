from django.contrib import admin
from .models import TeamSta, Report
from .views import team_sta, work_report

# Register your models here.


class TeamStaAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_content=None):
        return team_sta(request)


class ReportAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_content=None):
        return work_report(request)


admin.site.register(TeamSta, TeamStaAdmin)
admin.site.register(Report, ReportAdmin)
