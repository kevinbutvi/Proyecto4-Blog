from django.db import models
#
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):
    """ Manager para creacion de usuarios tipo admin y comun """

    def _create_user(self, email, full_name, password, is_staff, is_superuser, is_active, **extra_fields):
        """ Plantilla para la creacion de usuario """
        user = self.model(
            email=email,
            full_name=full_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, email, full_name,  password=None, **extra_fields):
        """ Creacion de usuario normal """
        return self._create_user(email, full_name, password, False, False, False, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """ Creacion de usuario ADMIN """
        return self._create_user(email, password, True, True, True, **extra_fields)

    def cod_validation(self, id_usuario, codigo_registro):
        """ Verificacion de codigo de Seguridad"""
        if self.filter(id = id_usuario, codregistro = codigo_registro):
            return (True)
        else:
            return (False)