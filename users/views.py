import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.http import HttpRequest, HttpResponse
from django.views.generic import FormView
from django.conf import settings
from django.views import View

# from orders.models import Order

from . import forms, mixins, models


class LoginView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        username = email.split("@")[0]
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            if user.login_method != models.User.LOGIN_EMAIL and user.login_method != None:
                messages.error(self.request, f"Invalid Login Method. Login with {user.login_method} instead.")
                return redirect("users:login")
            user.get_cart(self.request)
            user.login_method = models.User.LOGIN_EMAIL
            user.save()
            login(self.request, user)
        else:
            return redirect(reverse("users:login"))
        url = self.request.GET.get("next")
        return redirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, f"Welcome {self.request.user.first_name}")
        return self.request.GET.get("next", "/")


def log_out(request):
    logout(request)
    messages.success(request, "See you later")
    return redirect(reverse("users:login"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        username = email.split("@")[0]
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            user.login_method = models.User.LOGIN_EMAIL
            user.save()
            user.is_active = False
            user.verify_email(self.request)
        return redirect("/accounts/login/?command=verification&email=" + email)


class UserUpdateView(mixins.LoggedInOnlyView, View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user = self.request.user
        form = forms.UpdateForm(instance=user)
        context = {"user": user, "form": form}
        return redirect(request, "users/edit_user.html", context)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = forms.UpdateForm(request.POST)
        if form.is_valid():
            data = form.save()
            return redirect("users:user_profile", data.pk)


def activate(request: HttpRequest, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = models.User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, models.User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # todo: Add Messages
        # messages.success(request, "Email Verification Activation Successfull")
    return redirect("core:home")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        if models.User.objects.filter(email=email).exists():
            user = models.User.objects.get(email__exact=email)
            if user.login_method == models.User.LOGIN_GITHUB:
                messages.error(
                    request, f"Invalid Login Method. Login through {models.User.LOGIN_GITHUB.capitalize()} instead"
                )
                return redirect("users:login")
            user.send_reset_email(request)
            messages.success(request, "Password reset email has been sent to your email address.")
            return redirect("users:login")

        else:
            messages.error(request, "Account does not exist")
            return redirect("users:forgot_password")

    return render(request, "users/forgot_password.html")


def validate_reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = models.User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, models.User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please reset your Password")
        return redirect("users:reset_password")
    else:
        messages.error(request, "This reset link has expired.")
        return redirect("users:reset_password")


def reset_password(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Password do not match")
            return redirect("users:reset_password")
        else:
            uid = request.session.get("uid")
            user = models.User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful")
            return redirect("users:login")
    else:
        return render(request, "users/reset_password.html")


def github_auth(request):
    client_id = settings.GITHUB_ID

    redirect_uri = "http://localhost:8000/accounts/auth/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    """Because I got tired of typing return redirect(url)"""

    pass


def github_auth_callback(request):
    code = request.GET.get("code", None)

    try:
        if code is not None:
            client_secret = settings.GITHUB_SECRET_KEY
            client_id = settings.GITHUB_ID
            result = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            response_json = result.json()
            error = response_json.get("error", None)
            if error is not None:
                raise GithubException()
            else:
                access_token = response_json.get("access_token", None)
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"},
                )
                github_profile_json = profile_request.json()

                username = github_profile_json.get("login", None)
                if username is not None:
                    name = github_profile_json.get("name", None)
                    email = github_profile_json.get("email", None)
                    try:
                        user = models.User.objects.get(email=email)
                        if user is None:
                            raise GithubException()
                        if user.login_method != models.User.LOGIN_GITHUB and user.login_method != None:
                            messages.error(request, f"Invalid Login method. Login with {user.login_method} instead")
                            raise GithubException()
                    except models.User.DoesNotExist:
                        username = email.split("@")[0]
                        try:
                            first_name = name.split(" ")[1]
                            last_name = name.split(" ")[0]
                        except IndexError:
                            first_name = name
                            last_name = " "
                        user = models.User.objects.create(
                            username=username,
                            email=email,
                            first_name=first_name,
                            last_name=last_name,
                            login_method=models.User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()
                        user.save()
                    user.get_cart(request)
                    user.login_method = models.User.LOGIN_GITHUB
                    user.save()
                    login(request, user)
                    messages.success(request, f"Welcome {request.user.first_name}")
                    return redirect("core:home")
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        return redirect("users:login")


class UserDetailView(mixins.LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        current_user = self.request.user
        return render(request, "users/dashboard.html", {"current_user": current_user})


# class UserOrderHistory(View):
#     def get(self, request, *args, **kwargs):
#         user = self.request.user
#         orders = Order.objects.filter(user=user, is_ordered=True)
#         return render(request, "users/user_order_history.html", {"orders": orders})
