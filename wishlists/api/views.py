from rest_framework.views import APIView
from wishlists import models
from products.models import Product
from rest_framework.response import Response
from rest_framework import status


class ToggleWishlistView(APIView):
    def get(self, request, product_id, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                wishlist = models.Wishlist.objects.get(user=user)
            except models.Wishlist.DoesNotExist:
                wishlist = models.Wishlist.objects.create(user=user)

            product = Product.objects.get(id=product_id)

            if product in wishlist.products.all():
                wishlist.products.remove(product)
                data = {"message": "product removed from wishlist"}
            else:
                wishlist.products.add(product)
                data = {"message": "product added from wishlist"}

            return Response(data, status=status.HTTP_200_OK)

        return Response({"message": "login required"}, status=status.HTTP_403_FORBIDDEN)
