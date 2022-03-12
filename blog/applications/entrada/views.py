import imp

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView

from .models import Category, Entry


class EntryListView(LoginRequiredMixin, ListView):
    """ Vista para listar entradas y aplica filtros """
    
    template_name = "entrada/lista.html"
    context_object_name = "entradas"
    paginate_by = 6
    login_url = reverse_lazy("users_app:user-login")

    
    
    def get_context_data(self, **kwargs):
        """ Contexto para enviar al html y mostrar las categorias vigentes """
        
        context = super(EntryListView, self).get_context_data(**kwargs)
        context["categorias"] = Category.objects.all()
        return context
    
    def get_queryset(self):
        """ Vista que realiza las busquedas y filtros desde 'buscar' o el 'selector de categorias' """
        kword = self.request.GET.get("kword", "")
        categoria = self.request.GET.get("categoria","")
        # Consulta de busqueda
        resultado = Entry.objects.buscar_entrada(kword, categoria)
        return resultado



class EntradaDetailView(LoginRequiredMixin, DetailView):
    """ Vista para mostrar detalle de una entrada en particular """
    model = Entry
    template_name = "entrada/detail.html"
    login_url = reverse_lazy("users_app:user-login")

