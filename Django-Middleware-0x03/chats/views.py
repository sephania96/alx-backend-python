#!/usr/bin/env python3
"""Views for conversations and messages API."""

from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from typing import Type
from rest_framework import filters  # You'll need this
from django_filters.rest_framework import DjangoFilterBackend  # And this



class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for handling conversations."""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """Filter conversations to only show those where user is a participant."""
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        """Create conversation and add creator as participant."""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to return 403 if user is not a participant."""
        try:
            instance = self.get_object()
            if not instance.participants.filter(id=request.user.id).exists():
                return Response(
                    {"detail": "You are not a participant of this conversation."},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception:
            return Response(
                {"detail": "Access denied."},
                status=status.HTTP_403_FORBIDDEN
            )


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for handling messages."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    filter_backends = [DjangoFilterBackend]  # Add other backends if needed
    ordering = ['-timestamp']

    def get_queryset(self):
        """Filter messages based on conversation_id parameter and user participation."""
        queryset = Message.objects.all()

        # Check if conversation_id is provided in query params
        conversation_id = self.request.query_params.get('conversation_id', None)
        if conversation_id is not None:
            # Filter messages by conversation_id
            queryset = Message.objects.filter(conversation_id=conversation_id)

            # Verify user is participant of the conversation
            try:
                conversation = get_object_or_404(Conversation, id=conversation_id)
                if not conversation.participants.filter(id=self.request.user.id).exists():
                    # Return empty queryset if user is not a participant
                    return Message.objects.none()
            except Exception:
                return Message.objects.none()
        else:
            # Filter to only messages in conversations where user is a participant
            queryset = Message.objects.filter(conversation__participants=self.request.user)

        return queryset

    def perform_create(self, serializer):
        """Create message with current user as sender."""
        if conversation_id := self.request.data.get('conversation_id'):
            try:
                conversation = get_object_or_404(Conversation, id=conversation_id)
                if not conversation.participants.filter(id=self.request.user.id).exists():
                    return Response(
                        {"detail": "You are not a participant of this conversation."},
                        status=status.HTTP_403_FORBIDDEN
                    )
                serializer.save(sender=self.request.user, conversation=conversation)
            except Exception:
                return Response(
                    {"detail": "Invalid conversation."},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            serializer.save(sender=self.request.user)

    def list(self, request, *args, **kwargs):
        """Override list to handle conversation_id filtering and return 403 for unauthorized access."""
        if conversation_id := request.query_params.get('conversation_id', None):
            try:
                return self._extracted_from_list_5(conversation_id, request)
            except Exception:
                return Response(
                    {"detail": "Access denied."},
                    status=status.HTTP_403_FORBIDDEN
                )

        # Default behavior for listing all messages user has access to
        return super().list(request, *args, **kwargs)

    # TODO Rename this here and in `list`
    def _extracted_from_list_5(self, conversation_id, request):
        conversation = get_object_or_404(Conversation, id=conversation_id)
        if not conversation.participants.filter(id=request.user.id).exists():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Filter messages for this specific conversation
        queryset = Message.objects.filter(conversation_id=conversation_id).order_by('-timestamp')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to return 403 if user cannot access the message."""
        try:
            instance = self.get_object()
            if not instance.conversation.participants.filter(id=request.user.id).exists():
                return Response(
                    {"detail": "You are not a participant of this conversation."},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception:
            return Response(
                {"detail": "Access denied."},
                status=status.HTTP_403_FORBIDDEN
            )

    def update(self, request, *args, **kwargs):
        """Override update to return 403 if user cannot access the message."""
        try:
            instance = self.get_object()
            if not instance.conversation.participants.filter(id=request.user.id).exists():
                return Response(
                    {"detail": "You are not a participant of this conversation."},
                    status=status.HTTP_403_FORBIDDEN
                )
            return super().update(request, *args, **kwargs)
        except Exception:
            return Response(
                {"detail": "Access denied."},
                status=status.HTTP_403_FORBIDDEN
            )

    def destroy(self, request, *args, **kwargs):
        """Override destroy to return 403 if user cannot access the message."""
        try:
            instance = self.get_object()
            if not instance.conversation.participants.filter(id=request.user.id).exists():
                return Response(
                    {"detail": "You are not a participant of this conversation."},
                    status=status.HTTP_403_FORBIDDEN
                )
            return super().destroy(request, *args, **kwargs)
        except Exception:
            return Response(
                {"detail": "Access denied."},
                status=status.HTTP_403_FORBIDDEN
            )