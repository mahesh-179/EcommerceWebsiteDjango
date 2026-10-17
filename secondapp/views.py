from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
# Create your views here.
def index(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    category = request.GET.get('category')
    if query:
        products = products.filter(
            Q(name__icontains=query)
        )
    if category :
        products = products.filter(
            Q(category__name__iexact=category )
        )
    print('Query',query)
    print('Category',category)

    cart = request.session.get('cart',{})
    cart_count = len(cart)
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
    messages.success(request,"Successfully added in your cart")
    
    return redirect ('index')

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
    
def increase(request,product_id):
    cart = request.session.get('cart',{})
    product_id = str(product_id)
    
    if product_id in cart:
        cart[product_id] += 1
    request.session['cart']=cart
    return redirect('cart')

def remove(request,product_id):
    cart = request.session.get('cart',{})
    product_id = str(product_id)
    
    if product_id in cart:
        del cart[product_id] 
        request.session['cart']=cart
    return redirect('cart')

def decrease(request,product_id):
    cart = request.session.get('cart',{})
    product_id = str(product_id)
    
    if product_id in cart:
        cart[product_id] -= 1
    if cart[product_id] <=0:
        del cart[product_id]
        
    request.session['cart']=cart
    return redirect('cart')

