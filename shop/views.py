from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.text import slugify
from django.templatetags.static import static
from .models import product, Customer, Order, OrderItem
from math import ceil


# Create your views here.

def index(request):
    products = product.objects.all()
    
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    # attach quantity to each product to avoid template dict lookup filter limitations
    for prod in products:
        prod.cart_qty = cart.get(str(prod.id), 0)

    # Group products by category
    from collections import defaultdict
    categories_dict = defaultdict(list)
    
    for prod in products:
        categories_dict[prod.category].append(prod)
    
    # Create slides for each category (4 products per slide)
    products_by_category = {}
    for category, prods in sorted(categories_dict.items()):
        slides = []
        for i in range(0, len(prods), 4):
            slides.append(prods[i:i+4])
        products_by_category[category] = slides

    customer = None
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer = Customer.objects.filter(id=customer_id).first()

    params = {
        'products_by_category': products_by_category,
        'cart_count': cart_count,
        'customer': customer,
    }
    return render(request, "shop/index.html", params)


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart

    target = request.GET.get('next')
    if target:
        return HttpResponseRedirect(reverse('shop:index') + target)

    prod = product.objects.filter(id=product_id).first()
    anchor = ''
    if prod and prod.category:
        anchor = '#category-' + slugify(prod.category)

    return HttpResponseRedirect(reverse('shop:index') + anchor)


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('shop:cart')

def update_cart(request, product_id, action):
    cart = request.session.get('cart', {})
    pid = str(product_id)
    qty = cart.get(pid, 0)

    if action == 'increment':
        qty += 1
    elif action == 'decrement':
        qty = max(qty - 1, 0)

    if qty <= 0:
        cart.pop(pid, None)
    else:
        cart[pid] = qty

    request.session['cart'] = cart
    return redirect('shop:cart')


def cart(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0
    for product_id, qty in cart.items():
        try:
            p = product.objects.get(id=product_id)
            line_total = p.price * qty
            image_url = p.image.url if p.image else static('shop/image/django_project.png')
            products.append({'product': p, 'qty': qty, 'line_total': line_total, 'image_url': image_url})
            total += line_total
        except product.DoesNotExist:
            continue

    customer = None
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer = Customer.objects.filter(id=customer_id).first()

    return render(request, 'shop/cart.html', {'products': products, 'total': total, 'customer': customer})


def order_history(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('shop:login')

    customer = Customer.objects.get(id=customer_id)
    orders = customer.orders.order_by('-created_at')
    return render(request, 'shop/order_history.html', {'orders': orders, 'customer': customer})


def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        name = request.POST.get('name', '')
        if not phone:
            return render(request, 'shop/login.html', {'error': 'Phone is required.'})

        customer, created = Customer.objects.get_or_create(phone=phone, defaults={'name': name})
        if not created and name and not customer.name:
            customer.name = name
            customer.save()

        request.session['customer_id'] = customer.id
        return redirect('shop:index')

    return render(request, 'shop/login.html')


def logout_view(request):
    request.session.pop('customer_id', None)
    return redirect('shop:index')


def about(request):
    return render(request, "shop/about.html")

def home(request):
    return render(request, "shop/home.html")

def productview(request):
    return render(request, "shop/productview.html")

def checkout(request):
    cart = request.session.get('cart', {})
    if not request.session.get('customer_id'):
        return redirect('shop:login')

    if request.method == 'POST':
        customer = Customer.objects.get(id=request.session['customer_id'])
        order = Order(customer=customer)
        order.save()

        total = 0
        for product_id, qty in cart.items():
            try:
                p = product.objects.get(id=product_id)
                line_total = p.price * qty
                OrderItem.objects.create(order=order, product=p, quantity=qty, line_total=line_total)
                total += line_total
            except product.DoesNotExist:
                continue

        order.total_amount = total
        order.status = 'Placed'
        order.save()
        request.session['cart'] = {}
        return redirect('shop:order_history')

    products = []
    total = 0
    for product_id, qty in cart.items():
        try:
            p = product.objects.get(id=product_id)
            line_total = p.price * qty
            image_url = p.image.url if p.image else static('shop/image/django_project.png')
            products.append({'product': p, 'qty': qty, 'line_total': line_total, 'image_url': image_url})
            total += line_total
        except product.DoesNotExist:
            continue

    return render(request, "shop/checkout.html", {'products': products, 'total': total})


def search(request):
    return render(request, "shop/search.html")

def tracker(request):
    return render(request, "shop/tracker.html")


def charts(request):
    # Build demo data from products to show sales trend/stock by category
    from collections import defaultdict
    categories = defaultdict(int)
    for prod in product.objects.all():
        categories[prod.category] += 1

    return render(request, "shop/charts.html", {
        'chart_labels': list(categories.keys()),
        'chart_data': list(categories.values())
    })

