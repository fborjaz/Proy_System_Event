from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, Evento, Inscripcion


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "last_name",
            "avatar",
            "date_joined",
            "is_staff",
        ]
        read_only_fields = ["date_joined", "is_staff"]


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class EventoSerializer(serializers.ModelSerializer):
    creador = UserSerializer(read_only=True)

    class Meta:
        model = Evento
        fields = "__all__"


class InscripcionSerializer(serializers.ModelSerializer):
    evento = EventoSerializer(read_only=True)
    usuario = UserSerializer(read_only=True)

    class Meta:
        model = Inscripcion
        fields = "__all__"


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["avatar"] = user.avatar.url if user.avatar else None
        token["is_staff"] = user.is_staff
        token["name"] = user.name
        token["last_name"] = user.last_name

        return token
