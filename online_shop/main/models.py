from django.conf import settings
from django.db import models


class Items(models.Model):
    product_id = models.CharField("Product id", max_length=15, null=True)
    product_name = models.CharField("Product name", max_length=30, null=True)
    shop_name = models.CharField("Shop name", max_length=40, null=True)
    price = models.IntegerField("Item price $", null=True)
    img = models.ImageField("Image of product", upload_to='main/static/main/img', null=True, blank=True)

    def __str__(self):
        return self.product_id

    def get_absolute_url(self):
        return f"/{self.id}"

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"


class Carts(models.Model):
    # user_id = models.IntegerField(default='', null=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, default=0, null=True, on_delete=models.CASCADE)
    cart = models.JSONField(null=True,blank=True)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


