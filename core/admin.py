from django.contrib import admin
from .models import User, Evento, Inscripcion

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "last_name", "is_staff")


class EventoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "fecha_hora", "creador")


class InscripcionAdmin(admin.ModelAdmin):
    list_display = ("evento", "usuario", "fecha_inscripcion")


admin.site.register(User, UserAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Inscripcion, InscripcionAdmin)
