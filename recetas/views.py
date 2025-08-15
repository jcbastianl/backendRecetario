# Importa APIView, JsonResponse, HTTPStatus, Http404 y slugify
from email import header
import os
import datetime
from http import HTTPStatus
from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from django.utils.text import slugify
from .models import Receta
from categorias.models import Categoria
from .serializers import RecetaSerializer
from dotenv import load_dotenv
from django.core.files.storage import FileSystemStorage
from recetas.models import *
from seguridad.decorators import logueado

from jose import jwt
from django.conf import settings
from django.utils.dateformat import DateFormat

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Load environment variables
load_dotenv()


class Clase1(APIView):
    
    @swagger_auto_schema(
        operation_description="Obtener todas las recetas",
        responses={
            HTTPStatus.OK: openapi.Response(
                description="Lista de recetas obtenida exitosamente",
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
                                    'slug': openapi.Schema(type=openapi.TYPE_STRING),
                                    'tiempo': openapi.Schema(type=openapi.TYPE_STRING),
                                    'descripcion': openapi.Schema(type=openapi.TYPE_STRING),
                                    'fecha': openapi.Schema(type=openapi.TYPE_STRING),
                                    'categoria': openapi.Schema(type=openapi.TYPE_STRING),
                                    'categoria_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'imagen': openapi.Schema(type=openapi.TYPE_STRING),
                                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'user': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            )
                        )
                    }
                )
            )
        }
    )
    def get(self, request):
        data = Receta.objects.order_by('-id').all()
        datos_json = RecetaSerializer(data, many=True)
        return JsonResponse({"data": datos_json.data}, status=HTTPStatus.OK)

    @logueado()
    @swagger_auto_schema(
        operation_description="Crear una nueva receta",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la receta'),
                'tiempo': openapi.Schema(type=openapi.TYPE_STRING, description='Tiempo de preparación'),
                'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción de la receta'),
                'categoria_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la categoría'),
                'foto': openapi.Schema(type=openapi.TYPE_FILE, description='Imagen de la receta')
            },
            required=['nombre', 'tiempo', 'descripcion', 'categoria_id', 'foto']
        ),
        responses={
            HTTPStatus.CREATED: openapi.Response(description="Receta creada correctamente"),
            HTTPStatus.BAD_REQUEST: openapi.Response(description="Error en los datos enviados"),
            HTTPStatus.UNAUTHORIZED: openapi.Response(description="No autorizado")
        }
    )
    def post(self, request):
        if request.data.get("nombre") is None or not request.data['nombre']:
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("tiempo") is None or not request.data['tiempo']:
            return JsonResponse({"estado": "error", "mensaje": "El campo tiempo es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("descripcion") is None or not request.data['descripcion']:
            return JsonResponse({"estado": "error", "mensaje": "El campo descripcion es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get("categoria_id") is None or not request.data['categoria_id']:
            return JsonResponse({"estado": "error", "mensaje": "El campo categoria_id es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        #validamos que no exista la categoria_id
        try:
            categoria = Categoria.objects.filter(pk=request.data.get('categoria_id')).get()
        except Categoria.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "La categoria no existe"}, status=HTTPStatus.BAD_REQUEST)
        
        
        #select * from recetas where nombre = request.data.get('nombre')
        #validamos que el nombre de la receta este disponible
        if Receta.objects.filter(nombre=request.data.get('nombre')).exists():
            return JsonResponse({"estado": "error", "mensaje": "El nombre de la receta ya existe"}, status=HTTPStatus.BAD_REQUEST)
        
        fs = FileSystemStorage()
        try:
            foto = f"{datetime.datetime.now().timestamp()}{os.path.splitext(str(request.FILES['foto'].name))[1]}"
        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": "Error al procesar la imagen: " + str(e)}, status=HTTPStatus.BAD_REQUEST)
        if request.FILES['foto'].content_type in ('image/jpeg','image/png'):
            # Guardar archivo (una sola vez)
            try:
                fs.save(f"recetas/{foto}", request.FILES['foto'])
            except Exception as e:
                return JsonResponse({"estado": "error", "mensaje": f"Error al procesar la imagen: {str(e)}"}, status=HTTPStatus.BAD_REQUEST)

            # Decodificar token
            try:
                header = request.headers.get('Authorization','').split(' ')
                if len(header) != 2:
                    return JsonResponse({"estado": "error", "mensaje": "Token no provisto correctamente"}, status=HTTPStatus.UNAUTHORIZED)
                resuelto = jwt.decode(header[1], settings.SECRET_KEY, algorithms=['HS512'])
            except Exception:
                return JsonResponse({"estado": "error", "mensaje": "Token inválido"}, status=HTTPStatus.UNAUTHORIZED)

            # Crear receta
            try:
                Receta.objects.create(
                    nombre=request.data['nombre'],
                    tiempo=request.data.get('tiempo'),
                    descripcion=request.data.get('descripcion'),
                    categoria_id=request.data.get('categoria_id'),
                    foto=foto,
                    user_id=resuelto['id'],
                )
                return JsonResponse({"estado": "ok", "mensaje": "Receta creada correctamente"}, status=HTTPStatus.CREATED)
            except Exception as e:
                return JsonResponse({"estado": "error", "mensaje": f"Error al crear la receta: {str(e)}"}, status=HTTPStatus.BAD_REQUEST)
        else:
            return JsonResponse({"estado": "error", "mensaje": "El formato de imagen no es válido. Solo se acepta JPG o PNG"}, status=HTTPStatus.BAD_REQUEST)



class Clase2(APIView):
    def get(self, request, id):
        try:
            data = Receta.objects.get(id=id)
            
            return JsonResponse({
                "data": {
                    "id": data.id,
                    "nombre": data.nombre,
                    "descripcion": data.descripcion,
                    "tiempo": data.tiempo,
                    "categoria_id": data.categoria_id,
                    "user_id": data.user_id,
                    "user": data.user.first_name if data.user else None,
                    "fecha": DateFormat(data.fecha).format('d/m/Y') if data.fecha else None,
                    "foto": f"{os.getenv('BASE_URL')}uploads/recetas/{data.foto}" if data.foto else None
                }
            }, status=HTTPStatus.OK)
        except Receta.DoesNotExist:
            return JsonResponse({"error": "Receta not found"}, status=HTTPStatus.NOT_FOUND)

    def put (self, request, id):
    
        try:
           data = Receta.objects.filter(pk=id).get()
        except Receta.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Receta not found"}, status=HTTPStatus.NOT_FOUND)
        
        try:
            Receta.objects.filter(pk=id).update(
                nombre=request.data.get('nombre', data.nombre),
                slug=slugify(request.data.get('nombre', data.nombre)),
                tiempo=request.data.get('tiempo', data.tiempo),
                descripcion=request.data.get('descripcion', data.descripcion),
                categoria_id=request.data.get('categoria_id', data.categoria_id),
            )
            return JsonResponse({"estado": "ok", "mensaje": "Receta updated successfully"}, status=HTTPStatus.OK)
       
        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": f"Error al actualizar la receta: {str(e)}"}, status=HTTPStatus.BAD_REQUEST)
        
    
    def delete(self, request, id):
        try:
            data = Receta.objects.get(pk=id)
        except Receta.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Receta not found"}, status=HTTPStatus.NOT_FOUND)
        
        # Delete the associated image file if it exists
        if data.foto:
            import os
            file_path = os.path.join(settings.MEDIA_ROOT, 'recetas', str(data.foto))
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting file: {e}")
        
        # Delete the recipe
        data.delete()
        return JsonResponse({"estado": "ok", "mensaje": "Receta deleted successfully"}, status=HTTPStatus.OK)

