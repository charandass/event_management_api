from django.contrib import admin
from .models import Ticket, Event
# Register your models here.
admin.site.register(Event)
admin.site.register(Ticket)
