from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse , Http404
from datetime import datetime  # Asegúrate de importar datetime al inicio del archivo
from rest_framework.response import Response
from http import HTTPStatus
#upload
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.
class Class_Ejemplo(APIView):
    def get(self, request):
        #return HttpResponse(f"Metodo GET parametros id={request.GET.get('id',None)} slug={request.GET.get('slug',None)}")
        return JsonResponse(
            {
                "estado": "ok",
                "mensaje": f"Metodo GET con el id {request.GET.get('id', None)} slug {request.GET.get('slug', None)}"
            },
            status=200
        )

    def post(self, request):
        if request.data.get('correo')==None or request.data.get('password')==None:
            raise Http404("No se ha proporcionado el correo o la contraseña")

        #return HttpResponse("Metodo POST")
        return JsonResponse({"estado": "ok", "mensaje": f"Método POST con el correo {request.data.get('correo')} y la contraseña {request.data.get('password')}"},HTTPStatus.OK)
    # def put(self, request):
    #     return HttpResponse("Metodo PUT")
    
    # def delete(self, request):
    #     return HttpResponse("Metodo DELETE")
class Class_EjemploParametros(APIView):
    def get(self, request, id):
        return HttpResponse(f"Metodo GET con parametro: {id}")
    
    def put(self, request, id):
        return HttpResponse(f"Metodo POST con parametro: {id}")
    
    def put(self, request, id):
        return HttpResponse(f"Metodo PUT con parametro: {id}")
    
    def delete(self, request , id):
        return HttpResponse(f"Metodo DELETE con parametro: {id}")
    
class Class_EjemploUpload(APIView):

    def post(self, request):
        fs = FileSystemStorage()
        fecha = datetime.now()
        foto = f"{datetime.timestamp(fecha)}{os.path.splitext(str(request.FILES['file'].name))[1]}"
        fs.save(f"ejemplo/{foto}", request.FILES['file'])
        fs.url(request.FILES['file'])
        return JsonResponse({"estado":"ok", "mensaje":"Se subio el archivo"})