from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator

# Account Verification Imports
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

# # GET CART USER IMPORTS
# from carts.models import Cart, CartItem
# from carts.views import _cart_id


class User(AbstractUser):
    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_FACEBOOK = "facebook"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_FACEBOOK, "Facebook"),
        (LOGIN_GITHUB, "Github"),
    )

    phone_number = models.CharField(max_length=20, null=True)
    login_method = models.CharField(max_length=20, choices=LOGIN_CHOICES, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.first_name = str.capitalize(self.first_name)
        self.last_name = str.capitalize(self.last_name)
        super().save(*args, **kwargs)

    def get_full_name(self) -> str:
        return super().get_full_name()

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    def verify_email(self, request):
        current_site = get_current_site(request)
        domain = current_site
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        token = default_token_generator.make_token(self)

        html_message = render_to_string(
            "users/mail/user_verification_email.html",
            {"domain": domain, "uidb64": uid, "token": token, "first_name": self.first_name},
        )
        send_mail(
            "Activate your Account",
            strip_tags(html_message),
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
            html_message=html_message,
        )
        self.save()

    def send_reset_email(self, request):
        current_site = get_current_site(request)
        domain = current_site
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        token = default_token_generator.make_token(self)

        html_message = render_to_string(
            "users/mail/reset_password_email.html",
            {"domain": domain, "uid": uid, "token": token, "first_name": self.first_name},
        )
        send_mail(
            "Reset Your Password",
            strip_tags(html_message),
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
            html_message=html_message,
        )

    # def get_cart(self, request):
    #     try:
    #         cart_id = _cart_id(request)
    #         cart = Cart.objects.get(cart_id=cart_id)
    #         cart_cart_item = CartItem.objects.filter(cart=cart)

    #         if CartItem.objects.filter(user=self).exists():
    #             user_cart_item = CartItem.objects.filter(user=self)
    #             for user_item in user_cart_item:
    #                 for cart_item in cart_cart_item:
    #                     if user_item.product.pk is cart_item.product.pk:
    #                         print(user_item.product.pk, user_item.product.pk)
    #                         cart_item.quantity += user_item.quantity
    #                         cart_item.user = user_item.user
    #                         cart_item.save()
    #                         user_item.delete()
    #                     else:
    #                         cart_item.user = self
    #                         cart_item.save()
    #         else:
    #             CartItem.objects.filter(cart=cart).update(user=self)
    #     except Cart.DoesNotExist:
    #         pass
