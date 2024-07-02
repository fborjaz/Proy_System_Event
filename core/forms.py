from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import User, Evento
from django.utils import timezone


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email","name","last_name","avatar",)  # Incluye todos los campos de tu modelo

    def clean_password2(self):
        # Validación de que las contraseñas coincidan
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("email", "password")

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'ubicacion', 'fecha_hora', 'capacidad', 'imagen']

    def clean_fecha_hora(self):
        fecha_hora = self.cleaned_data['fecha_hora']
        if fecha_hora <= timezone.now():
            raise forms.ValidationError("La fecha y hora del evento deben ser futuras.")
        return fecha_hora
