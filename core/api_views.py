# api_views.py
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import NotFound, PermissionDenied
from django.db import IntegrityError

from .models import User, Evento, Inscripcion
from .serializers import (
    RegisterUserSerializer,
    MyTokenObtainPairSerializer,
    UserSerializer,
    EventoSerializer,
    InscripcionSerializer,
)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_solo_user(request, pk):
    """
    Obtiene los detalles de un usuario específico por su ID (pk).

    Requiere autenticación.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise NotFound("Usuario no encontrado")

    serializer = UserSerializer(user)
    return Response(serializer.data)


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


# Vistas para obtener, editar y eliminar usuarios (con mejor manejo de errores)
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return User.objects.get(pk=self.kwargs["pk"])
        except User.DoesNotExist:
            raise NotFound("Usuario no encontrado")


class UserEditView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return User.objects.get(email=self.kwargs["email"])
        except User.DoesNotExist:
            raise NotFound("Usuario no encontrado")

    def perform_update(self, serializer):
        if self.request.user == serializer.instance:
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para editar este usuario")


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return User.objects.get(pk=self.kwargs["pk"])
        except User.DoesNotExist:
            raise NotFound("Usuario no encontrado")

    def perform_destroy(self, instance):
        if self.request.user.is_staff:
            instance.delete()
        else:
            raise PermissionDenied("No tienes permiso para eliminar este usuario")


@api_view(["GET"])
def search(request):
    query = request.query_params.get("query")
    if query is None:
        query = ""
    user = User.objects.filter(email__icontains=query)
    serializer = UserSerializer(user, many=True)
    return Response({"users": serializer.data})


@api_view(["POST"])
def register(request):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()  # el serializador maneja la creación del usuario y el hash de la contraseña
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (IntegrityError):  # Atrapa el error de integridad en caso de que el correo ya exista
            return Response(
                {"error": "El correo electrónico ya está en uso."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_users(request):
    users = (
        User.objects.exclude(email="admin@admin.com")
        if request.user.is_staff
        else User.objects.none()
    )
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
