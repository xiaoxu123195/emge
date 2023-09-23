from django.shortcuts import render, redirect
from app01 import models


def depart_list(request):
    # 去数据库获取所有部门列表
    queryset = models.Department.objects.all()

    return render(request, "depart_list.html", {'queryset': queryset})


def depart_add(request):
    if request.method == 'GET':
        return render(request, "depart_add.html")
    # 获取用户提交过来的数据
    title = request.POST.get('title')
    # 保存到数据库
    models.Department.objects.create(title=title)
    # 重定向回到部门列表
    return redirect("/depart/list")


def depart_delete(request):
    # 获取id
    nid = request.GET.get('nid')
    # 删除
    models.Department.objects.filter(id=nid).delete()
    # 跳转回部门列表
    return redirect('/depart/list')


def depart_edit(request, nid):
    if request.method == "GET":
        # 根据nid获取数据
        row_object = models.Department.objects.filter(id=nid).first()
        # row_object是一个列表 里面有参数id和title
        return render(request, 'depart_edit.html', {"row_object": row_object})
    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list')
