"""
URL configuration for System_Event project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from core import views

urlpatterns = [
    # URLs de la aplicación de administración de Django
    path("admin/", admin.site.urls),

    # URLs de la aplicación principal (core)
    path("", views.home, name="base"),  # URL para la página de inicio
    path("signup/", views.signup, name="signup"),  # URL para el registro de usuarios
    path("signin/", views.AppLoginView.as_view(), name="signin"),  # URL para el inicio de sesión
    path("logout/", views.signout, name="logout"),  # URL para cerrar sesión


    # Incluye las URLs de la aplicación 'core' en un espacio de nombres llamado 'core'
    path('core/', include('core.urls', namespace='core')),

]
