from django.urls import path
from . import views

urlpatterns = [
    path('kanban/work_report', views.work_report),
    path('kanban/work_report_pdf', views.work_report_pdf),
    path('kanban/work_report_preview', views.work_report_preview),
]
