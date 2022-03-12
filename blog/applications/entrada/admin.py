from django.contrib import admin

from applications.entrada.models import Category, Entry, Tag

# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Entry)
