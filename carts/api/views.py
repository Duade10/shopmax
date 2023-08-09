from django.contrib.sessions.models import Session
from rest_framework import response, status, views

from carts import models
from products import models as product_models

from . import serializers


def get_cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


class CartView(views.APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            cart_item = models.CartItem.objects.filter(user=user)
        else:
            cart, created = models.Cart.objects.get_or_create(cart_id=get_cart_id(request))
            cart_item, created = models.CartItem.objects.filter(cart=cart)
        serializer = serializers.CartSerializer(cart)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class AddToCartView(views.APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        user = request.user
        data = request.data
        product_slug = data.get("product-slug")
        size = data.get("size")
        product = product_models.Product.objects.get(slug=product_slug)
        if user.is_authenticated:
            variation = product_models.Variation.objects.get(product=product, size__iexact=size)
            cart_item, created = models.CartItem.objects.get_or_create(user=user, product=product)
            cart_item_variations = {item.variation: item for item in cart_item.cart_item_variations.all()}
            if variation in cart_item_variations:
                cart_item = cart_item_variations[variation]
                cart_item.quantity += 1
                cart_item.save()
            else:
                cart_item = models.CartItemVariation.objects.create(cart_item=cart_item, variation=variation)
                cart_item.quantity = 1
                cart_item.save()
            serializer = serializers.CartItemSerializer(cart_item)

        else:
            # try:
            #     cart_id = request.session.session_key
            #     cart = models.Cart.objects.get(cart_id=cart_id)
            # except models.Cart.DoesNotExist:
            #     cart_id = request.session.create()
            #     if cart_id is None:
            #         cart_id = request.session.session_key
            #         if cart_id is None:
            #             cart_id = request.session.create()
            #     cart = models.Cart.objects.create(cart_id=cart_id)
            cart, created = models.Cart.objects.get_or_create(cart_id=get_cart_id(request))
            variation = product_models.Variation.objects.get(product=product, size__iexact=size)
            cart_item, created = models.CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item_variations = {item.variation: item for item in cart_item.cart_item_variations.all()}
            if variation in cart_item_variations:
                cart_item = cart_item_variations[variation]
                cart_item.quantity += 1
                cart_item.save()
            else:
                cart_item = models.CartItemVariation.objects.create(cart_item=cart_item, variation=variation)
                cart_item.quantity = 1
                cart_item.save()
            serializer = serializers.CartItemSerializer(cart_item)
        return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)
