from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def hello_old(request):
    return HttpResponse("Hello world")


def hello(request):
    return render(
        request,
        "users/hello.html",
        {
            "message": "Hello world"
        }
    )
