from django.contrib import admin
from .models import Order, OrderItem, Payment, DiscountLife, Coupons, OrderCoupon

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(DiscountLife)
admin.site.register(Coupons)
admin.site.register(OrderCoupon)