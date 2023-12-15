from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField(upload_to='product_icons', null=True, blank=True)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    author = models.ForeignKey(to='users.User', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Shop(models.Model):
    name = models.CharField(max_length=128)
    adress = models.CharField(max_length=256, null=True, blank=True)
    icon = models.ImageField(upload_to='shop_icons', null=True, blank=True)
    author = models.ForeignKey(to='users.User', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Price(models.Model):
    shop = models.ForeignKey('users.User_Shop', on_delete=models.CASCADE)
    product = models.ForeignKey('users.User_Product', on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    comment = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.shop.user.username + ': ' + self.shop.shop.name + ' ' + self.product.product.name