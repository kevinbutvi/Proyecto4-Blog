import datetime

# Modelos
from applications.entrada.models import Entry

from applications.home.forms import ContactForm, SuscribersForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
#
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .models import Home


class HomePageView(TemplateView):
    """ Vista de HOME, lista entradas home, portada y recientes """
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        # Cargamos el Home
        context["home"] = Home.objects.latest("created")
        # Contexto de noticia para portada
        context["portada"] = Entry.objects.entrada_en_portada()
        # Contecto para las 4 noticias complementarias
        context["entradas_home"] = Entry.objects.entradas_en_home()
        # Contexto para traer las ultimas 6 entradas mas recientes
        context["entradas_recientes"] = Entry.objects.entradas_recientes()
        # Enviamos formulario de suscripcion
        context["form"] = SuscribersForm
        
        return context



class SuscribersCreateView(CreateView):
    """ Vista que almacena mail de suscriptores y recarga la pagina. Comunica via mail que se suscribio correctamente """
    form_class = SuscribersForm
    
    def form_valid(self, form):
        # Enviar el codigo al email del usuario se usa 'send_email'
        asunto = "Registro exitoso"
        mensaje = "** Gracias por registrarse a nuestro newsletter "
        email_remitente = "developertest.kevin@gmail.com"
        #
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data["email"],])

        return(HttpResponseRedirect(reverse("home_app:index")))


class ContactCreateView(CreateView):
    """ Vista para consultas y contacto del footer  """
    form_class = ContactForm
    success_url = reverse_lazy("home_app:index")

