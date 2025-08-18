import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_control
import mimetypes

@require_GET
@cache_control(max_age=3600)  # Cache por 1 hora
def serve_media(request, path):
    """
    Vista personalizada para servir archivos media en producción.
    """
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Verificar que el archivo existe
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise Http404("Archivo no encontrado")
    
    # Obtener el tipo MIME
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    
    # Leer y servir el archivo
    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=content_type)
            return response
    except IOError:
        raise Http404("Error al leer el archivo")
