from django.contrib import admin
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('productview/', views.productview, name='productview'),
    path('checkout', views.checkout, name='checkout'),
    path('search', views.search, name='search'),
    path('tracker', views.tracker, name='tracker'),
    path('cart/', views.cart, name='cart'),
    path('charts/', views.charts, name='charts'),
    path('orders/', views.order_history, name='order_history'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/<str:action>/', views.update_cart, name='update_cart'),
]