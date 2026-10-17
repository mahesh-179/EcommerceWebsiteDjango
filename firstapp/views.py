from django.shortcuts import render,redirect
from .forms import CheckOut
from .models import Product
from .models import CustomerOrder,Customer
from django.contrib import messages
from django.db.models import Sum, F
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def CheckOutForm(request):
    customer = Customer.objects.filter(
        user=request.user
    ).first()

    if request.method == "POST":
        form = CheckOut(request.POST, instance=customer)

        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()

            cart = request.session.get("cart", {})

            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)

                CustomerOrder.objects.create(
                    customer=customer,
                    product=product,
                    quantity=quantity,
                    price=product.price,
                )

            request.session.pop("cart", None)

            messages.success(
                request,
                "Order placed successfully!"
            )

            return redirect("index")

    else:
        form = CheckOut(instance=customer)

    return render(
        request,
        "firstapp/checkout.html",
        {"form": form}
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("/")

    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("/")

    return render(request, "register.html", {"form": form})


from .models import CustomerOrder



@login_required
def order_history(request):
    customer = Customer.objects.filter(
        user=request.user
    ).first()

    if customer is None:
        orders = CustomerOrder.objects.none()
    else:
        orders = (
            CustomerOrder.objects
            .filter(customer=customer)
            .select_related("product")
            .order_by("-ordered_date")
        )

    total = orders.aggregate(
        total=Sum(F("price") * F("quantity"))
    )
    total["total"] = total["total"] or 0

    return render(request, "firstapp/orderhistory.html", {
        "orders": orders,
        "total": total,
    })


from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa



from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.db.models import F, ExpressionWrapper, DecimalField
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa

from .models import CustomerOrder


@login_required
def download_all_receipts(request):
    orders = (
        CustomerOrder.objects
        .filter(
            customer__user=request.user,
            status="COMPLETED",
        )
        .select_related("product", "customer", "customer__user")
        .annotate(
            subtotal=ExpressionWrapper(
                F("price") * F("quantity"),
                output_field=DecimalField(
                    max_digits=12,
                    decimal_places=2,
                ),
            )
        )
        .order_by("-ordered_date")
    )

    html = get_template("receipt_pdf.html").render({
        "orders": orders,
    })

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        'attachment; filename="all-order-receipts.pdf"'
    )

    result = pisa.CreatePDF(html, dest=response)

    if result.err:
        return HttpResponse(
            "Could not generate receipts.",
            status=500,
        )

    return response



# @login_required
# def download_receipt(request, pk):
#     order = get_object_or_404(
#         CustomerOrder.objects.select_related(
#             "product", "customer"
#         ),
#         id=pk,
#         customer__user=request.user,
#         status=True,
#     )

#     html = get_template("receipt_pdf.html").render({
#         "order": order,
#         "subtotal": order.price * order.quantity,
#     })

#     response = HttpResponse(content_type="application/pdf")
#     response["Content-Disposition"] = (
#         f'attachment; filename="receipt-{order.id}.pdf"'
#     )

#     result = pisa.CreatePDF(html, dest=response)

#     if result.err:
#         return HttpResponse(
#             "Could not generate receipt.",
#             status=500
#         )

#     return response
