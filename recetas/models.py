from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User

class Receta(models.Model):
    user= models.ForeignKey(User, models.DO_NOTHING, default=1)
    categoria= models.ForeignKey('categorias.Categoria', models.DO_NOTHING, related_name='recetas', blank=True, null=True)
    nombre = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='nombre', unique=True, editable=False)
    tiempo = models.CharField(max_length=50, blank=True, null=True)
    foto = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'recetas'
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'