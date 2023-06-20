from django.urls import path, include

urlpatterns = [
    path('account/', include('account.urls')),
    path('event/', include('event_management_app.urls')),
]