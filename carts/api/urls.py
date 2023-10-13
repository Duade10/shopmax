from django.urls import path
from . import views

app_name = "carts_api"

urlpatterns = [
    path("context-data/", views.ContextData.as_view(), name="data"),
    path("get-cart-item-list/", views.CartItemsListView.as_view(), name="cart_item_list"),
    path("decrease-quantity/<int:variation_id>/", views.DecreaseCartView.as_view()),
    path("add-to-cart/", views.AddToCartView.as_view(), name="add"),
    path("get-variation-data/", views.CartVariationData.as_view(), name="variation_data"),
    path("test/", views.CartItemsListView.as_view(), name="test"),
]
