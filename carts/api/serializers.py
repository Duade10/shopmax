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


class CartObjectSerializer(serializers.ModelSerializer):
    sub_total = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()
    cart_item_variations = serializers.SerializerMethodField()

    class Meta:
        model = models.CartItem
        fields = [
            "cart",
            "user",
            "product",
            "total_quantity",
            "sub_total",
            "cart_item_variations",
        ]

    def get_sub_total(self, obj):
        quantity = 0
        cart_item_variations = models.CartItemVariation.objects.filter(cart_item=obj)
        for i in cart_item_variations.all():
            quantity += i.quantity
        sub_total = obj.product.price * quantity
        return sub_total

    def get_total_quantity(self, obj):
        quantity = 0
        cart_item_variations = models.CartItemVariation.objects.filter(cart_item=obj)
        for i in cart_item_variations.all():
            quantity += i.quantity
        return quantity

    def get_cart_item_variations(self, obj):
        cart_item_variations = models.CartItemVariation.objects.filter(cart_item=obj)
        serializer = CartItemVariationSerializer(cart_item_variations, many=True)
        return serializer.data
