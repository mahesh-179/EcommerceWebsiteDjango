from django.shortcuts import render,redirect
from .models import *
# Create your views here.
def index(request):
    products = Product.objects.all()
    cart = request.session.get('cart',{})
    cart_count = sum(cart.values())

    context = {
        "products":products,
        "cart_count":cart_count,
    }
    return render(request,"index.html",context=context)

def order_view(request,product_id):
    cart = request.session.get('cart',{})

    product_id = str(product_id)
    if product_id in cart:
        cart[product_id]+=1
    else:
        cart[product_id]=1
    request.session['cart'] = cart
    
    return redirect ('cart')

from .models import Product

def cart_view(request):
    cart = request.session.get('cart', {})

    items = []
    total = 0

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)

        subtotal = product.price * qty
        total += subtotal

        items.append({
            "product": product,
            "qty": qty,
            "subtotal": subtotal
        })

    return render(request, 'cart.html', {
        "items": items,
        "total": total
    })