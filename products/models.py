from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from users.models import User
from orders.models import Order

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=80, validators=[MinLengthValidator(2, message="Minimum length should be 2")])
    
    NOT_PUBLISHED = 0
    PUBLISHED = 1

    STATUS_CHOICES = [
        (NOT_PUBLISHED, 'Not published'),
        (PUBLISHED, 'Published (for users)'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=NOT_PUBLISHED)
    
    CANNOT_BE_DELETED_OR_UPDATED = 0    
    CAN_BE_DELETED_OR_UPDATED = 1

    BUILTIN_CHOICES = [
        (CANNOT_BE_DELETED_OR_UPDATED, 'Cannot be deleted or updated'),
        (CAN_BE_DELETED_OR_UPDATED, 'Can be deleted or updated'),
    ]

    builtIn = models.BooleanField(choices=BUILTIN_CHOICES, default=CANNOT_BE_DELETED_OR_UPDATED)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.title
    
    
class Brand(models.Model):
    name = models.CharField(max_length=70, validators=[MinLengthValidator(4, message="Minimum length should be 4")])
    
    NOT_PUBLISHED = 0
    PUBLISHED = 1

    STATUS_CHOICES = [
        (NOT_PUBLISHED, 'Not published'),
        (PUBLISHED, 'Published (for users)'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=NOT_PUBLISHED)
    image = models.ImageField()
    
    CANNOT_BE_DELETED_OR_UPDATED = 0
    CAN_BE_DELETED_OR_UPDATED = 1

    BUILTIN_CHOICES = [
        (CANNOT_BE_DELETED_OR_UPDATED, 'Cannot be deleted or updated'),
        (CAN_BE_DELETED_OR_UPDATED, 'Can be deleted or updated'),
    ]

    builtIn = models.BooleanField(choices=BUILTIN_CHOICES, default=CANNOT_BE_DELETED_OR_UPDATED)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        
    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=100, validators=[MinLengthValidator(10, message="Minimum length should be 10")])
    title = models.CharField(max_length=150, validators=[MinLengthValidator(5, message="Minimum length should be 5")])
    short_desc = models.CharField(max_length=300, blank=True, null=True)
    long_desc = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(validators=[MinLengthValidator(0, message="Minimum length should be 0")])
    stock_amount = models.IntegerField()
    stock_alarm_limit = models.IntegerField()
    slug = models.SlugField(max_length=200, validators=[MinLengthValidator(5, message="Minimum length should be 5")])
    featured = models.BooleanField(default=False)
    image = models.ImageField()
    new_product = models.BooleanField()
    like = models.IntegerField(default=0)
    
    NOT_PUBLISHED = 0
    PUBLISHED = 1

    STATUS_CHOICES = [
        (NOT_PUBLISHED, 'Not published'),
        (PUBLISHED, 'Published (for users)'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=NOT_PUBLISHED)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    
    CANNOT_BE_DELETED_OR_UPDATED = 0
    CAN_BE_DELETED_OR_UPDATED = 1

    BUILTIN_CHOICES = [
        (CANNOT_BE_DELETED_OR_UPDATED, 'Cannot be deleted or updated'),
        (CAN_BE_DELETED_OR_UPDATED, 'Can be deleted or updated'),
    ]

    builtIn = models.BooleanField(choices=BUILTIN_CHOICES, default=CANNOT_BE_DELETED_OR_UPDATED)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title
    
class Review(models.Model):
    content = models.CharField(max_length=200)
    rating = models.IntegerField(validators=[
        MinValueValidator(1, message="Minimum value should be 1"),
        MaxValueValidator(5, message="Maximum value should be 5")
    ])
    
    NOT_PUBLISHED = 0
    PUBLISHED = 1

    STATUS_CHOICES = [
        (NOT_PUBLISHED, 'Not published'),
        (PUBLISHED, 'Published (for users)'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=NOT_PUBLISHED)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        
    def __str__(self):
        return self.content
    
    
class ShoppingCartItem(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Shopping Cart Item'
        verbose_name_plural = 'Shopping Cart Items'
        
    def __str__(self):
        return self.amount
    
    
class Image(models.Model):
    data = models.BinaryField()
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, blank=True, null=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        db_table = 'your_table_name' 
        
    def __str__(self):
        return self.name
        
        
class Transaction(models.Model):
    CREATED = 'CREATED'
    UPDATED = 'UPDATED'
    CANCELED = 'CANCELED'
    COMPLETED = 'COMPLETED'

    TRANSACTION_CHOICES = [
        (CREATED, 'Created'),
        (UPDATED, 'Updated'),
        (CANCELED, 'Canceled'),
        (COMPLETED, 'Completed'),
    ]
    
    transaction = models.CharField(max_length=100, choices=TRANSACTION_CHOICES)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        
    def __str__(self):
        return self.transaction