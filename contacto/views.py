from http.client import BAD_REQUEST
from urllib import response
from .models import *
from rest_framework.views import APIView
from http import HTTPStatus
from django.http import JsonResponse
from datetime import datetime

from utilidades import utilidades
# Create your views here.

#Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Clase1(APIView):
    
    @swagger_auto_schema(
        operation_description="Endpoint para crear un contacto",
        responses={
            HTTPStatus.CREATED: openapi.Response(description="Contacto creado correctamente"),
            HTTPStatus.BAD_REQUEST: openapi.Response(description="Error al crear el contacto"),
            HTTPStatus.INTERNAL_SERVER_ERROR: openapi.Response(description="Error interno del servidor")
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del contacto'),
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del contacto'),
                'telefono': openapi.Schema(type=openapi.TYPE_STRING, description='Telefono del contacto'),
                'mensaje': openapi.Schema(type=openapi.TYPE_STRING, description='Mensaje del contacto')
            },
            required=['nombre', 'correo', 'telefono', 'mensaje'],
        )
    )
    
    def post(self, request):
        if request.data.get("nombre") == None or not request.data['nombre']:
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
 
        if request.data.get("correo") == None or not request.data['correo']:
            return JsonResponse({"estado": "error", "mensaje": "El campo correo es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
     
        if request.data.get("telefono") == None or not request.data['telefono']:
            return JsonResponse({"estado": "error", "mensaje": "El campo telefono es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        if request.data.get("mensaje") == None or not request.data['mensaje']:
            return JsonResponse({"estado": "error", "mensaje": "El campo mensaje es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        try:
            Contacto.objects.create(
                nombre=request.data['nombre'],
                correo=request.data['correo'],
                telefono=request.data['telefono'],
                mensaje=request.data['mensaje'],
                fecha=datetime.now()
            )  
            
            
            html = f""" 
                <h1>Nuevo mensaje de sitio web</h1>
                <ul>
                    <li><strong>Nombre:</strong> {request.data['nombre']}</li>
                    <li><strong>Correo:</strong> {request.data['correo']}</li>
                    <li><strong>Telefono:</strong> {request.data['telefono']}</li>
                    <li><strong>Mensaje:</strong> {request.data['mensaje']}</li>
                </ul>
            """

            utilidades.sendMail(html, "Prueba curso", request.data['correo'])
            
        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": "Error al crear el contacto: " + str(e)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
        
        return JsonResponse({"estado": "ok", "mensaje": "Contacto creado correctamente"}, status=HTTPStatus.CREATED)