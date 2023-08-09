from django.shortcuts import render
from django.views import View
from . import models
from django.http import HttpRequest, HttpResponse


class ProductDetail(View):
    def get(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:
        cart = request.session.session_key
        if not cart:
            cart = request.session.create()
        product = models.Product.objects.get(slug=slug)
        print(product.variation.count())
        # add_to_cart_button_func = lambda x: False if x.variation.count() < 1 else x is True
        if product.variation.count() < 1:
            add_to_cart_button = False
        elif product.variation.count() > 1:
            add_to_cart_button = True
        print(add_to_cart_button)
        return render(
            request,
            "products/product_detail.html",
            context={"product": product, "add_to_cart_button": add_to_cart_button},
        )
