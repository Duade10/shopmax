from django.db.models import Max, Min
from django.shortcuts import render
from django.views import View

from products.models import Brand, Product

# from django.core.paginator import Paginator
# from rest_framework import response, views
# from products.serializers import ProductSerializer


class Shop(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        highest_price = products.aggregate(Max("price"))["price__max"]
        lowest_price = products.aggregate(Min("price"))["price__min"]
        brands = Brand.objects.all()
        context = {"brands": brands, "highest_price": highest_price, "lowest_price": lowest_price}
        return render(request, "shop/shop.html", context)


# class FilterProduct(views.APIView):
#     def get(self, request):
#         if
#         print(request.GET)
#         subcategories = request.GET.get("subcategory", None)
#         brand = request.GET.get("brand", None)
#         filter_args = {}
#         if brand is not None:
#             print(brand)
#             filter_args["brand__slug"] = brand

#         if subcategories is not None:
#             print(subcategories)
#             filter_args["category__subcategory__slug"] = subcategories

#         products = Product.objects.filter(**filter_args)
#         print(products)
#         data = ProductSerializer(data=products, many=True)
#         return response.Response(data.data)
