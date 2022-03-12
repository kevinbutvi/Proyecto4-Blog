#
from django.urls import path
from . import views

app_name = "favoritos_app"

# favoritos_app:perfil
# favoritos_app:delete-favoritos


urlpatterns = [
    path(
        'perfil/', 
        views.UserPageView.as_view(),
        name='perfil',
    ),
    path(
        'add-entrada/<pk>/', 
        views.AddFavoritoView.as_view(),
        name='add-favoritos',
    ),
    path(
        'delete-favorites/<pk>/', 
        views.FavoritoDeleteView.as_view(),
        name='delete-favoritos',
    ),
]

