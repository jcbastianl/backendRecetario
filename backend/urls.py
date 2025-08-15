"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# --- Configuración de Swagger (Documentación) ---
scheme_view = get_schema_view(
    openapi.Info(
        title="API de Recetas Django + Vue ",
        default_version='v1',
        description="Documentación de la API de recetas",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contacto@ejemplo.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# --- INICIO DE LA CORRECCIÓN ---

# Agrupamos TODAS las rutas de la API en una sola lista para organizarlas
api_urlpatterns = [
    path('ejemplo/', include('ejemplo.urls')),
    path('categorias/', include('categorias.urls')),
    path('recetas/', include('recetas.urls')),
    path('contacto/', include('contacto.urls')),
    path('seguridad/', include('seguridad.urls')),
    path('recetas-helper/', include('recetas_helper.urls')),
]

# --- Rutas Principales del Proyecto ---
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),

    # Un ÚNICO punto de entrada para toda la API v1 que usa la lista de arriba
    path('api/v1/', include(api_urlpatterns)),

    # --- CÓDIGO ANTIGUO COMENTADO ---
    # El problema era que tenías múltiples líneas para 'api/v1/'.
    # Django encontraba la primera ('ejemplo.urls') y nunca revisaba las demás.
    # path('api/v1/', include('ejemplo.urls')),
    # path('api/v1/', include('categorias.urls')),
    # path('api/v1/', include('recetas.urls')),
    # path('api/v1/', include('contacto.urls')),
    # path('api/v1/', include('seguridad.urls')),
    # path('api/v1/', include('recetas_helper.urls')),
    # --- FIN DEL CÓDIGO ANTIGUO ---

    # Rutas para la documentación de la API
    path('documentacion/', scheme_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', scheme_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# --- FIN DE LA CORRECCIÓN ---

# Esta línea es para servir archivos de medios (imágenes) durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)