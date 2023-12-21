from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinLengthValidator
from users.models import User, UserAddress
# from products.models import Product

# Create your models here.

class Order(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\(\d{3}\) \d{3}-\d{4}$',
        message="Phone number must be in the format: (999) 999-9999"
    )
    
    code = models.CharField(max_length=8, validators=[MinLengthValidator(8, message="Minimum length should be 8")])
    
    PENDING = 0
    BEING_SUPPLIED = 1
    READY_TO_SHIP = 2
    DELIVERY_DONE = 3
    RETURNED = 4
    CANCELED = 5
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (BEING_SUPPLIED, 'Being supplied'),
        (READY_TO_SHIP, 'Ready to ship'),
        (DELIVERY_DONE, 'Delivery done'),
        (RETURNED, 'Returned'),
        (CANCELED, 'Canceled'),
    ]
    
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    contact_name = models.CharField(max_length=80)
    contact_phone = models.CharField(validators=[phone_regex], max_length=14)
    shopping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    shopping_details = models.CharField(max_length=150)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_address_id = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='invoice_orders')
    shipping_address_id = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='shipping_orders')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        
    def __str__(self):
        return self.contact_name

    
class OrderItem(models.Model):
    sku = models.CharField(max_length=100, validators=[MinLengthValidator(10, message="Minimum length should be 10")])
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    product_id = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        
    def __str__(self):
        return str(self.quantity)
    

class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.CharField(max_length=100)
    
    CREATED = 0
    PENDING = 1
    BEING_SUPPLIED = 2
    READY_TO_SHIP = 3
    DELIVERY_DONE = 4
    RETURNED = 5
    CANCELED = 6
    
    STATUS_CHOICES = [
        (CREATED, 'Created'),
        (PENDING, 'Pending'),
        (BEING_SUPPLIED, 'Being supplied'),
        (READY_TO_SHIP, 'Ready to ship'),
        (DELIVERY_DONE, 'Delivery done'),
        (RETURNED, 'Returned'),
        (CANCELED, 'Canceled'),
    ]
    
    status = models.IntegerField(choices=STATUS_CHOICES, default=CREATED)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        
    def __str__(self):
        return self.provider
    

class DiscountLife(models.Model):
    value = models.IntegerField()

    def is_infinite(self):
        return self.value == -1
    
    
class Coupons(models.Model):
    code = models.CharField(max_length=14, validators=[RegexValidator(
            regex=r'^[0-9]{4}-[0-9]{4}-[0-9]{4}$',
            message="Format should be XXXX-XXXX-XXXX (where X is a digit)",
        )])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    EXACT_AMOUNT = 0
    PERCENTAGE_AMOUNT = 1
    
    TYPE_CHOICES = [
        (EXACT_AMOUNT, 'Exact amount'),
        (PERCENTAGE_AMOUNT, 'Percentage amount'),
    ]
    
    life = models.ForeignKey(DiscountLife, on_delete=models.CASCADE)
    
    PASSIVE = 0
    ACTIVE = 1
    
    STATUS_CHOCIES = [
        (PASSIVE, 'Passive'),
        (ACTIVE, 'Active'),
    ]
    
    status = models.IntegerField(choices=STATUS_CHOCIES, default=PASSIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
        
    def __str__(self):
        return self.code


class OrderCoupon(models.Model):
    coupon_id = models.ForeignKey(Coupons, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Order Coupon'
        verbose_name_plural = 'Order Coupons'
        
    def __str__(self):
        return str(self.coupon_id)