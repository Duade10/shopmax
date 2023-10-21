from django.db import models

from core.models import AbstractTimeStampModel


class Wishlist(AbstractTimeStampModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="wishlist")
    products = models.ManyToManyField("products.Product")

    def __str__(self):
        return f"{self.user} wishlist"
