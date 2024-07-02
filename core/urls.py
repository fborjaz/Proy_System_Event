from django.urls import path, include
from .views import (
    CustomLoginView,
    RegisterView,
    LogoutView,
    home_view,
    EventoListView,
    EventoCreateView,
    EventoUpdateView,
    EventoDeleteView,
    InscripcionesListView,
    EventoDetailView,
    inscribirse,
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
    path("eventos/", EventoListView.as_view(), name="lista_eventos"),
    path("eventos/crear/", EventoCreateView.as_view(), name="crear_evento"),
    path('eventos/<int:pk>/inscribirse/', inscribirse, name='inscribirse'),
    path("eventos/<int:pk>/", EventoDetailView.as_view(), name="detalle_evento"),
    path('eventos/<int:pk>/editar/', EventoUpdateView.as_view(), name='editar_evento'),
    path('eventos/<int:pk>/eliminar/', EventoDeleteView.as_view(), name='eliminar_evento'),
    path('mis_inscripciones/', InscripcionesListView.as_view(), name='mis_inscripciones'),
    path("api/", include(router.urls)),
    path("api/users/<int:pk>/", get_solo_user, name="user_detail"),
    path("api/users/search/", search, name="user_search"),
]
