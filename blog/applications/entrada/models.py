from datetime import timedelta, datetime
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy

# Apps de Terceros
from model_utils.models import TimeStampedModel
from ckeditor_uploader.fields import RichTextUploadingField

# Managers
from .managers import EntryManager

# Create your models here.


class Category(TimeStampedModel):
    """ Modelo de Categorias de una Entrada """
    
    short_name = models.CharField("Nombre Corto", max_length=50, unique= True)
    name = models.CharField("Nombre", max_length=50)
    
    
    class Meta():
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
    
    def __str__(self):
        return (self.name)


class Tag(TimeStampedModel):
    """ Modelo Tags de Entradas """
    name = models.CharField("Nombre", max_length=50)
    
    class Meta():
        verbose_name = "Etiqueta"
        verbose_name_plural = "Tags"
    
    def __str__(self):
        return (self.name)


class Entry(TimeStampedModel):
    """ Modelo para Entradas o Articulos """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    tag = models.ManyToManyField(Tag)
    title = models.CharField("Titulo", max_length=50)
    resume = models.TextField("Resumen")
    content = RichTextUploadingField("Contenido")
    public = models.BooleanField(default = False)
    image = models.ImageField(
        "Imagen",
        upload_to="Entry",
        )
    portada = models.BooleanField(default=False)
    in_home = models.BooleanField(default=False)
    slug = models.SlugField(editable=False, max_length=300)
    
    objects = EntryManager()
    
    
    class Meta():
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"


    def __str__(self):
        return (self.title)
    
    def get_absolute_url(self):
        """ Se sobreescribe la funcion para poder utilizar el Sitemap """
        return reverse_lazy(
            "entrada_app:entry-detalle",
            kwargs = {'slug': self.slug})
    
    def save(self, *args, **kwargs):
        """ Sobreescribir Save para crear Slug Unicos generados con la hora actual """
        # Calculamos el total de segundos de la hora actual
        now = datetime.now()
        total_time = timedelta(
            hours = now.hour,
            minutes = now.minute,
            seconds = now.second
        )
        seconds = int(total_time.total_seconds())
        slug_unique = f"{self.title}{str(seconds)}"
        self.slug = slugify(slug_unique)
        
        super(Entry, self).save(*args, **kwargs)