from django.urls import path
from .views import *

app_name = "friend"

""" /friends/ + ... """
urlpatterns = [
    path('<nick>/', friends, name="friends"),
    path('request/send_to/<nick>/', send_friend_request, name="send_request"),
    path('requests/<nick>/', friend_requests, name="requests"),
    path('request/accept/<friend_request_id>', accept_friend, name='accept_request'),
    path('request/decline/<nick>', decline_friend, name='decline_request'),
    path('request/cancel/', cancel_request, name='cancel_request'),
    path('remove/<nick>', remove_friend, name='remove_friend'),
]