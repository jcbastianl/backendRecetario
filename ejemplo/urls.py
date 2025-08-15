from django.urls import path
from .views import Class_Ejemplo, Class_EjemploParametros , Class_EjemploUpload

urlpatterns = [
    path('', Class_Ejemplo.as_view()),  # /api/v1/ejemplo/
    path('<int:id>/', Class_EjemploParametros.as_view()),  # /api/v1/ejemplo/1/
    path('upload/', Class_EjemploUpload.as_view()),  # /api/v1/ejemplo/upload/
]