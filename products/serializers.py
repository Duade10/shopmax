from rest_framework import serializers
from . import models
from wishlists.models import Wishlist


class DiscountPercentageField(serializers.Field):
    def to_representation(self, value):
        price = value.price
        discounted_price = value.discounted_price
        if price and discounted_price:
            discounted_percentage = (price - discounted_price) / 100
            # discounted_percentage = (discounted_price * 100) / price
            return int(discounted_percentage)
        else:
            return None


class HoverImageField(serializers.Field):
    def to_representation(self, value):
        try:
            hover_image = value.images.first()
            hover_image_url = hover_image.image.url
        except AttributeError:
            hover_image_url = None
        return hover_image_url


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)
    sub_category = serializers.StringRelatedField(many=True)
    brand = serializers.StringRelatedField()
    discounted_percentage = DiscountPercentageField(source="*")
    hover_image_url = HoverImageField(source="*")
    is_in_wishlist = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image",
            "price",
            "discounted_price",
            "stock",
            "category",
            "sub_category",
            "brand",
            "is_active",
            "age_group",
            "images",
            "created_at",
            "updated_at",
            "discounted_percentage",
            "hover_image_url",
            "is_in_wishlist",
        ]
        read_only_fields = ["id", "slug", "is_active", "images", "created_at", "updated_at"]

    def get_is_in_wishlist(self, obj):
        request = self.context.get("request")
        try:
            if request.user.is_authenticated:
                try:
                    wishlist = Wishlist.objects.filter(user=request.user, products=obj)
                    if wishlist.exists():
                        return True
                except Wishlist.DoesNotExist:
                    return False
        except AttributeError:
            return False


class VariationSerializer(serializers.ModelSerializer):
    # size = serializers.CharField(required=False)

    class Meta:
        model = models.Variation
        fields = [
            "size",
        ]
