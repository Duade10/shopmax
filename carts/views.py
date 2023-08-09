from django.shortcuts import render
from django.views import View


class CartView(View):
    def get(self, request, *args, **kwargs):
        cart = request.session.session_key
        if not cart:
            cart = request.session.create()
        return render(request, "carts/cart.html")
