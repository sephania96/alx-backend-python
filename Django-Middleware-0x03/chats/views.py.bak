from django.shortcuts import render
from rest_framework import viewsets , status, filters
from .models import User
from .models import Conversation
from .models import Message
from .serializers import ChatSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_403_FORBIDDEN
# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filterset_fields = ['message_body']
    search_fields = ['message_body']
    ordering_fields = ['created_at']

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filterset_fields = ['conversattion', 'participants']
    search_fields = ['content']
    ordering_fields = ['conversation_id']
