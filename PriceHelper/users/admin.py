from django.contrib import admin

# Register your models here.

from users.models import User, City, User_Product, User_Shop

admin.site.register(User)
admin.site.register(City)
admin.site.register(User_Product)
admin.site.register(User_Shop)