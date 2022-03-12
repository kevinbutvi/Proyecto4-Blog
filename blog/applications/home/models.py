from django.db import models
# Apps de terceros
from model_utils.models import TimeStampedModel


# Create your models here.

class Home(TimeStampedModel):
    """ Modelo de Pagina Prinicpal """
    title = models.CharField("Nombre", max_length=50)
    description = models.TextField()
    about_title = models.CharField("Titulo Nosotros", max_length=50)
    about_text = models.TextField()
    contact_mail = models.EmailField("Email de Contacto", blank = True, null = True, max_length=254)
    phone = models.CharField("Telefono de Contacto", max_length=50)
    
    class Meta:
        verbose_name = "Pagina Principal"
        verbose_name_plural = "Pagina Principal"
    
    def __str__(self):
        return (self.title)


class Suscribers(TimeStampedModel):
    """ Modelo de Suscriptores """
    email = models.EmailField(max_length=254)
    
    class Meta:
        verbose_name = "Suscriptor"
        verbose_name_plural = "Suscriptores"
    
    def __str__(self):
        return (self.email)


class Contact(TimeStampedModel):
    """ Modelo de Contacto """
    full_name = models.CharField("Nombres", max_length=50)
    email = models.EmailField(max_length=254)
    messagge = models.TextField(blank=True)
    
    class Meta():
        verbose_name = "Contacto"
        verbose_name_plural = "Mensajes"
    
    def __str__(self):
        return (self.full_name)