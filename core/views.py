from django.shortcuts import render, redirect
from django.contrib.auth import login

# Create your views here.

def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos/lista_eventos.html', {'eventos': eventos})
