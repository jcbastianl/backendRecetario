from django.urls import path
from .views import *

urlpatterns = [
    path('registro/', Clase1.as_view()),  # /api/v1/seguridad/registro/
    path('verificacion/<str:token>/', Clase2.as_view()),  # /api/v1/seguridad/verificacion/token/
    path('login/', Clase3.as_view()),  # /api/v1/seguridad/login/
] 