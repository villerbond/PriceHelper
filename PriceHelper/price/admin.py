from django.contrib import admin

# Register your models here.

from price.models import Category, Product, Shop, Price, Basket

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Shop)
admin.site.register(Price)
admin.site.register(Basket)