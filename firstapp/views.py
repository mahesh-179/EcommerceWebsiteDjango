from django.shortcuts import render,redirect
from .forms import CheckOut
from .models import Product
from .models import CustomerOrder
from django.contrib import messages
from django.db.models import Sum, F
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.
def CheckOutForm(request):
    if request.method == 'POST':
        form = CheckOut(request.POST)

        if form.is_valid():
            customer = form.save()

            cart = request.session.get('cart', {})

            for product_id, quantity,in cart.items():
                product = Product.objects.get(id=product_id)

                CustomerOrder.objects.create(
                    customer=customer,
                    product=product,
                    quantity=quantity,
                    price = product.price
                )

            # CLEAR CART AFTER ORDER
            request.session.pop('cart', None)

            messages.success(request, "Order placed successfully!")

            return redirect('index')

    else:
        form = CheckOut()

    return render(request, "firstapp/checkout.html", {"form": form})
        
def view_order(request):
    total = CustomerOrder.objects.aggregate(
    total=Sum(F('price') * F('quantity'))
    )

    orders = CustomerOrder.objects.all().order_by('id')
    context = {
        "orders":orders,
        "total":total,
    }
    return render(request,"firstapp/orderhistory.html",context = context )



def register(request):
    if request.user.is_authenticated:
        return redirect("/")

    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("/")

    return render(request, "register.html", {"form": form})