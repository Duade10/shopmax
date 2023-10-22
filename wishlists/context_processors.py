from . import models


def wishlist_context_processor(request):
    wishlist = []

    if request.user.is_authenticated:
        try:
            wishlist = models.Wishlist.objects.get(user=request.user)
        except models.Wishlist.DoesNotExist:
            pass

    return {"wishlist": wishlist}
