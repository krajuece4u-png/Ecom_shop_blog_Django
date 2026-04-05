from django.shortcuts import render
from django.http import HttpResponse, request


# Create your views here.
def index(request):
    return render(request, "blog/index.html")

def home(request):
    return render(request, "blog/home.html")

def about(request):
    return render(request, "blog/about.html")
