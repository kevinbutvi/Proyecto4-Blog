from django.contrib import admin

from applications.home.models import Contact, Home, Suscribers

# Register your models here.


admin.site.register(Home)
admin.site.register(Suscribers)
admin.site.register(Contact)