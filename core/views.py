# views.py
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import UserLoginForm, CustomUserCreationForm
from .models import Evento
from django.contrib.auth import login


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "pages/login.html"

    def get_success_url(self):
        next_url = self.request.POST.get("next")
        if next_url:
            return next_url
        else:
            return reverse_lazy("core:home")


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "pages/register.html"
    success_url = reverse_lazy("core:home")  # Cambia 'core:home' a tu URL de inicio deseada

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # Inicia sesión al usuario después del registro
        return response

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request, error)
        return self.render_to_response(self.get_context_data(form=form))


def home_view(request):
    data = {"title1": "Autor | Frank Borja", "title2": "Sistemas de gestion de eventos"}
    return render(request, "pages/home.html", data)


def logout_view(request):
    logout(request) 
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect("core:home")


def lista_eventos(request):
    eventos = Evento.objects.all()  # Mostrar todos los eventos
    return render(request, "pages/home.html", {"eventos": eventos})
