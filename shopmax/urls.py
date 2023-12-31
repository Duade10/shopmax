"""shopmax URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("users/", include("users.urls", namespace="users")),
    path("shop/", include("shop.urls", namespace="shop")),
    path("carts/", include("carts.urls", namespace="carts")),
    path("product/", include("products.urls", namespace="products")),
    path("wishlist/", include("wishlists.urls", namespace="wishlists")),
]

urlpatterns += [
    path("api/shop/", include("shop.api.urls", namespace="shop_api")),
    path("api/carts/", include("carts.api.urls", namespace="carts_api")),
    path("api/wishlist/", include("wishlists.api.urls", namespace="wishlist_api")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
