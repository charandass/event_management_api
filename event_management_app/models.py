from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Event(models.Model):
    EVENT_TYPES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
    )

    name = models.CharField(max_length=255)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES)
    max_seats = models.PositiveIntegerField()
    booking_open_window_start = models.DateTimeField()
    booking_open_window_end = models.DateTimeField()

    def __str__(self):
        return self.name


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ticket {self.id} - {self.event.name} ({self.user.username})'

