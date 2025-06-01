#chats serializer
from rest_framework import serializers
from .models import User, Conversation, Message

# Serialize User data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Serialize Message model
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Display sender info

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']

# Serialize Conversation and include nested messages
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at']