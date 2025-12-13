from django.contrib import admin
from products.models import Product, PoductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
