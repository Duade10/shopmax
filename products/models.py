import datetime
from datetime import timedelta
from django.db import models
from core.models import AbstractTimeStampModel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

# from shortuuidfield import ShortUUIDField
from django.urls import reverse
from django.utils import timezone


class Brand(AbstractTimeStampModel):
    name = models.CharField(_("Brand Name"), max_length=255)
    slug = models.SlugField(_("Slug"), null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class ProductManager(models.Manager):
    def active(self):
        return super().filter(is_active=True)


class Product(AbstractTimeStampModel):
    KIDS = "kids"
    ADULTS = "adults"

    AGE_GROUP_CHOICES = ((KIDS, "Kids"), (ADULTS, "Adults"))

    name = models.CharField(_("Product Name"), max_length=255)
    slug = models.SlugField(_("Slug"), null=True, blank=True)
    # uuid = ShortUUIDField()
    description = models.TextField()
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    price = models.DecimalField(_("Product Price"), max_digits=10, decimal_places=2)
    discounted_price = models.IntegerField(blank=True, null=True)
    stock = models.PositiveIntegerField()
    category = models.ManyToManyField("categories.Category", related_name="product")
    sub_category = models.ManyToManyField("categories.SubCategory", related_name="product")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    age_group = models.CharField(choices=AGE_GROUP_CHOICES, max_length=10, blank=True, null=True)
    objects = ProductManager()

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})

    def in_stock(self):
        if self.stock > 0:
            return True
        else:
            return False

    def is_new(self):
        now = timezone.now()
        product_age = now - self.created_at
        if product_age > timedelta(days=3):
            return False
        else:
            return True

    def discount_percentage(self):
        # discount_percent = (int(self.discounted_price) * 100) / int(self.price)
        discounted_percent = int((int(self.price) - self.discounted_price) / 100)
        return discounted_percent

    def save(self, *args, **kwargs):
        self.name = str(self.name).upper()
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Image(AbstractTimeStampModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField()
    # uuid = ShortUUIDField()

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return self.product.name


class VariationManager(models.Manager):
    def colour(self):
        return super().filter(variation_category="colour")

    def size(self):
        return super().filter(variation_category="size")


class Variation(AbstractTimeStampModel):
    VARIATION_SIZE = "size"
    VARIATION_COLOUR = "colour"

    VARIATION_CHOICES = ((VARIATION_SIZE, "Size"), (VARIATION_COLOUR, "Colour"))

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variation")
    variation_category = models.CharField(choices=VARIATION_CHOICES, max_length=7)
    variation_value = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    objects = VariationManager()

    class Meta:
        verbose_name = "Variation"
        verbose_name_plural = "Variations"

    def __str__(self):
        return f"{self.product.name} | {self.variation_category} => {self.variation_value}"
