from django.core.paginator import Paginator
from rest_framework import response, views

from products.models import Product
from products.serializers import ProductSerializer


class GetProduct(views.APIView):
    def get(self, request):
        filter_args = {}
        page = request.GET.get("page")
        subcategories = request.GET.getlist("subcategory", "")
        brand = request.GET.getlist("brand", "")
        if brand:
            filter_args["brand__slug__in"] = brand

        if subcategories:
            filter_args["sub_category__slug__in"] = subcategories

        if filter_args:
            path_info = request.META.get("PATH_INFO")
            query_string = request.META.get("QUERY_STRING")
            pagination_url = f"{path_info}?{query_string}"
            products = Product.objects.filter(**filter_args).order_by("-created_at")
        else:
            pagination_url = None
            products = Product.objects.all().order_by("-created_at")

        paginator = Paginator(products, 9, orphans=2)

        page = request.GET.get("page", 1)
        products = paginator.get_page(page)
        serializer = ProductSerializer(products.object_list, many=True)
        pagination = {
            "pagination_url": pagination_url,
            "number_of_pages": paginator.num_pages,
            "has_next": products.has_next(),
            "has_previous": products.has_previous(),
            "current_page_number": products.number,
        }
        responses = dict(products=serializer.data, pagination=pagination)
        return response.Response(responses)
