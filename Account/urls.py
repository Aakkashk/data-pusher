from django.urls import path
from .views import AccountViews

urlpatterns = [
    path('accounts', AccountViews.as_view()),
    path('accounts/<str:email>', AccountViews.as_view())
]