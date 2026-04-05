from django.db import models

# Create your models here.

class student(models.Model):
    frist_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class product(models.Model):
    product_id   = models.AutoField
    product_name = models.CharField(max_length=30)
    category     = models.CharField(max_length=50, default="")
    subcategory  = models.CharField(max_length=50, default="")
    price        = models.IntegerField(default=0)
    desc         = models.CharField(max_length=60)
    put_date     = models.DateField()
    image        = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name


class Customer(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return f"{self.phone} ({self.name})" if self.name else self.phone


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} ({self.customer.phone})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity}"
    
