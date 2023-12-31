from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django import forms
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5


def admin_list(request):
    """ 管理员列表 """
    # 构造搜索
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["username__contains"] = search_data
    # 根据搜索条件去数据库中获取
    queryset = models.Admin.objects.filter(**data_dict)
    # 分页
    page_object = Pagination(request, queryset)
    content = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'search_data': search_data,
    }
    return render(request, "admin_list.html", content)


class AdminModelForm(BootStrapModelForm):
    # 添加一个数据库中不存在的字段 为确认密码 并将密码的显示换成***
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        # 将密码的显示改为**
        widgets = {
            "password": forms.PasswordInput
        }

    # 对密码进行加密 再保存到数据库
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    # 使用钩子获取两次输入的密码，并进行比较
    def clean_confirm_password(self):
        # 获取到的pwd就是上面已经加密过的密码了
        pwd = self.cleaned_data.get("password")
        # 获取确认密码
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致，请重新输入")
        return confirm


def admin_add(request):
    """ 添加管理员 """
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "change.html", {'form': form, "title": title})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, "change.html", {'form': form, "title": title})


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username', 'password']


def admin_edit(request, nid):
    """ 编辑管理员 """
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, "error.html", {"msg": "数据不存在"})

    title = "编辑管理员"
    if request.method == "GET":
        # instance=row_object 将默认值填入里面
        form = AdminEditModelForm(instance=row_object)
        return render(request, "change.html", {"form": form, "title": title})
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, "change.html", {"form": form, "title": title})


def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        # 将密码的显示改为**
        widgets = {
            "password": forms.PasswordInput
        }

    # 对密码进行加密 再保存到数据库
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        # 去数据库校验当前密码和新输入的密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("不能与之前密码一致")
        return md5_pwd

    # 使用钩子获取两次输入的密码，并进行比较
    def clean_confirm_password(self):
        # 获取到的pwd就是上面已经加密过的密码了
        pwd = self.cleaned_data.get("password")
        # 获取确认密码
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致，请重新输入")
        return confirm


def admin_reset(request, nid):
    """ 重置密码  """
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')
    title = "重置密码 - {}".format(row_object.username)
    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'change.html', {"form": form, "title": title})
    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {"form": form, "title": title})
