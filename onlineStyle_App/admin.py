from django.contrib import admin
# Register your models here.
from .models import Person
from .models import Product
from .models import Cart
from .models import Sale
from .models import ProductINSale
from .models import Order
from .models import wishList
from .models import Category

admin.site.register(Person)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Sale)
admin.site.register(ProductINSale)
admin.site.register(Order)
admin.site.register(wishList)



