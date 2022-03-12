import imp

from applications.home.sitemap import EntrySitemap, Sitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# SEO
from django.contrib.sitemaps.views import sitemap

from django.urls import include, path

urlpatterns_main = [
    path('admin/', admin.site.urls),
    path('', include('applications.users.urls')),
    path('', include('applications.home.urls')),
    path('', include('applications.entrada.urls')),
    path('', include('applications.favoritos.urls')),
    # URLS PARA 'CKEDITOR'
    path(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # esta ultima linea configura para que funcionen los multimedia dentro de las plantillas


# Objeto Sitemap que general XML
sitemaps = {
    "sitemap": Sitemap(["home_app:index"]),
    "entradas": EntrySitemap
}


urlpatterns_sitemap = [
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemap.views.sitemap")
]


urlpatterns = urlpatterns_main + urlpatterns_sitemap
