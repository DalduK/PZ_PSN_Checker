from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Item)
admin.site.register(ItemPrice)
# admin.site.register(Basket)
admin.site.register(BasketItem)
