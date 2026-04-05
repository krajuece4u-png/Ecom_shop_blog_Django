from .models import Customer

def cart_count(request):
    cart = request.session.get('cart', {})
    count = sum(cart.values()) if cart else 0
    customer = None
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer = Customer.objects.filter(id=customer_id).first()
    return {'cart_count': count, 'customer': customer}
