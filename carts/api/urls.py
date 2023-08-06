from django.urls import path
from . import views

app_name = "carts_api"

urlpatterns = [path("add-to-cart/", views.AddToCartView.as_view(), name="add")]
