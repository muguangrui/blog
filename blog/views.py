from django.shortcuts import render,HttpResponse

# Create your views here.
from blog.utils.get_code_img import get_validCode_img

def login(request):


    return render(request, 'blog/login.html')


def get_valid_code_img(request):

    data = get_validCode_img(request)
    return HttpResponse(data)