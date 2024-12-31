from django.urls import path
from .views import DestinationView, DestinationById
urlpatterns = [
    path('destination', DestinationView.as_view()),
    path('destination/<uuid:account_id>', DestinationById.as_view())
]