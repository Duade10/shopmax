from django.urls import path
from . import views

app_name = "wishlist_api"

urlpatterns = [
    path("toggle/<int:product_id>/", views.ToggleWishlistView.as_view()),
]
