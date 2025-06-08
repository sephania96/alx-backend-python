from rest_framework import permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()


lass IsParticipantOfConversation(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

       
        if request.method in SAFE_METHODS:
            return user in obj.conversation.participants.all()

        
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return obj.sender == user

     
        if request.method == "POST":
            return user in obj.conversation.participants.all()

        return False
class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipant]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
