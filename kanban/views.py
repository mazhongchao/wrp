import os
import json
from random import randrange
from django.utils.encoding import escape_uri_path
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig, RenderType

# CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./kanban/templates/pyecharts"))

from pyecharts import options as opts
from pyecharts.charts import Bar, Pie
from pyecharts.faker import Faker

import pdfkit
from work.models import Log
from conf.models import Zone
from wrp import utils
from wrp import settings


CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./kanban/templates/pyecharts"))
# Create your views here.


def team_sta(request):
    this_week_start, this_week_end = utils.this_week_range()

    users_name, users_count = _staff_work_count()

    work_count_bar = (
        Bar().add_xaxis(users_name)
        .add_yaxis("工作项数", users_count)
        .set_global_opts(title_opts=opts.TitleOpts(title="工作量统计", subtitle=""))
    )

    zones = Zone.objects.all()
    worklog = Log.objects.filter(start_time__gte=this_week_start, start_time__lte=this_week_end)

    zone_sta = {}
    for zone in zones:
        zone_sta[zone.id] = [zone.name, 0]

    for work in worklog:
        if work.zone_id in zone_sta:
            zone_sta[work.zone_id][1] = zone_sta[work.zone_id][1] + 1

    zone_count_pie = (
        Pie()
        .add("", [list(z) for z in zone_sta.values()], radius="60%")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="工作域统计"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )

    context = {'work_count_data': work_count_bar.dump_options(), 'project_count_data': zone_count_pie.dump_options()}
    return render(request, 'team_sta.html', context=context)


def work_report(request):
    context = _report_data()
    return render(request, 'work_report.html', context)


def work_report_pdf(request):

    context = _report_data()

    # find the template and render it.
    template_path = 'work_report_pdf.html'
    template = get_template(template_path)
    html = template.render(context)

    file_name = 'work_report.pdf'
    pdf_file = f'{os.path.abspath(os.path.dirname(os.path.dirname(__file__)))}/static/{file_name}'
    print(pdf_file)

    # 通过网页生成PDF
    try:
        config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
        pdfkit.from_url('http://127.0.0.1:8000/kanban/kanban/work_report_preview', pdf_file,
                        options={'encoding': "utf-8", 'javascript-delay': 500},
                        configuration=config)
    except Exception as e:
        return HttpResponse('PDF生成失败：'+str(e))

    file_name = f"产品技术部工作周报-{utils.today_date('.')}"
    report_file = open(pdf_file, 'rb')
    response = FileResponse(report_file)
    response['Content-Type'] = 'application/pdf'
    # response = HTTPResponse(report_file)
    # response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename="{escape_uri_path(file_name)}.pdf"'

    return response


def work_report_preview(request):
    context = _report_data()

    users_name, users_count = _staff_work_count()
    work_count_bar = (
        Bar(init_opts=opts.InitOpts(renderer=RenderType.SVG,
                                    animation_opts=opts.AnimationOpts(animation=False)))
        .add_xaxis(users_name)
        .add_yaxis("工作项数", users_count)
        .set_global_opts(title_opts=opts.TitleOpts(title="工作量统计", subtitle=""))
    )
    context['work_count_data'] = work_count_bar.dump_options()
    return render(request, 'work_report_preview.html', context)


def _staff_work_count():
    users = User.objects.all()

    work_count = {}
    users_name = []
    users_count = []
    for user in users:
        if user.id in settings.STA_EXCLUDE_USER_ID:
            continue
        work_count[user.id] = [f'{user.first_name}{user.last_name}', 0]

    this_week_start, this_week_end = utils.this_week_range()
    work_sta = Log.objects.filter(start_time__gte=this_week_start,
                                  start_time__lte=this_week_end).values('user_id')
    for sta in work_sta:
        user_id = sta['user_id']
        if user_id not in work_count:
            work_count[user_id][1] = 1
        else:
            work_count[user_id][1] = work_count[user_id][1] + 1

    for value in work_count.values():
        users_name.append(value[0])
        users_count.append(value[1])

    return users_name, users_count


def _report_data():
    this_week_start, this_week_end = utils.this_week_range()

    natures = {1: '主线工作', 2: '支持工作', 3: '临时工作'}
    users = User.objects.all()
    zones = Zone.objects.all()
    worklog = Log.objects.filter(start_time__gte=this_week_start, start_time__lte=this_week_end)

    users_dict = {}
    for user in users:
        if user.id in settings.STA_EXCLUDE_USER_ID:
            continue

        if user.id not in users_dict:
            users_dict[user.id] = f'{user.first_name}{user.last_name}'

    zone_dict = {}
    for zone in zones:
        if zone.id not in zone_dict:
            zone_dict[zone.id] = zone.name

    # 本周工作
    zone_logs = {}
    for work in worklog:
        work.user_name = users_dict[work.user_id]
        work.nature_name = natures[work.nature_id]

        if work.end_time is not None:
            work.status = '完成'
            work.duration = utils.work_duration(work.start_time, work.end_time)
            work.end_time = work.end_time.strftime('%m-%d %H:%M')
        else:
            work.status = '未完成'
            work.duration = '-'
            work.end_time = '-'

        work.start_time = work.start_time.strftime('%m-%d %H:%M')

        zone_id = work.zone_id
        if zone_id in zone_logs:
            if work.user_id in zone_logs[zone_id]['works']:
                zone_logs[zone_id]['works'][work.user_id].append(work)
            else:
                zone_logs[zone_id]['works'][work.user_id] = [work]
        else:
            zone_logs[zone_id] = {}
            zone_logs[zone_id]['name'] = zone_dict[zone_id]
            zone_logs[zone_id]['works'] = {}

            if work.user_id in zone_logs[zone_id]['works']:
                zone_logs[zone_id]['works'][work.user_id].append(work)
            else:
                zone_logs[zone_id]['works'][work.user_id] = [work]

        num = 1
        for zone_work in zone_logs.values():
            zone_work['num'] = num
            num = num + 1

    # 下周计划
    next_week_start, next_week_end = utils.next_week_range()
    worklog = Log.objects.filter(expected_start_time__gte=next_week_start, expected_start_time__lte=next_week_end)
    work_plans = {}
    for user_id, user_name in users_dict.items():
        work_plans[user_id] = {'user_name': user_name, 'plan_list': []}

    for plan in worklog:
        if plan.user_id in work_plans:
            plan.expected_start_time = plan.expected_start_time.strftime('%m-%d')
            plan.expected_end_time = plan.expected_end_time.strftime('%m-%d')
            work_plans[plan.user_id]['plan_list'].append(plan)

    return {"zone_logs": zone_logs, "work_plans": work_plans,
            "this_week_start": this_week_start, "this_week_end": this_week_end}


def chart_temp_1_view(request):
    chart = (
        Bar().add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
        .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return render(request, 'chart_temp_1.html', context={'chart_data': chart.dump_options()})


def chart_temp_2_view(request):
    return render(request, 'chart_temp_2.html')


def chart_temp_2_json(request):
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
        .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
        .dump_options_with_quotes()
    )
    return json_response(json.loads(c))


def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)
