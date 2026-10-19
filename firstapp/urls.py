
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from secondapp.views import my_details
from .views import CheckOutForm, order_history

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    path("register/", views.register, name="register"),

    path("checkout/", CheckOutForm, name="checkout"),

    path("order-history/", order_history, name="order-history"),

    path(
        "orders/all-receipts/",
        views.download_all_receipts,
        name="download-all-receipts",
    ),
    path("my-details/", my_details, name="my_details"),
]
