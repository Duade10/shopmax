from django.contrib.sessions.models import Session
from rest_framework import response, status, views
from django.db.models import Sum
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


class ContextData(views.APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            cart_items = models.CartItem.objects.filter(user=user)
            total_quantity = models.CartItemVariation.objects.filter(cart_item__user=user).aggregate(
                total_quantity=Sum("quantity")
            )["total_quantity"]
        else:
            cart, created = models.Cart.objects.get_or_create(cart_id=get_cart_id(request))
            cart_items = models.CartItem.objects.filter(cart=cart)
            total_quantity = models.CartItemVariation.objects.filter(cart_item__cart=cart).aggregate(
                total_quantity=Sum("quantity")
            )["total_quantity"]
        all_product_price = cart_items.aggregate(total_price=Sum("product__price"))["total_price"]
        sub_total = all_product_price * total_quantity
        tax = round((2 * sub_total) / 100, 2)
        grand_total = sub_total + tax
        serializer = serializers.CartObjectSerializer(cart_items, many=True)
        context_data = dict(
            total_quantity=total_quantity,
            tax=tax,
            sub_total=round(sub_total, 2),
            grand_total=round(grand_total, 2),
        )
        cart_response = dict(context_data=context_data, cart_items=serializer.data)
        return response.Response(cart_response, status=status.HTTP_200_OK)


class CartItemsListView(views.APIView):
    def get(self, request, *arg, **kwargs):
        user = request.user
        if user.is_authenticated:
            cart_items = models.CartItem.objects.filter(user=user)
            serializer = serializers.CartObjectSerializer(cart_items, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        else:
            cart_id = get_cart_id(request)
            cart, created = models.Cart.objects.filter(cart=cart_id)
            cart_items = models.CartItem.objects.filter(cart=cart)
            serializer = serializer.CartObjectSerializer(cart_items, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)


class DecreaseCartView(views.APIView):
    def get(self, request, variation_id, *args, **kwargs):
        user = request.user
        variation = models.CartItemVariation.objects.get(id=variation_id)
        variation.quantity -= 1
        if variation.quantity <= 0:
            variation.delete()
        else:
            variation.save()
        cart_item = models.CartItem.objects.get(id=variation.cart_item.id)
        total_quantity = cart_item.get_total_quantity()
        if total_quantity <= 0:
            cart_item.delete()
        if user.is_authenticated:
            cart_items = models.CartItem.objects.filter(user=user)
            serializer = serializers.CartObjectSerializer(cart_items, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        else:
            cart_id = get_cart_id(request)
            cart, created = models.Cart.objects.filter(cart=cart_id)
            cart_items = models.CartItem.objects.filter(cart=cart)
            serializer = serializer.CartObjectSerializer(cart_items, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({"message": "variation decreased"}, status=status.HTTP_200_OK)


class AddToCartView(views.APIView):
    def post(self, request, *args, **kwargs):
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


class CartVariationData(views.APIView):
    def get(self, request, *args, **kwargs):
        # user = request.user
        # cart_item_variations_list = []
        # if user.is_authenticated():
        #     cart_items = models.CartItem.objects.filter(user=user)
        #     for cart_item in cart_items:
        #         for item in cart_item.cart_item_variations.all():
        #             cart_item_variations_list.append(item)
        #     print(cart_item_variations_list)
        return response.Response({"done": "Done"})
