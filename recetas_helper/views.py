from math import log
from rest_framework.views import APIView
from django.http import JsonResponse
from http import HTTPStatus
from django.http import Http404
from seguridad.decorators import logueado
from django.contrib.auth.models import User
from recetas.serializers import *
from recetas.models import Receta
from dotenv import load_dotenv
from django.utils.dateformat import DateFormat
import os
from datetime import datetime
from categorias.models import Categoria
from django.core.files.storage import FileSystemStorage

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class Clase1(APIView):
    
    @logueado()
    @swagger_auto_schema(
        operation_description="Editar foto de una receta",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la receta'),
                'foto': openapi.Schema(type=openapi.TYPE_FILE, description='Nueva imagen de la receta')
            },
            required=['id', 'foto']
        ),
        responses={
            HTTPStatus.OK: openapi.Response(description="Foto actualizada correctamente"),
            HTTPStatus.BAD_REQUEST: openapi.Response(description="Error en los datos enviados"),
            HTTPStatus.UNAUTHORIZED: openapi.Response(description="No autorizado")
        }
    )
    def post(self, request):
        if request.data.get('id') is None or not request.data['id']:
            return JsonResponse({"estado": "error", "mensaje": "El campo id es obligatorio"}, status=HTTPStatus.BAD_REQUEST)

        try:
            existe = Receta.objects.get(pk=request.data['id'])
            anterior = existe.foto
        except Receta.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "La receta no existe"}, status=HTTPStatus.BAD_REQUEST)
        
        fs = FileSystemStorage()
        try:
            foto = f"{datetime.now().timestamp()}{os.path.splitext(str(request.FILES['foto'].name))[1]}"
        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": "Error al procesar la imagen: " + str(e)}, status=HTTPStatus.BAD_REQUEST)
        
        if request.FILES['foto'].content_type == 'image/jpeg' or request.FILES['foto'].content_type == 'image/png':
            try:
                fs.save(f"recetas/{foto}", request.FILES['foto'])
                fs.url(request.FILES['foto'])
            except Exception as e:
                return JsonResponse({"estado": "error", "mensaje": "Error al procesar la imagen: " + str(e)}, status=HTTPStatus.BAD_REQUEST)
            
            try:
                Receta.objects.filter(pk=request.data['id']).update(
                    foto=foto
                )
                # Eliminar la foto anterior solo si existe
                if anterior and anterior.strip() != '':
                    # Intentar con ruta completa primero
                    ruta_completa = os.path.join("uploads", "recetas", anterior)
                    if os.path.exists(ruta_completa):
                        try:
                            os.remove(ruta_completa)
                            print(f"Foto anterior eliminada: {ruta_completa}")
                        except Exception as e:
                            print(f"Error al eliminar foto anterior: {str(e)}")
                    else:
                        print(f"Foto anterior no encontrada en: {ruta_completa}")
                
                return JsonResponse({"estado": "ok", "mensaje": "Foto actualizada correctamente"}, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse({"estado": "error", "mensaje": f"Error al actualizar la foto: {str(e)}"}, status=HTTPStatus.BAD_REQUEST)
        else:
            return JsonResponse({"estado": "error", "mensaje": "El formato de la imagen no es valido"}, status=HTTPStatus.BAD_REQUEST)
        
class Clase2(APIView):
    
    @swagger_auto_schema(
        operation_description="Obtener receta por slug",
        responses={
            HTTPStatus.OK: openapi.Response(
                description="Receta obtenida exitosamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'nombre': openapi.Schema(type=openapi.TYPE_STRING),
                                'slug': openapi.Schema(type=openapi.TYPE_STRING),
                                'imagen': openapi.Schema(type=openapi.TYPE_STRING),
                                'descripcion': openapi.Schema(type=openapi.TYPE_STRING),
                                'tiempo': openapi.Schema(type=openapi.TYPE_STRING),
                                'categoria_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'categoria': openapi.Schema(type=openapi.TYPE_STRING),
                                'fecha': openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        )
                    }
                )
            ),
            HTTPStatus.NOT_FOUND: openapi.Response(description="Receta no encontrada")
        }
    )
    def get(self, request, slug):
        try:
            data = Receta.objects.filter(slug=slug).get()
            return JsonResponse({
                "data": {
                    "id": data.id,
                    "nombre": data.nombre,
                    "slug": data.slug,
                    "imagen": f"{os.getenv('BASE_URL')}/uploads/recetas/{data.foto}" ,
                    "descripcion": data.descripcion,
                    "tiempo": data.tiempo,
                    "categoria_id": data.categoria_id,
                    "categoria": data.categoria.nombre,
                    "fecha": DateFormat(data.fecha).format("%d-%m-%Y")
                }
            }, status=HTTPStatus.OK)
        except Receta.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "La receta no existe"}, status=HTTPStatus.NOT_FOUND)
            

class Clase3(APIView):
    
    @swagger_auto_schema(
        operation_description="Obtener 3 recetas aleatorias para la página de inicio",
        responses={
            HTTPStatus.OK: openapi.Response(
                description="Recetas aleatorias obtenidas exitosamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_OBJECT)
                        )
                    }
                )
            )
        }
    )
    def get(self , request):
        data = Receta.objects.order_by('?').all()[:3]
        datos_json = RecetaSerializer(data, many=True)
        return JsonResponse({"data": datos_json.data}, status=HTTPStatus.OK)



        
class Clase4(APIView):
    
    @logueado()
    @swagger_auto_schema(
        operation_description="Obtener recetas de un usuario específico",
        responses={
            HTTPStatus.OK: openapi.Response(
                description="Recetas del usuario obtenidas exitosamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_OBJECT)
                        )
                    }
                )
            ),
            HTTPStatus.BAD_REQUEST: openapi.Response(description="Usuario no existe"),
            HTTPStatus.UNAUTHORIZED: openapi.Response(description="No autorizado")
        }
    )
    def get(self, request, id):
        try:
            existe = User.objects.get(pk=id)
        except User.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "El usuario no existe"}, status=HTTPStatus.BAD_REQUEST)
        
        data = Receta.objects.filter(user_id=id).order_by('-id').all()
        datos_json = RecetaSerializer(data, many=True)
        return JsonResponse({"data": datos_json.data}, status=HTTPStatus.OK)
    
class Clase5(APIView):
    
    @swagger_auto_schema(
        operation_description="Buscar recetas por categoría y texto",
        manual_parameters=[
            openapi.Parameter(
                'categoria_id',
                openapi.IN_QUERY,
                description="ID de la categoría para filtrar",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Texto a buscar en el nombre de la receta",
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={
            HTTPStatus.OK: openapi.Response(
                description="Recetas encontradas",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_OBJECT)
                        )
                    }
                )
            ),
            HTTPStatus.BAD_REQUEST: openapi.Response(description="Categoría requerida o no existe")
        }
    )
    def get(self, request):
        if request.GET.get("categoria_id") is None or not request.GET.get("categoria_id"):
            return JsonResponse({"estado": "error", "mensaje": "El campo categoria_id es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        try:
            existe = Categoria.objects.filter(id=request.GET.get("categoria_id")).get()

        except Categoria.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "La categoría no existe"}, status=HTTPStatus.BAD_REQUEST)

        #select * from recetas where categoria_id=6 and nombre like '%algo%'
        data = Receta.objects.filter(categoria_id=request.GET.get("categoria_id")).filter(nombre__icontains=request.GET.get("search")).order_by('-id').all()
        datos_json = RecetaSerializer(data, many=True)
        return JsonResponse({"data": datos_json.data}, status=HTTPStatus.OK)