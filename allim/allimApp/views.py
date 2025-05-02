from django.shortcuts import render

def index(request):
    return render(request,'index.html')


def Login_page(request):
    return render(request,'login.html')

def register_page(request):
    return render(request,'registration.html')
# Create your views here.
