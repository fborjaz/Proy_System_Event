# views.py

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, CustomUserCreationForm, EventoForm
from .models import Evento, Inscripcion
from django.http import HttpResponseRedirect
from django.urls import reverse


# -------------------------
# Vistas de autenticación:
# -------------------------


class CustomLoginView(LoginView):
    """Vista personalizada para el inicio de sesión."""

    form_class = UserLoginForm
    template_name = "pages/login.html"

    def get_success_url(self):
        """Redirecciona a la página apropiada después del inicio de sesión."""
        next_url = self.request.POST.get("next")
        if next_url:
            return next_url
        else:
            return reverse_lazy("core:home")


class RegisterView(CreateView):
    """Vista para el registro de nuevos usuarios."""

    form_class = CustomUserCreationForm
    template_name = "pages/register.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        """Inicia sesión al usuario después de un registro exitoso."""
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def form_invalid(self, form):
        """Muestra mensajes de error si el formulario no es válido."""
        for field in form:
            for error in field.errors:
                messages.error(self.request, error)
        return self.render_to_response(self.get_context_data(form=form))


# -------------------------
# Vistas para la página de inicio:
# -------------------------


def home_view(request):
    """Renderiza la página de inicio."""
    data = {"title": "Home", "title2": "Sistemas de gestión de eventos"}
    return render(request, "pages/home.html", data)


# -------------------------
# Vistas para eventos:
# -------------------------


class EventoListView(ListView):
    """Vista para listar todos los eventos."""

    model = Evento
    template_name = "pages/lista_eventos.html"
    context_object_name = "eventos"


class EventoDetailView(DetailView):
    """Vista para mostrar los detalles de un evento."""

    model = Evento
    template_name = "pages/detalle_evento.html"
    context_object_name = "evento"

    def get_context_data(self, **kwargs):
        """Agrega información extra al contexto de la plantilla, como si el usuario está inscrito o no al evento."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["esta_inscrito"] = self.request.user in self.object.inscriptos.all()
        return context


class EventoCreateView(LoginRequiredMixin, CreateView):
    """Vista para crear un nuevo evento (requiere inicio de sesión)."""

    model = Evento
    form_class = EventoForm
    template_name = "pages/crear_evento.html"
    success_url = reverse_lazy('core:lista_eventos')

    def form_valid(self, form):
        form.instance.creador = self.request.user
        return super().form_valid(form)


class EventoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Vista para editar un evento existente (requiere inicio de sesión y ser el creador o staff)."""

    model = Evento
    form_class = EventoForm
    template_name = "pages/editar_evento.html"
    success_url = reverse_lazy("core:lista_eventos")

    def test_func(self):
        """Verifica si el usuario tiene permiso para editar el evento."""
        evento = self.get_object()
        return self.request.user == evento.creador or self.request.user.is_staff


class EventoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Vista para eliminar un evento (requiere inicio de sesión y ser el creador o staff)."""

    model = Evento
    template_name = "pages/eliminar_evento.html"
    success_url = reverse_lazy("core:lista_eventos")

    def test_func(self):
        """Verifica si el usuario tiene permiso para eliminar el evento."""
        evento = self.get_object()
        return self.request.user == evento.creador or self.request.user.is_staff


# -------------------------
# Vistas para inscripciones:
# -------------------------


class InscripcionesListView(LoginRequiredMixin, ListView):
    """Vista para listar las inscripciones de un usuario."""

    model = Inscripcion
    template_name = "eventos/mis_inscripciones.html"
    context_object_name = "inscripciones"

    def get_queryset(self):
        """Obtiene las inscripciones del usuario actual."""
        return Inscripcion.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        """Agrega un mensaje si el usuario no tiene inscripciones."""
        context = super().get_context_data(**kwargs)
        if not context["inscripciones"]:
            context["mensaje_no_inscripciones"] = (
                "No estás inscrito en ningún evento. ¡Revisa la lista de eventos!"
            )
        return context


@login_required
def inscribirse(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if request.method == "POST":
        if evento.cupos_disponibles() > 0:  # Verificar si hay cupos disponibles
            inscripcion, created = Inscripcion.objects.get_or_create(
                evento=evento, usuario=request.user
            )
            if created:
                evento.capacidad -= 1  # Reducir la capacidad en 1
                evento.save()
                messages.success(request, "Te has inscrito al evento exitosamente.")
            else:
                messages.info(request, "Ya estás inscrito en este evento.")
        else:
            messages.error(
                request, "Lo sentimos, el evento no tiene cupos disponibles."
            )

        # Redirigir a la misma página (lista de eventos) con el mensaje
        return redirect(reverse("core:lista_eventos"))
