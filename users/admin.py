from django.contrib import admin
from .models import User, Role, UserRole, UserAddress

# Register your models here.

admin.site.register(User)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(UserAddress)