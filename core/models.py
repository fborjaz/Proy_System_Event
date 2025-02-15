from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# Create your models here.

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Debes tener un correo electronico")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        # Aquí puedes solicitar los datos adicionales
        name = input("Nombre: ")
        last_name = input("Apellido: ")
        avatar = input("Avatar (opcional): ")

        extra_fields.setdefault("name", name)
        extra_fields.setdefault("last_name", last_name)
        if avatar:  # Si se proporciona un valor para avatar, lo asigna
            extra_fields.setdefault("avatar", avatar)

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    avatar = models.ImageField(default="avatar.png")
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-date_joined"]

    def eventos_inscriptos(self):
        return Evento.objects.filter(
            inscripcion__usuario=self, inscripcion__estado="confirmada"
        )


class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=200)
    fecha_hora = models.DateTimeField()
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
    capacidad = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='images/', null=True, blank=True, default='images/default_event_image.jpg')

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.imagen:  # Si no se ha subido una imagen
            self.imagen = 'images/default_event_image.jpg'  # Asignar la imagen por defecto
        super().save(*args, **kwargs)  

    def clean(self):
        if self.fecha_hora and self.fecha_hora < timezone.now():
            raise ValidationError("La fecha del evento debe ser futura.")

    def cupos_disponibles(self):
        return max(0, self.capacidad - self.inscripcion_set.count())

    @property
    def inscriptos(self):
        return self.inscripcion_set.filter(estado="confirmada")


class Inscripcion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    ESTADO_CHOICES = [
        ("confirmada", "Confirmada"),
        ("espera", "En espera"),
        ("cancelada", "Cancelada"),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default="espera")

    class Meta:
        unique_together = ("evento", "usuario")

    def clean(self):
        if self.fecha_inscripcion > self.evento.fecha_hora:
            raise ValidationError(
                "La fecha de inscripción no puede ser posterior a la fecha del evento."
            )
