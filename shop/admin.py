from django.contrib import admin

# Register your models here.
from .models import product , Order, OrderItem, Customer

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(product)