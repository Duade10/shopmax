from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("<slug>/", views.ProductDetail.as_view(), name="detail"),
]
