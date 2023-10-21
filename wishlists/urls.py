from django.urls import path
from . import views

app_name = "wishlists"

urlpatterns = [
    path("", views.WishlistListView.as_view(), name="list"),
]
