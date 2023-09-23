from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms

from io import BytesIO

from app01 import models
from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5
from app01.utils.code import check_code


class LoginForm(BootStrapForm):
    # required=True默认不为空，必填, render_value=True验证密码错误的时候不会清空
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():

        # 验证码校验 使用pop的原因是下面**form.cleaned_data会去数据库进行校验，而数据库中没code这个字段但是cleaned_data里面有，所以用pop在获取的同时进行剔除
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', '')
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {"form": form})

        # form.cleaned_data 就是验证成功后，获取到的用户名和密码
        # 去数据库验证用户名和密码是否正确，获取用户对象， none
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            # 与数据库的数据进行比较，若不符合则admin_object就为空，这样就返回到原页面
            return render(request, 'login.html', {"form": form})

        # 验证正确
        # 网站生成随机字符串，写到用户浏览器的cookie中，在写入到session中
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}
        # 设置session信息保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("/admin/list/")

    return render(request, 'login.html', {"form": form})


def logout(request):
    request.session.clear()
    return redirect('/index/')


def image_code(request):
    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中 （以便于后续获取验证码在进行校验）
    request.session['image_code'] = code_string
    # 给session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def index(request):
    return render(request, "index.html")
