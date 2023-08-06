from django.shortcuts import render
from django.views import View


class CartView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "carts/cart.html")
