from django.urls import path
from .views import *

urlpatterns = [
    path('', Clase1.as_view()),  # /api/v1/recetas/
    path('<int:id>/', Clase2.as_view())  # /api/v1/recetas/1/
] 