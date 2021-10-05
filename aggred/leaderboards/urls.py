from django.urls import path
from . import views


urlpatterns = [
    path('leaderboards/region=<region>', views.leaderboards, name='leaderboards'),
]