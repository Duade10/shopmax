from django.db import models
from core.models import AbstractTimeStampModel
from django.utils.text import slugify


class CategoryManager(models.Manager):
    def get_active(self):
        return self.filter(is_active=True)


class CategoryAbstractModel(AbstractTimeStampModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    is_active = models.BooleanField(default=True)
    objects = CategoryManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(CategoryAbstractModel):
    description = models.TextField(null=True, blank=True)
    # image = models.ImageField(upload_to="categories/", null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    # def product_count(self):
    #     return self.product.count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class SubCategory(CategoryAbstractModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategory")

    class Meta:
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return f"{self.name} | {self.category.name}"

    def save(self, *args, **kwargs):
        slug = f"{self.name} {self.category.name}"
        self.slug = slugify(slug)
        return super().save(*args, **kwargs)
