from django.urls import path
from .views import *

urlpatterns = [
    # editar foto
    path('editar/foto/', Clase1.as_view()),  # /api/v1/recetas-helper/editar/foto/
    path('slug/<str:slug>/', Clase2.as_view()),  # /api/v1/recetas-helper/slug/mi-receta/
    path('home/', Clase3.as_view()),  # /api/v1/recetas-helper/home/
    path('panel/<int:id>/', Clase4.as_view()),  # /api/v1/recetas-helper/panel/1/
    path('buscador/', Clase5.as_view()),  # /api/v1/recetas-helper/buscador/
] 