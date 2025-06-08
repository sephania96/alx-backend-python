from rest_framework import serializers
from .models import User
from .models import Conversation
from .models import Message
from .models import Chat

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
    def validate_message(self, obj):
        if ( message_body =! obj.conversation_id):
            raise serializers.ValidationError("Title is too short.")
        return value