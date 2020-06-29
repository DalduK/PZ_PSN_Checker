from django.conf import settings
from django.db import models

# Create your models here.

PLATFORMS = [('', ''), ('PS3', 'PlayStation 3'), ('PS4', 'PlayStation 4'), ('PSV', 'PlayStation Vita'),
             ('PSP', 'PlayStation Portable'), ('PS2', 'PlayStation 2'), ]


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    title = models.SlugField(blank=False)
    price = models.FloatField(null=True)
    platform = models.CharField(max_length=3, choices=PLATFORMS, default=' ')
    ps_id = models.CharField(max_length=50, blank=True)
    image = models.SlugField(blank=True)
    age_rating = models.IntegerField(default=99)
    trailer_url = models.SlugField(blank=True)
    onsale = models.BooleanField(default=False)
    tag = models.SlugField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class ItemPrice(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    historical_price = models.FloatField(null=True)
    date_fetched = models.DateTimeField(auto_now_add=True)


class Basket(models.Model):
    basket_title = models.CharField(max_length=100, blank=True, null=True)
    basket_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    total = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, null=True, blank=True, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)


class Carousel(models.Model):
    image_url = models.SlugField()
