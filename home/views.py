from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

# Create your views here.

@require_http_methods(["GET"])
def home_inicio(request):
    return JsonResponse({
        "message": "Recetario API - Backend funcionando correctamente",
        "version": "1.0.0",
        "endpoints": {
            "admin": "/admin/",
            "api_v1": "/api/v1/",
            "categorias": "/api/v1/categorias/",
            "recetas": "/api/v1/recetas/",
            "contacto": "/api/v1/contacto/",
            "seguridad": "/api/v1/seguridad/",
            "documentacion": "/documentacion/",
            "redoc": "/redoc/"
        },
        "status": "online"
    })

