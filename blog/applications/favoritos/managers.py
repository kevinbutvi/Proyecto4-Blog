from django.db import models

class FavoritesManager(models.Manager):
    
    def entradas_user(self, usuario):
        """ Manager que trae todas las entradas favoritas publicadas de cierto usuario """
        return (self.filter(
            entry__public = True,
            user = usuario
            ).order_by("-created")
                )