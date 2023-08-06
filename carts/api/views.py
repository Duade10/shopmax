from rest_framework import views, response, status
from . import serializers
from carts import models


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
        user = request.user
        if user.is_authenticated:
            cart_item = models.CartItem.objects.filter(user=user)
        else:
            cart, created = models.Cart.objects.get_or_create(cart_id=get_cart_id(request))
            cart_item = models.CartItem.objects.filter(cart=cart)
        print(request.data)
        return response.Response({"data": "Done"}, status=status.HTTP_200_OK)
