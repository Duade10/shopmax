from django.shortcuts import render
from products import models as product_models


def index(request):
    products = product_models.Product.objects.all()
    return render(request, "core/index.html", {"products": products})
