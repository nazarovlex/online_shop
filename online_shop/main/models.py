from django.db import models


class Items(models.Model):
    product_name = models.CharField("Product name", max_length=30, null=True)
    shop_name = models.CharField("Shop name", max_length=40, null=True)
    price = models.IntegerField("Item price $", null=True)
    img = models.ImageField("Image of product", upload_to='main/static/main/img', null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return f"/{self.id}"

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"


class Carts(models.Model):
    user_id = models.IntegerField(null=True)
    cart = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


# class ShopItems(models.Model):
#     shop_id = models.IntegerField(null=True)
#     shop_items = models.JSONField(null=True, blank=True)
#
#     class Meta:
#         verbose_name = "ShopItem"
#         verbose_name_plural = "ShopItems"
