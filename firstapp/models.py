from django.db import models
from django.db import models
from secondapp.models import Product 

class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.IntegerField()
    address = models.CharField(max_length=255)
    email = models.EmailField()
    payment_method = [
        ('COD','CASH ON DELIVERY'),
        ('ESEWA','ESEWA'),
        ('KHALTI','KHALTI')
    ]
    Payment = models.CharField(max_length=10,choices=payment_method)
    def __str__(self):
        return self.name
    
class CustomerOrder(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='orders',default=True,blank=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='total_orders')
    quantity = models.IntegerField()
    ordered_date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    status = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-ordered_date',)
    
