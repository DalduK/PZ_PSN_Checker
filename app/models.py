from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

PLATFORMS = [('', ''), ('PS3', 'PlayStation 3'), ('PS4', 'PlayStation 4'), ('PSV', 'PlayStation Vita'),
             ('PSP', 'PlayStation Portable'), ('PS2', 'PlayStation 2'), ]


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    price = models.FloatField(default=999999)
    platform = models.CharField(max_length=3, choices=PLATFORMS, default=' ')

    def __str__(self):
        return self.title


class ItemPrice(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    historical_price = models.FloatField(default=999999)
    date_fetched = models.DateTimeField(auto_now_add=True, )


class BasketItem(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.FloatField(default=999999)


class Basket(models.Model):
    basket_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(BasketItem)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.basket_owner.username
