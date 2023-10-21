from rest_framework.serializers import ModelSerializer
from wishlists.models import Wishlist


class WishlistSerializers(ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"
