from django.contrib import admin
from .models import Customer,CustomerOrder
# Register your models here.
class AdminCustomer(admin.ModelAdmin):
    list_display = ['name','phone','address','Payment','email']

admin.site.register(Customer,AdminCustomer)

class AdminCustomerOrder(admin.ModelAdmin):
    list_display = ['customer','product','quantity','ordered_date','status','price']
    
admin.site.register(CustomerOrder,AdminCustomerOrder)