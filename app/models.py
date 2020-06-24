<<<<<<< HEAD
from django.conf import settings
from django.db import models
=======
from django.db import models
from django.conf import settings
from django.utils import timezone
>>>>>>> bc-4

# Create your models here.

PLATFORMS = [('', ''), ('PS3', 'PlayStation 3'), ('PS4', 'PlayStation 4'), ('PSV', 'PlayStation Vita'),
             ('PSP', 'PlayStation Portable'), ('PS2', 'PlayStation 2'), ]


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
<<<<<<< HEAD
    price = models.FloatField(null=True)
    platform = models.CharField(max_length=3, choices=PLATFORMS, default=' ')
    ps_id = models.CharField(max_length=50, blank=True)
    image = models.CharField(max_length=250, blank=True)
    age_rating = models.IntegerField(default=99)
=======
    price = models.FloatField(default=999999)
    platform = models.CharField(max_length=3, choices=PLATFORMS, default=' ')
>>>>>>> bc-4

    def __str__(self):
        return self.title


class ItemPrice(models.Model):
<<<<<<< HEAD
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    historical_price = models.FloatField(null=True)
    date_fetched = models.DateTimeField(auto_now_add=True)


class Basket(models.Model):
    basket_title = models.CharField(max_length=100, blank=True, null=True)
    basket_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    total = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
=======
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    historical_price = models.FloatField(default=999999)
    date_fetched = models.DateTimeField(auto_now_add=True, )


class BasketItem(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.FloatField(default=999999)


class Basket(models.Model):
    basket_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(BasketItem)
>>>>>>> bc-4
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.basket_owner.username
<<<<<<< HEAD


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, null=True, blank=True, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
=======
>>>>>>> bc-4
