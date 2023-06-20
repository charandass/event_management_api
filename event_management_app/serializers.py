from rest_framework import serializers
from .models import Event, Ticket

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class TicketSerializer(serializers.Serializer):
    event_Id=serializers.IntegerField()