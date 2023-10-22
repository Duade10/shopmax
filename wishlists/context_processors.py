from . import models


def wishlist(request):
    try:
        user = request.user
        wishlist = models.Wishlist.objects.get(user=user)
    except models.Wishlist.DoesNotExist:
        wishlist = []
    return dict(wishlist=wishlist)
