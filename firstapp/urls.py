from django.urls import path
from .views import CheckOutForm,view_order
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path('checkout/',CheckOutForm,name="checkout"),
    path('order-history/',view_order,name="order-history"),
]
