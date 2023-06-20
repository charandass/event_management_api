from django.shortcuts import render
from rest_framework import generics, permissions
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from .helper import api_response, error_formator
import traceback
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from .models import Event, Ticket
from .serializers import EventSerializer, TicketSerializer
from django.utils import timezone
from django.db.models import Sum



class CreateEventAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = EventSerializer(data = data)
            if request.user.is_staff:
                if serializer.is_valid():
                    Event.objects.create(name=serializer.data['name'],event_type=serializer.data['event_type'],max_seats=serializer.data['max_seats'],booking_open_window_start=serializer.data['booking_open_window_start'],booking_open_window_end=serializer.data['booking_open_window_end'])
                        
                    return JsonResponse(api_response(0,[],"Event Created Successfully",[]))
                else:
                    err = error_formator(serializer.errors)
                    return JsonResponse(api_response(1,[],"Error",err))
            else:
                return JsonResponse(api_response(1,[],"You are not Admin",[]))
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return JsonResponse(api_response(1,[],"Error",str(e)))
            
class ListallEventsAPI(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [JWTAuthentication]
    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_staff:
                instance = Event.objects.all().values_list()
                list_result = [ entry for entry in instance ]
                return JsonResponse(api_response(0,list_result," all Event list",[]))
            else:
                return JsonResponse(api_response(1,[],"You are not Admin",[]))
                
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return JsonResponse(api_response(1,[],"Error",str(e)))
    
class UpdateEventAPI(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [JWTAuthentication]
    def post(self, request, event_id,*args, **kwargs):
        try:
            data = request.data
            serializer = EventSerializer(data = data)
            if request.user.is_staff:
                if serializer.is_valid():
                    instance = Event.objects.filter(id=event_id).update(name=serializer.data['name'],event_type=serializer.data['event_type'],max_seats=serializer.data['max_seats'],booking_open_window_start=serializer.data['booking_open_window_start'],booking_open_window_end=serializer.data['booking_open_window_end'])
                    if instance:
                        return JsonResponse(api_response(0,[],"Event updated",[]))
                    else:
                        return JsonResponse(api_response(1,[],"Event Not Found",[]))
                else:
                    err = error_formator(serializer.errors)
                    return JsonResponse(api_response(1,[],"Error",err))
            else:
                return JsonResponse(api_response(1,[],"You are not Admin",[]))
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return JsonResponse(api_response(1,[],"Error",str(e)))   

    
    

class eventSummaryAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_staff:
                today = timezone.now().date()
                events = Event.objects.filter(booking_open_window_end__gte=today)
                event_summary = []
                
                for event in events:
                    booked_seats = Ticket.objects.filter(event=event).count()
                    available_seats = event.max_seats - booked_seats
                    
                    event_data = {
                        'event_name': event.name,
                        'max_seats': event.max_seats,
                        'booked_seats': booked_seats,
                        'available_seats': available_seats,
                    }
                    event_summary.append(event_data)
                
                return JsonResponse(api_response(0, event_summary, "Event summary", []))
            
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return JsonResponse(api_response(1, [], "Error", str(e)))

    

# Users can
# - View events
# - Book ticket for an event
# - View Ticket
# - View all registered events sorted by event chronologically   

class viewEventsAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request, *args, **kwargs):
        try:
            today = timezone.now().date()
            instance = Event.objects.filter(booking_open_window_end__gte=today).order_by('booking_open_window_start').values_list()
            if instance:
                list_result = [ entry for entry in instance ]
                return JsonResponse(api_response(0,list_result," all Event list",[]))
            else:
                return JsonResponse(api_response(1,[],"No Events found on this day",[]))
            
                
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return JsonResponse(api_response(1,[],"Error",str(e)))
        
class BookTicketAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = TicketSerializer(data = data)
            user = request.user
            if Ticket.objects.filter(user_id=user.id).exists():
                return JsonResponse(api_response(1, [], "You have already booked a ticket", []))
            
            if serializer.is_valid():
                event = Event.objects.get(pk=serializer.data['event_Id'])
                
                current_time = timezone.now()
                if current_time < event.booking_open_window_start or current_time > event.booking_open_window_end:
                    return JsonResponse(api_response(1, [], "Booking window has closed", []))

                
                booked_seats = Ticket.objects.filter(event=event).count()
                if booked_seats >= event.max_seats:
                    return JsonResponse(api_response(1, [], "Maximum seats limit reached", []))

                
                res = Ticket.objects.create(event_id= serializer.data['event_Id'], user_id= user.id)
                if res:
                    return JsonResponse(api_response(0, [], "Ticket booked successfully", []))
            else:
                err = error_formator(serializer.errors)
                return JsonResponse(api_response(1, [], "Error", err))
        except Event.DoesNotExist:
            return JsonResponse(api_response(1, [], "Event does not exist", []))
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return JsonResponse(api_response(1, [], "Error", str(e)))


class viewicketAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, ticket_id,*args, **kwargs):
        try:
            instance =Ticket.objects.filter(id=ticket_id).values()
            print(instance)
            if instance:
                list_result = [entry for entry in instance]
                return JsonResponse(api_response(0, list_result, "Your ticket", []))
            
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return JsonResponse(api_response(1, [], "Error", str(e)))

            
                
        

    






