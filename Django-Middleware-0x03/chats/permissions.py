from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View
from typing import Optional
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    Allows all CRUD operations (GET, POST, PUT, PATCH, DELETE) for participants.
    """
    def has_permission(self, request: Request, view: View) -> bool:
        """
        Check if user is authenticated for all requests.
        """
        return request.user.is_authenticated
    
    def has_object_permission(self, request: Request, view: View, obj) -> bool:
        """
        Check if user is a participant of the conversation.
        Handles both Conversation and Message objects.
        Allows all HTTP methods (GET, POST, PUT, PATCH, DELETE) for participants.
        """
        if not request.user.is_authenticated:
            return False
        
        # Handle Conversation objects
        if isinstance(obj, Conversation):
            return obj.participants.filter(id=request.user.id).exists()
        
        # Handle Message objects - check if user is participant of the conversation
        elif isinstance(obj, Message):
            return obj.conversation.participants.filter(id=request.user.id).exists()
        
        return False