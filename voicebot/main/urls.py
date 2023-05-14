from django.urls import path
from .views import chatbot , chat

urlpatterns = [
    path('api/chatbot/', chatbot, name='chatbot'),
    path('', chat, name='chat'),
]