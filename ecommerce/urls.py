from secondapp.views import index,order_view,cart_view
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="index"),
    path('add/<int:product_id>/',order_view,name='add'),
    path('cart/',cart_view, name='cart'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)