from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from .models import Product

PRODUCTS_PER_PAGE = 4
#siganls

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Profile


@login_required
def my_details(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        user = request.user

        # Update user information
        user.first_name = request.POST.get("first_name", "").strip()
        user.last_name = request.POST.get("last_name", "").strip()

        # Keep email editable if desired
        user.email = request.POST.get("email", "").strip()
        user.save()

        # Update profile information
        profile.phone = request.POST.get("phone", "").strip()
        profile.address = request.POST.get("address", "").strip()
        profile.bio = request.POST.get("bio", "").strip()

        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES["profile_picture"]

        profile.save()

        messages.success(request, "Your profile was updated successfully.")
        return redirect("my_details")

    return render(request, "my_details.html", {
        "profile": profile,
    })


def index(request):
    products = Product.objects.select_related("category").order_by("-id")

    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()

    if query:
        products = products.filter(Q(name__icontains=query))
    if category:
        products = products.filter(Q(category__name__iexact=category))

    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))  
    params = request.GET.copy()
    params.pop("page", None)
    querystring = params.urlencode()
    querystring = f"{querystring}&" if querystring else ""

    context = {
        "page_obj": page_obj,
        "query": query,
        "querystring": querystring,
    }
    return render(request, "index.html", context)


def order_view(request, product_id):
    cart = request.session.get("cart", {})
    product_id = str(product_id)

    cart[product_id] = cart.get(product_id, 0) + 1
    request.session["cart"] = cart

    messages.success(request, "Successfully added in your cart")
    return redirect("index")


def cart_view(request):
    cart = request.session.get("cart", {})

    items = []
    total = 0

    products = Product.objects.in_bulk([int(pid) for pid in cart.keys()])

    for product_id, qty in list(cart.items()):
        product = products.get(int(product_id))
        if product is None:
            del cart[product_id]
            continue

        subtotal = product.price * qty
        total += subtotal
        items.append({"product": product, "qty": qty, "subtotal": subtotal})

    request.session["cart"] = cart

    return render(request, "cart.html", {"items": items, "total": total})


def increase(request, product_id):
    cart = request.session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    request.session["cart"] = cart
    return redirect("cart")


def decrease(request, product_id):
    cart = request.session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] -= 1
        if cart[product_id] <= 0:
            del cart[product_id]

    request.session["cart"] = cart
    return redirect("cart")


def remove(request, product_id):
    cart = request.session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]
    request.session["cart"] = cart
    return redirect("cart")