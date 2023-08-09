from django.urls import path
from . import views

app_name = "carts_api"

urlpatterns = [
    path("get-data/<str:extra_data>/", views.CartData.as_view(), name="data"),
    path("add-to-cart/", views.AddToCartView.as_view(), name="add"),
]
