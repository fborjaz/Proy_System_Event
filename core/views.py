from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from core.forms import UserLoginForm, UserCreationForm

from .models import User, Evento
from .serializers import (
    RegisterUserSerializer,
    MyTokenObtainPairSerializer,
    UserSerializer,
)

from django.contrib.auth.views import LogoutView

from rest_framework import generics
from .models import Inscripcion
from .serializers import InscripcionSerializer

from rest_framework import viewsets
from .serializers import UserSerializer, EventoSerializer, InscripcionSerializer

# Create your views here.


def home_view(request):
    data = {"title1": "Autor | TeacherCode", "title2": "Super Mercado Economico"}
    return render(request, "pages/home.html", data)


def logout_view(request):
    LogoutView.as_view(next_page="core:home")

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_solo_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(["PUT"])
def edit_profile(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user == user:
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def search(request):
    query = request.query_params.get("query")
    if query is None:
        query = ""
    user = User.objects.filter(email__icontains=query)
    serializer = UserSerializer(user, many=True)
    return Response({"users": serializer.data})


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    if request.user.is_staff:
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_users(request):
    users = User.objects.exclude(email="admin@admin.com") if request.user.is_staff else User.objects.none()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def register(request):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save() # el serializador maneja la creación del usuario y el hash de la contraseña
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError: # Atrapa el error de integridad en caso de que el correo ya exista
            return Response({"error": "El correo electrónico ya está en uso."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class EventoListCreateView(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creador=self.request.user)  

class EventoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer

def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(
            request, data=request.POST
        )  # Pasa 'request' como primer argumento
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(
                request, email=email, password=password
            )  # Autenticación con email
            if user is not None:
                login(request, user)
                # Redirige a la página deseada después del login exitoso
                return redirect("Base")
        # Si la autenticación falla, el formulario se volverá a mostrar con los errores
    else:
        form = UserLoginForm()
    return render(request, "pages/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")  # Reemplaza 'home' con la URL de tu página de inicio
    else:
        form = UserCreationForm()
    return render(request, "pages/register.html", {"form": form})


def lista_eventos(request):
    eventos = Evento.objects.filter(creador=request.user)
    return render(request, "pages/home.html", {"eventos": eventos})
