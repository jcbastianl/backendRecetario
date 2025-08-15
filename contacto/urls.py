from django.urls import path
from .views import *

urlpatterns = [
    path('', Clase1.as_view()),  # /api/v1/contacto/
]