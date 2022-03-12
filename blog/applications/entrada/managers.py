from msilib.schema import PublishComponent
from unicodedata import category
from django.db import models

class EntryManager(models.Manager):
    """ Managaer para Entrada """
    
    def entrada_en_portada(self):
        """ Carga el primer (el mas actual) articulo que sea portada y este publicado

        Returns:
            object: Devuelve la primer entrada en orden cronologico que sea 'portada'
        """
        return self.filter(
            public=True,
            portada=True
        ).order_by("-created").first()
    
    def entradas_en_home(self):
        """ Carga las 4 entradas complementarias para completar el home

        Returns:
            object: Devuelve las primeras 4 entradas mas recientes que son articulos de 'home'
        """
        return self.filter(
            public=True,
            in_home=True
        ).order_by("-created")[:4]
    
    def entradas_recientes(self):
        """ Carga las ultimas 6 entradas mas recientes

        Returns:
            object: Devuelve las ultimas 6 entradas en orden cronologico, pueden ser portadas y/o home
        """
        return self.filter(
            public=True,
        ).order_by("-created")[:6]
    
    def buscar_entrada(self, kword, categoria):
        """Manager para buscar entradas segun kword enviados por el usuario y/o categorias. Los devuelve ordenados

        Args:
            kword (char): palabra clave enviada por buscador de html
            categoria (char): categoria, enviada por selector

        Returns:
            object: Devuelve todas las categorias que coinciden con los criterios de busqueda
        """
        if len(categoria) > 0:
            return self.filter(
                category__short_name = categoria,
                title__icontains = kword,
                public = True
            ).order_by("-created")
        
        else:
            return self.filter(
                title__icontains = kword,
                public = True
            ).order_by("-created")