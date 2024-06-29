from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import User


class UserCreationForm(UserCreationForm):
    confirm_password = forms.CharField(
        label=_("Confirmar contraseña"),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)
        widgets = {"email": forms.EmailInput(attrs={"class": "form-control"})}

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(_("Las contraseñas no coinciden."))


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("email", "password")
