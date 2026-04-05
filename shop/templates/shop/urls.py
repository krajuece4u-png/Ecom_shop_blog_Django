from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('productview/', views.productview, name='productview'),
    path('checkout', views.checkout, name='checkout'), 
]