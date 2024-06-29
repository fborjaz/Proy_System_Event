from django.urls import path
from core import views
from .views import Evento, Inscripcion

app_name = "core"

urlpatterns = [
    path('evento/', Evento.as_view(), name='evento'),
    path('inscripcion/', Inscripcion.as_view(), name='inscripcion'),
]
