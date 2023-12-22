from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from price.models import Product, Shop

class City(models.Model):
    name = models.CharField(max_length=64, unique=True)
    custom = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class User(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', null=True, blank=True)
    city = models.ForeignKey(to=City, on_delete=models.SET_NULL, null=True, blank=True)
    private = models.BooleanField(default=False)
    products = models.ManyToManyField(Product, through="User_Product")
    shops = models.ManyToManyField(Shop, through="User_Shop")

    def __str__(self):
        return self.username

class User_Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' - ' + self.product.name

class User_Shop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    adress = models.CharField(max_length=256, null=True, blank=True)
    difficulty = models.SmallIntegerField()

    def __str__(self):
        if self.adress:
            return self.user.username + ' - ' + self.shop.name + ' (' + self.adress + ') '
        else:
            return self.user.username + ' - ' + self.shop.name

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(difficulty__gte=1) & models.Q(difficulty__lt=6),
                name="A value of difficulty is valid between 1 and 5",
            )
        ]
        unique_together = ('user', 'shop', 'adress')
