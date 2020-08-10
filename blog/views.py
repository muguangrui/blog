from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.contrib import auth
# Create your views here.
from blog.utils.get_code_img import get_validCode_img
from blog.utils.myforms import UserForm
from blog.models import *
def login(request):

    if request.method == "POST":
        response = {"user": None, "msg":None}
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        valid_code = request.POST.get("valid_code")
        valid_code_str = request.session.get("valid_code_str")
        if valid_code.upper() == valid_code_str.upper():
            user_obj = auth.authenticate(username=user,password=pwd)
            if user_obj:
                auth.login(request,user_obj)
                response["user"] = request.user.username
                next_url = request.GET.get("next", "/index/")
                response["next_url"] = next_url
            else:
                response["msg"] = "用户名或密码错误！"
        else:
            response["msg"] = "验证码错误！"
        return  JsonResponse(response)

    return render(request, 'blog/login.html')


def get_valid_code_img(request):

    data = get_validCode_img(request)
    return HttpResponse(data)


def index(request):

    article_list = Article.objects.all()

    return render(request, 'blog/index.html', locals())


def register(request):

    if request.method == "POST":
        form = UserForm(request.POST)
        response = {"user": None, "msg": None}
        if form.is_valid():
            response["user"] = form.cleaned_data.get("user")
            # print(form.cleaned_data)
            # 生成一条用户记录
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avatar_obj = request.FILES.get("avatar")
            extra = {}
            if avatar_obj:
                extra["avatar"] = avatar_obj
            UserInfo.objects.create_user(username=user, password=pwd,email=email, **extra)

        else:
            response["msg"] = form.errors
        return JsonResponse(response)

    form = UserForm()
    return render(request,'blog/register.html',locals())


def logout(request):
    auth.logout(request)
    return redirect('/login/')
