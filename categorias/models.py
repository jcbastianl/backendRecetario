from django.db import models

from autoslug import AutoSlugField

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    slug = AutoSlugField(populate_from='nombre', unique=True, null=False, blank=False)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table= 'categorias'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'