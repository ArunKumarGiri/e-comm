from django.contrib import admin
from .models import Customer,Product,OrderPlaced,Cart
# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(OrderPlaced)
admin.site.register(Cart)