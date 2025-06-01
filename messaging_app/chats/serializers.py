#!/usr/bin/env python3
"""Serializers for chats app."""

from rest_framework import serializers
from .models import User, Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    message_id = serializers.CharField(max_length=255)
    summary = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = '__all__'
class ConversationSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField(max_length=255)
    summary = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = '__all__'        
    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value