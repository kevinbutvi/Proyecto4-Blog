import http
from sre_constants import SUCCESS

#
from applications.entrada.models import Entry
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, ListView, View

#
from .models import Favorites

# Create your views here.



class UserPageView(LoginRequiredMixin, ListView):
    """ Vista de perfil para usuarios logueados """
    template_name = "favoritos/perfil.html"
    context_object_name = "entradas_user"
    login_url = reverse_lazy("users_app:user-login") # Redireccion para usuarios NO logueados
    
    def get_queryset(self):
        """ 'self.request.user' trae el usuario que esta activo en dicha session """
        return Favorites.objects.entradas_user(self.request.user)


class AddFavoritoView(LoginRequiredMixin, View):
    """ Vista para agregar una entrada a favoritos """
    login_url = reverse_lazy("users_app:user-login")
    
    def post(self, request, *arg, **kwargs):
        # Recuperar usuario
        usuario = self.request.user
        entrada = Entry.objects.get(id=self.kwargs["pk"])
        # Registramos FAvorito
        Favorites.objects.create(
            user = usuario,
            entry = entrada,
            )
        
        return (HttpResponseRedirect(
            reverse(
                "favoritos_app:perfil",
            )
        ))



class FavoritoDeleteView(DeleteView):
    """ Vista para eliminar favoritos del perfil de usuario segun template por 'PK' """
    model = Favorites
    success_url = reverse_lazy('favoritos_app:perfil')
