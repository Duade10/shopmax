from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email", "tabindex": "1"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
            self.fields


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email", "password", "phone_number")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Phone Number"}),
            "password": forms.PasswordInput(attrs={"placeholder": "Password", "class": "pwstrength"}),
        }

    password1 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
    )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
            self.fields["password"].widget.attrs["class"] = "form-control pwstrength"
            self.fields

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("That email is already taken", code="existing_user")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        print(email)
        phone_number = self.cleaned_data.get("phone_number")
        username = email.split("@")[0]
        password = self.cleaned_data.get("password")
        user.username = username
        user.phone_number = phone_number
        user.set_password(password)
        user.save()
        print(user)
        return user


class UpdateForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "phone_number")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        phone_number = self.cleaned_data.get("phone_number")
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.save()
        return user
