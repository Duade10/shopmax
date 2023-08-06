from django.contrib import admin
from . import models


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


class VariationInline(admin.TabularInline):
    model = models.Variation


class ImageInline(admin.TabularInline):
    model = models.Image


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "discounted_price", "stock", "is_active", "brand")
    list_filter = ["category", "brand", "age_group", "sub_category"]
    search_fields = ["name"]
    list_editable = ["price"]
    inlines = [VariationInline, ImageInline]
    list_per_page = 20
