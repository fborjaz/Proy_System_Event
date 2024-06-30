from django.urls import path, include
from .views import (
    CustomLoginView,
    RegisterView,
    LogoutView,
    home_view,
    lista_eventos,
)
from .api_views import (
    UserViewSet,
    EventoListCreateView,
    InscripcionViewSet,
    get_solo_user,
    search,
)
from rest_framework.routers import DefaultRouter

app_name = "core"

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"eventos", EventoListCreateView, basename="evento")
router.register(r"inscripciones", InscripcionViewSet, basename="inscripcion")

urlpatterns = [
    path("", home_view, name="home"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(next_page="core:home"), name="logout"),
    path("eventos/", lista_eventos, name="lista_eventos"),
    path("api/", include(router.urls)),
    path("api/users/<int:pk>/", get_solo_user, name="user_detail"),
    path("api/users/search/", search, name="user_search"),
]
