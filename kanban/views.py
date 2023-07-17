import os
from django.utils.encoding import escape_uri_path
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.contrib.auth.models import User
from django.template.loader import get_template
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig, RenderType
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie
import pdfkit
from work.models import Log
from conf.models import Zone
from wrp import utils
from wrp import settings

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./kanban/templates/pyecharts"))
# Create your views here.


def team_sta(request):
    users_name, users_count = _staff_work_count()

    work_count_bar = (
        Bar().add_xaxis(users_name)
        .add_yaxis("工作项数", users_count)
        .set_global_opts(title_opts=opts.TitleOpts(title="工作量统计", subtitle=""))
    )

    zone_sta = _zone_work_count()

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

    template_path = 'work_report_pdf.html'
    template = get_template(template_path)
    html = template.render(context)

    file_name = 'work_report.pdf'
    pdf_file = f'{os.path.abspath(os.path.dirname(os.path.dirname(__file__)))}/static/{file_name}'
    print(pdf_file)

    # to generate PDF from web page url
    try:
        url = settings.SITE_HOST + '/kanban/kanban/work_report_preview'
        print(url)
        config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
        pdfkit.from_url(url, pdf_file,
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
                                  start_time__lte=this_week_end,
                                  ).values('user_id')

    for sta in work_sta:
        user_id = sta['user_id']
        if user_id in settings.STA_EXCLUDE_USER_ID:
            continue

        if user_id not in work_count:
            work_count[user_id][1] = 1
        else:
            work_count[user_id][1] = work_count[user_id][1] + 1

    for value in work_count.values():
        users_name.append(value[0])
        users_count.append(value[1])

    return users_name, users_count


def _zone_work_count():
    this_week_start, this_week_end = utils.this_week_range()

    zones = Zone.objects.all()
    worklog = Log.objects.filter(start_time__gte=this_week_start, start_time__lte=this_week_end)

    zone_sta = {}
    for zone in zones:
        zone_sta[zone.id] = [zone.name, 0]

    for work in worklog:
        if work.zone_id in zone_sta:
            zone_sta[work.zone_id][1] = zone_sta[work.zone_id][1] + 1

    return zone_sta


# def _report_chart_image():
#     users_name, users_count = _staff_work_count()
#     zone_work_count = _zone_work_count()
#     pie_values = []
#     pie_labels = []
#     colors = ["#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#e6ab02"]
#     for v in zone_work_count.values():
#         pie_labels.append(v[0])
#         pie_values.append(v[1])
#
#     fig = plt.figure()
#     ax = fig.add_axes([0, 0, 1, 1])
#     ax.bar(users_name, users_count)
#     image_dir = settings.BASE_DIR / "static/tmp"
#     plt.savefig(f'{image_dir}/bar_work_count.png', dpi=500)
#
#     plt.figure(figsize=(8, 6))
#     wedges, texts, autotexts = plt.pie(pie_values, labels=pie_labels, autopct='%1.1f%%')
#     plt.legend(wedges, pie_labels, title="工作域", loc="center left",
#                bbox_to_anchor=(1, 0, 0.5, 1))
#     plt.title('工作域统计')
#     plt.axis('equal')
#     plt.savefig(f'{image_dir}/pie_zone_count.png', dpi=500)


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
        if work.user_id in settings.STA_EXCLUDE_USER_ID:
            continue

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
    worklog = Log.objects.filter(expected_start_time__gte=next_week_start, expected_start_time__lte=next_week_end,
                                 is_plan=1)
    work_plans = {}
    for user_id, user_name in users_dict.items():
        work_plans[user_id] = {'user_name': user_name, 'plan_list': []}

    for plan in worklog:
        if plan.user_id in work_plans:
            plan.expected_start_time = plan.expected_start_time.strftime('%m-%d')
            if plan.expected_end_time is not None:
                plan.expected_end_time = plan.expected_end_time.strftime('%m-%d')
            else:
                plan.expected_end_time = '未知'
            work_plans[plan.user_id]['plan_list'].append(plan)

    return {"zone_logs": zone_logs, "work_plans": work_plans,
            "this_week_start": this_week_start, "this_week_end": this_week_end}
