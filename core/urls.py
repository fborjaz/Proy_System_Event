from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views

app_name = 'core'

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'eventos', views.EventoListCreateView, basename='evento')
router.register(r'inscripciones', views.InscripcionViewSet, basename='inscripcion')

urlpatterns = [
    path('', views.home_view, name="home"),  # URL para la página de inicio
    path('api/', include(router.urls)),  # URLs de la API
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('eventos/', views.lista_eventos, name='lista_eventos'),  # Vista tradicional para listar eventos
]
