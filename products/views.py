from django.shortcuts import render
from django.views import View
from . import models
from django.http import HttpRequest, HttpResponse


class ProductDetail(View):
    def get(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:
        product = models.Product.objects.get(slug=slug)
        return render(request, "products/product_detail.html", context={"product": product})
