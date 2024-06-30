from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import Evento, Inscripcion


User = get_user_model()


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

    def validate_email(self, value):
        # Validar que el correo electrónico sea único
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Este correo electrónico ya está registrado."
            )
        return value


class EventoSerializer(serializers.ModelSerializer):
    creador = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )  # Solo el ID del creador

    class Meta:
        model = Evento
        fields = "__all__"


class InscripcionSerializer(serializers.ModelSerializer):
    evento = serializers.PrimaryKeyRelatedField(queryset=Evento.objects.all())
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

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
