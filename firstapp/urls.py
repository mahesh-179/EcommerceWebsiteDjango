from django.urls import path
from .views import CheckOutForm,view_order
urlpatterns = [
   
    path('checkout/',CheckOutForm,name="checkout"),
    path('order-history/',view_order,name="order-history"),
]