from http import HTTPStatus
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Categoria
from .serializers import CategoriaSerializer
from django.http import Http404
from django.utils.text import slugify

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class Clase1(APIView):
    
    @swagger_auto_schema(
        operation_description="Obtener todas las categorías",
        responses={
            HTTPStatus.OK: openapi.Response(
                description="Lista de categorías obtenida exitosamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'nombre': openapi.Schema(type=openapi.TYPE_STRING),
                                    'slug': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            )
                        )
                    }
                )
            )
        }
    )
    def get(self, request):
        data = Categoria.objects.order_by('-id').all()
        datos_json = CategoriaSerializer(data, many=True)
        # return JsonResponse(datos_json.data)
        return JsonResponse({"data": datos_json.data}, status=HTTPStatus.OK)
    
    @swagger_auto_schema(
        operation_description="Crear una nueva categoría",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la categoría')
            },
            required=['nombre']
        ),
        responses={
            HTTPStatus.CREATED: openapi.Response(description="Categoría creada correctamente"),
            HTTPStatus.BAD_REQUEST: openapi.Response(description="Error en los datos enviados")
        }
    )
    def post(self, request):
        if request.data.get("nombre") == None or not request.data['nombre']:
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        try:
            Categoria.objects.create(
                nombre=request.data['nombre'])
            return JsonResponse({"message": "Categoria created successfully"}, status=HTTPStatus.CREATED)
        except Exception as e:
            raise Http404

class Clase2(APIView):
    
    @swagger_auto_schema(
        operation_description="Obtener una categoría por ID",
        responses={
            HTTPStatus.OK: openapi.Response(
                description="Categoría obtenida exitosamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'nombre': openapi.Schema(type=openapi.TYPE_STRING),
                                'slug': openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        )
                    }
                )
            ),
            HTTPStatus.NOT_FOUND: openapi.Response(description="Categoría no encontrada")
        }
    )
    def get(self, request, id):
        try:
            data = Categoria.objects.get(id=id)
            datos_json = CategoriaSerializer(data)
            return JsonResponse({"data": {"id":data.id, "nombre":data.nombre, "slug":data.slug}}, status= HTTPStatus.OK)
        except Categoria.DoesNotExist:
            return JsonResponse({"error": "Categoria not found"}, status=HTTPStatus.NOT_FOUND)
        except Exception as e:
            raise Exception(f"Internal Server Error: {str(e)}")
    
    @swagger_auto_schema(
        operation_description="Actualizar una categoría",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nuevo nombre de la categoría')
            },
            required=['nombre']
        ),
        responses={
            HTTPStatus.OK: openapi.Response(description="Categoría actualizada correctamente"),
            HTTPStatus.BAD_REQUEST: openapi.Response(description="Error en los datos enviados"),
            HTTPStatus.NOT_FOUND: openapi.Response(description="Categoría no encontrada")
        }
    )
    def put(self, request, id):
        if request.data.get("nombre") == None:
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es requerido"}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get("nombre"):
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre no puede estar vacío"}, status=HTTPStatus.BAD_REQUEST)
        try:
            data= Categoria.objects.filter(pk=id).get()
            # Generar slug automáticamente basado en el nombre
            nuevo_slug = slugify(request.data.get("nombre"))
            Categoria.objects.filter(pk=id).update(
                nombre=request.data.get("nombre"), 
                slug=nuevo_slug
            )
            return JsonResponse({"message": "Categoria updated successfully"}, status=HTTPStatus.OK)
        except Categoria.DoesNotExist:
            raise Http404
        
    @swagger_auto_schema(
        operation_description="Eliminar una categoría",
        responses={
            HTTPStatus.OK: openapi.Response(description="Categoría eliminada correctamente"),
            HTTPStatus.NOT_FOUND: openapi.Response(description="Categoría no encontrada")
        }
    )
    def delete(self, request, id):
        try:
            data = Categoria.objects.filter(pk=id).get()
            Categoria.objects.filter(pk=id).delete()
            return JsonResponse({"message": "Categoria deleted successfully"}, status=HTTPStatus.OK)  
        except Categoria.DoesNotExist:
            return Http404