from carts import models
from rest_framework import serializers


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = "__all__"
