from django import forms
from django.forms import widgets
from blog.models import UserInfo
from django.core.exceptions import ValidationError

class UserForm(forms.Form):

    user = forms.CharField(max_length=32,min_length=4,label="用户名",error_messages={"required":"字段不能为空","min_length":"用户名最少为4位"},
                           widget=widgets.TextInput(attrs={"class":"form-control"}))
    pwd = forms.CharField(max_length=32, min_length=4, label="密码",
                           error_messages={"required": "字段不能为空", "min_length": "密码最少为4位"},
                           widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    re_pwd = forms.CharField(max_length=32, min_length=4, label="确认密码",
                          error_messages={"required": "字段不能为空", "min_length": "密码最少为4位"},
                          widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    email = forms.CharField(max_length=32, label="邮箱",
                          error_messages={"required": "字段不能为空"},
                          widget=widgets.EmailInput(attrs={"class": "form-control"}))


    def clean_user(self):
        val = self.cleaned_data.get("user")
        user_obj = UserInfo.objects.filter(username=val).first()
        if not user_obj:
            return val
        else:
            raise ValidationError("用户名已经被注册了！")

    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")
        if pwd and re_pwd:
            if pwd == re_pwd:
                return self.cleaned_data
            else:
                raise ValidationError("两次密码不一致")
        else:
            return self.cleaned_data