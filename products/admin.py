from django.contrib import admin
from .models import Category, Brand, Product, Review, ShoppingCartItem, Image, Transaction

# Register your models here.

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(ShoppingCartItem)
admin.site.register(Image)
admin.site.register(Transaction)