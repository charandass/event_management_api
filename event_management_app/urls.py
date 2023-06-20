from django.urls import path
from .views import CreateEventAPI,ListallEventsAPI,UpdateEventAPI, viewEventsAPI,BookTicketAPI, viewicketAPI, eventSummaryAPI
urlpatterns = [
    path('createEvent/', CreateEventAPI.as_view(),name="createEvent"),
    path('listAllEvent/', ListallEventsAPI.as_view(),name="listAllEvent"),
    path('updateEvent/<int:event_id>', UpdateEventAPI.as_view(),name="updateEvent"),
    path('viewEvents/', viewEventsAPI.as_view(),name="viewEvents"),
    path('bookTicket/', BookTicketAPI.as_view(),name="bookTicket"),
    path('viewTicket/<int:ticket_id>', viewicketAPI.as_view(),name="viewTicket"),
    path('eventSummary/', eventSummaryAPI.as_view(),name="eventSummary"),
    
    
]