from secondapp.views import index,order_view,cart_view,remove,decrease,increase
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="index"),
    path('add/<int:product_id>/',order_view,name='add'),
    path('cart/',cart_view, name='cart'),
    path('remove/<int:product_id>/',remove,name='remove'),
    path('increase/<int:product_id>/',increase,name="increase"),
    path('decrease/<int:product_id>/',decrease,name="decrease"),
    path('checkout/',include('firstapp.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)