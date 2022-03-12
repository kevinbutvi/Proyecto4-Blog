#
from django.urls import path
from . import views

app_name = "entrada_app"

# entrada_app:entry-lista


urlpatterns = [
    path(
        'entradas/', 
        views.EntryListView.as_view(),
        name='entry-lista',
    ),
    # SLUG enviado automaticamente por el DetailView de la vista.
    path(
        'entrada/<slug>/', 
        views.EntradaDetailView.as_view(),
        name='entry-detalle',
    ),
]

