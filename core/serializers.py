from serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, Evento, Inscripcion


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "last_name", "id", "avatar"]


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "last_name", "password"]


class EventoSerializer(serializers.ModelSerializer):
    creador = UserSerializer(
        read_only=True
    )  # Muestra el creador como un objeto anidado

    class Meta:
        model = Evento
        fields = ["id", "nombre", "descripcion", "ubicacion", "fecha_hora", "creador"]


class InscripcionSerializer(serializers.ModelSerializer):
    evento = EventoSerializer(read_only=True)
    usuario = UserSerializer(read_only=True)

    class Meta:
        model = Inscripcion
        fields = ["id", "evento", "usuario", "fecha_inscripcion"]

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["avatar"] = user.avatar.url
        token["is_staff"] = user.is_staff
        token["name"] = user.name
        token["last_name"] = user.last_name

        return token
