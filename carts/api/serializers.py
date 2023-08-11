from rest_framework import serializers

from carts import models
from products.models import Variation
from products.serializers import ProductSerializer, VariationSerializer


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = "__all__"


class CartItemVariationSerializer(serializers.ModelSerializer):
    variation = VariationSerializer()

    class Meta:
        model = models.CartItemVariation
        exclude = ["created_at", "updated_at"]


class CartItemVariationField(serializers.Field):
    def to_representation(self, obj):
        cart_item_v = models.CartItemVariation.objects.filter(cart_item=obj)
        serializer = CartItemVariationSerializer(cart_item_v, many=True)
        return serializer.data


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    cart_item_variation = serializers.SerializerMethodField()

    class Meta:
        model = models.CartItem
        fields = ["cart", "user", "product", "total_quantity", "cart_item_variation"]

    def get_cart_item_variation(self, obj):
        cart_item_variation_query = obj.cart_item_variations.all()
        # variation_list = []
        # for i in cart_item_variation_query:
        #     print(i.quantity, i.variation, i.variation.size)
        #     variation_list.append(i.variation)
        # serializer = VariationSerializer(variation_list, many=True)
        serializer = CartItemVariationSerializer(cart_item_variation_query, many=True)
        return serializer.data
