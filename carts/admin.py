from django.contrib import admin
from . import models


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    pass


class CartItemVariationInline(admin.TabularInline):
    model = models.CartItemVariation


@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    inlines = [
        CartItemVariationInline,
    ]
