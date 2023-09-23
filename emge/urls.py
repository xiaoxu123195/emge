from django.contrib import admin
from django.urls import path

from app01.views import depart, pretty, user, admin, account, task, order, chart

urlpatterns = [
    # path("admin/", admin.site.urls),
    # 部门管理
    # http://127.0.0.1:8000/depart/list/
    path("depart/list/", depart.depart_list),
    path("depart/add/", depart.depart_add),
    path("depart/delete/", depart.depart_delete),
    # http://127.0.0.1:8000/depart/2/list/ 也就是说在depart后面必须有一个数字
    path("depart/<int:nid>/edit/", depart.depart_edit),
    # 用户管理
    path("user/list/", user.user_list),
    path("user/add/", user.user_add),
    path("user/model/form/add/", user.user_model_form_add),
    path("user/<int:nid>/edit/", user.user_edit),
    path("user/<int:nid>/delete/", user.user_delete),
    # 靓号管理
    path("pretty/list/", pretty.pretty_list),
    path("pretty/add/", pretty.pretty_add),
    path("pretty/<int:nid>/edit/", pretty.pretty_edit),
    path("pretty/<int:nid>/delete/", pretty.pretty_delete),
    # 管理员管理
    path("admin/list/", admin.admin_list),
    path("admin/add/", admin.admin_add),
    path("admin/<int:nid>/edit/", admin.admin_edit),
    path("admin/<int:nid>/delete/", admin.admin_delete),
    path("admin/<int:nid>/reset/", admin.admin_reset),
    # 登录
    path("", account.index),
    path("login/", account.login),
    path("logout/", account.logout),
    path("image/code/", account.image_code),
    # 任务管理
    path('task/list/', task.task_list),
    path('task/add/', task.task_add),
    # 订单管理
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),
    path('order/detail/', order.order_detail),
    path('order/edit/', order.order_edit),
    # 数据统计
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),
    path('chart/pie/', chart.chart_pie),
    path('chart/line/', chart.chart_line),
    path('chart/highcharts/', chart.highcharts),
]
