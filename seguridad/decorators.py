from functools import wraps
from django.http import JsonResponse
from http import HTTPStatus
from jose import jwt
from django.conf import settings
import os
import time
from datetime import datetime, timedelta
def logueado():
    def metodo(func):
        @wraps(func)
        def _decorator(request, *args, **kwargs):
            req = args[0]
            if not req.headers.get('Authorization') or req.headers.get('Authorization') == None:
                return JsonResponse({"estado": "error", "mensaje": "No autorizado"}, status=HTTPStatus.UNAUTHORIZED)
            header = req.headers.get('Authorization').split(" ")
            try:
                resuelto = jwt.decode(header[1], settings.SECRET_KEY, algorithms=['HS512'])
            except Exception as e:
                return JsonResponse({"estado": "error", "mensaje": f"Error al procesar la solicitud: {str(e)}"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
            
            if int(resuelto['exp']) > int(time.time()):
                return func(request, *args, **kwargs)
            else:
                return JsonResponse({"estado": "error", "mensaje": "Token expirado"}, status=HTTPStatus.UNAUTHORIZED)
        return _decorator
    return metodo




# def logueado():
#     def metodo(func):
#         @wraps(func)
#         def _decorator(request, *args, **kwargs):
#             # Se accede directamente a la variable 'request'
#             auth_header = request.headers.get('Authorization')
#             # Imprime el encabezado de autorización
#             print(f"Authorization={auth_header}")
#             # Llama a la función original y devuelve su resultado
#             return func(request, *args, **kwargs)
#         return _decorator
#     return metodo