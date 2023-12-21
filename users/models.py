from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from django_use_email_as_username.models import BaseUser, BaseUserManager
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext as _


# Create your models here.

class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\(\d{3}\) \d{3}-\d{4}$',
        message="Phone number must be in the format: (999) 999-9999"
    )
    
    first_name = models.CharField(max_length=30, validators=[MinLengthValidator(2, message="Minimum length should be 2")])
    last_name = models.CharField(max_length=30, validators=[MinLengthValidator(2, message="Minimum length should be 2")])
    phone = models.CharField(validators=[phone_regex], max_length=14)
    birth_date = models.DateField()
    email = models.EmailField(max_length=80, validators=[MinLengthValidator(10, message="Minimum length should be 10")], unique=True)
    
    NOT_PUBLISHED = 0
    PUBLISHED = 1

    STATUS_CHOICES = [
        (NOT_PUBLISHED, 'Not published'),
        (PUBLISHED, 'Published (for users)'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=NOT_PUBLISHED)
    password = models.CharField(max_length=30, validators=[MinLengthValidator(6, message="Minimum length should be 6")])
    
    CANNOT_BE_DELETED_OR_UPDATED = 0
    CAN_BE_DELETED_OR_UPDATED = 1

    BUILTIN_CHOICES = [
        (CANNOT_BE_DELETED_OR_UPDATED, 'Cannot be deleted or updated'),
        (CAN_BE_DELETED_OR_UPDATED, 'Can be deleted or updated'),
    ]

    builtIn = models.BooleanField(choices=BUILTIN_CHOICES, default=CANNOT_BE_DELETED_OR_UPDATED)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    objects = BaseUserManager()
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='custom_user_groups',  # related_name eklenmiştir.
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_permissions',  # related_name eklenmiştir.
    )
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    
class Role(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('customer', 'Customer'),
    ]
    
    role_name = models.CharField(choices=ROLE_CHOICES, max_length=10)
    
    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.role_name
    
    
class UserRole(models.Model):    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'User Role'
        verbose_name_plural = 'User Roles'

    def __str__(self):
        return f"{self.user_id} {self.role_id}"
    
    
class UserAddress(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\(\d{3}\) \d{3}-\d{4}$',
        message="Phone number must be in the format: (999) 999-9999"
    )
    
    title = models.CharField(max_length=80)
    first_name = models.CharField(max_length=30, validators=[MinLengthValidator(2, message="Minimum length should be 2")])
    last_name = models.CharField(max_length=30, validators=[MinLengthValidator(2, message="Minimum length should be 2")])
    phone = models.CharField(validators=[phone_regex], max_length=14)
    email = models.EmailField(max_length=80, validators=[MinLengthValidator(10, message="Minimum length should be 10")], unique=True)
    tc = models.CharField(max_length=11)
    address = models.TextField(max_length=250, validators=[MinLengthValidator(10, message="Minimum length should be 10")])
    province = models.CharField(max_length=70, validators=[MinLengthValidator(1, message="Minimum length should be 1")])
    city = models.CharField(max_length=70, validators=[MinLengthValidator(1, message="Minimum length should be 1")])
    country = models.CharField(max_length=70, validators=[MinLengthValidator(1, message="Minimum length should be 1")])
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'User Address'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"