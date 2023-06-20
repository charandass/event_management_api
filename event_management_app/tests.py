from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Event, Ticket
from .serializers import EventSerializer, TicketSerializer
from datetime import date, timedelta
from django.conf import settings


class APITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword')
        
        refresh_admin = RefreshToken.for_user(self.admin_user)  
        self.access_token_admin = str(refresh_admin.access_token)  

        refresh_user = RefreshToken.for_user(self.user)  
        self.access_token_user = str(refresh_user.access_token)  

        self.event_data = {
            'name': 'Test Event',
            'event_type': 'offline',
            'max_seats': 100,
            'booking_open_window_start': date.today(),
            'booking_open_window_end': date.today() + timedelta(days=7),
        }
        self.ticket_data = {
            'event_Id': 1,
        }
        
        self.event = Event.objects.create(**self.event_data)

    def test_create_event_api(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_admin)
        url = reverse('createEvent')
        response = self.client.post(url, data=self.event_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.count(), 2)  # Make sure event is created

    def test_list_all_events_api(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_admin)
        url = reverse('listAllEvent')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data['data']), 1)  # Make sure only 1 event is listed

    def test_update_event_api(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_admin)
        url = reverse('updateEvent', kwargs={'event_id': self.event.id})
        updated_event_data = {
            'name': 'Updated Event',
            'event_type': 'online',
            'max_seats': 200,
            'booking_open_window_start': date.today() + timedelta(days=1),
            'booking_open_window_end': date.today() + timedelta(days=8),
        }
        response = self.client.post(url, data=updated_event_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, updated_event_data['name'])
        self.assertEqual(self.event.event_type, updated_event_data['event_type'])
        self.assertEqual(self.event.max_seats, updated_event_data['max_seats'])

    def test_event_summary_api(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_admin)
        url = reverse('eventSummary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data['data']), 1)  

    def test_view_events_api(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user)
        url = reverse('viewEvents')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data['data']), 1) 

    def test_book_ticket_api(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user)
        url = reverse('bookTicket')
        response = self.client.post(url, data=self.ticket_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Ticket.objects.count(), 1)  # Make sure ticket is booked

    def test_view_ticket_api(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user)
        ticket = Ticket.objects.create(event=self.event, user=self.user)
        url = reverse('viewTicket', kwargs={'ticket_id': ticket.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['data'][0]['id'], ticket.id)
