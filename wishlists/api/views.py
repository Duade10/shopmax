from rest_framework.views import APIView
from wishlists import models
from products.models import Product
from rest_framework.response import Response
from rest_framework import status


class ToggleWishlistView(APIView):
    def get(self, request, product_id, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            try:
                wishlist = models.Wishlist.objects.get(user=user)
            except models.Wishlist.DoesNotExist:
                wishlist = models.Wishlist.objects.create(user=user)

            product = Product.objects.get(id=product_id)

            if product in wishlist.products.all():
                wishlist.products.remove(product)
                data = {"message": "product removed from wishlist"}
                request_status = status.HTTP_200_OK

            else:
                wishlist.products.add(product)
                data = {"message": "product added to wishlist"}
                request_status = status.HTTP_201_CREATED

            return Response(data, status=request_status)

        return Response({"message": "login required"}, status=status.HTTP_403_FORBIDDEN)
