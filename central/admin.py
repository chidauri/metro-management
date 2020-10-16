from django.contrib import admin

from .models import Station, Train, Ticket, Coach

# Register your models here.
admin.site.register(Station)
admin.site.register(Train)
admin.site.register(Ticket)
admin.site.register(Coach)