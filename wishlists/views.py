from django.shortcuts import render

from django.views import View
from . import models
from users.mixins import LoggedInOnlyView


class WishlistListView(LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        wishlist = models.Wishlist.objects.get(user=user)
        products = wishlist.products.all()
        context = {"wishlist": wishlist, "products": products}
        return render(request, "wishlist/list.html", context)
