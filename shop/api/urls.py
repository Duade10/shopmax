from django.urls import path
from . import views

app_name = "shop_api"

urlpatterns = [
    path("get-products/", views.GetProduct.as_view(), name="get_products"),
]
