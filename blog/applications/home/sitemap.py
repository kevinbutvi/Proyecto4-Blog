from datetime import datetime
from typing import Protocol
from django.contrib.sitemaps import Sitemap
from datetime import datetime
from django.urls import reverse_lazy
#
from applications.entrada.models import Entry


class EntrySitemap(Sitemap):
    """ Posicionamiento Sitemap de pagina web """
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"
    
    def items(self):
        """ Declaracion de items y Modelo sobre los cuales se va a generar URLs """
        return (Entry.objects.filter(public=True))
    
    def lastmod(self, obj):
        """ Definicion para el orden de las URLs"""
        return (obj.created)

class Sitemap(Sitemap):
    protocol = "https"
    
    def __init__(self, names):
        self.names = names
    
    def items(self):
        return (self.names)
    
    def changefreq(self, obj):
        return ("weekly")
    
    def lastmod(self, obj):
        return (datetime.now())
    
    def location(self, obj):
        return (reverse_lazy(obj))