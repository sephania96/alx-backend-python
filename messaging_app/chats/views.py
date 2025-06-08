# #!/usr/bin/env python3

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
    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)


# """Views for conversations and messages API."""

# from rest_framework import viewsets, status, filters
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .models import Conversation, Message
# from .serializers import ConversationSerializer, MessageSerializer
# from rest_framework.status import HTTP_403_FORBIDDEN

# class ConversationViewSet(viewsets.ModelViewSet):
#     """ViewSet for handling conversations."""
#     queryset = Conversation.objects.all()
#     serializer_class = ConversationSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return self.queryset.filter(participants=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save()

# class MessageViewSet(viewsets.ModelViewSet):
#     """ViewSet for handling messages."""
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.OrderingFilter]
#     ordering = ['-timestamp']

#     def get_queryset(self):
#         return self.queryset.filter(conversation__participants=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(sender=self.request.user)

