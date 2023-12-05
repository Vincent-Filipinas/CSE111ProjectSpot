from django.urls import path
from .views import *

urlpatterns = [
    path('auth-url/', AuthenticationURL.as_view()),
    path('redirect/', callback),
    path('check-auth/', CheckAuthentication.as_view()),
    path('current-song/', CurrentSong.as_view()),
]
