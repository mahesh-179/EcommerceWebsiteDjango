from django.contrib import admin
from .models import Product, Category
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','available','created','category']
    prepopulated_fields = {
        "slug": ("name",)
    }

    
admin.site.register(Product,ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug',]
    prepopulated_fields = {
        "slug": ("name",)
    }

    
admin.site.register(Category,CategoryAdmin)

