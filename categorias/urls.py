from django.urls import path
from .views import *

urlpatterns = [
    path('', Clase1.as_view()),  # /api/v1/categorias/
    path('<int:id>/', Clase2.as_view())  # /api/v1/categorias/1/
] 