from django.db import models
from core.models import AbstractTimeStampModel


class Cart(AbstractTimeStampModel):
    cart_id = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.created_at)


class CartItem(AbstractTimeStampModel):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey("users.User", related_name="cart_items", on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(
        "products.Product", related_name="cart_items", on_delete=models.CASCADE, blank=True, null=True
    )
    variations = models.ManyToManyField("products.Variation")
    quantity = models.IntegerField(blank=True, null=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product} | {self.pk}"
