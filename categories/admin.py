from django.contrib import admin
from . import models


class SubCategoryInlineModelAdmin(admin.TabularInline):
    model = models.SubCategory


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    inlines = (SubCategoryInlineModelAdmin,)
