from django.contrib import admin
from .models import Items, Carts, ShopItems

admin.site.register(Items)
admin.site.register(Carts)
admin.site.register(ShopItems)
