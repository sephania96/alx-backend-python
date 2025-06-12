# messaging/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Prefetch
from messaging.managers import UnreadMessagesManager

# Message model to store user-to-user messages
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_messages')
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')  # Support threaded replies
    read = models.BooleanField(default=False)

    #custom manager for unread
    unread = UnreadMessagesManager

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"
    
    def get_thread(self):
        """
        Recursively get all replies to this message.
        """
        thread = []

        def fetch_replies(message):
            for reply in message.replies.all():
                thread.append(reply)
                fetch_replies(reply)

        fetch_replies(self)
        return thread

    @classmethod
    def get_optimized_queryset(cls):
        """
        Optimized queryset using select_related for user and prefetch_related for threaded replies.
        """
        return cls.objects.select_related('sender', 'receiver', 'edited_by').prefetch_related(
            Prefetch('replies', queryset=cls.objects.select_related('sender', 'receiver'))
        )

# Model to store history of edited messages
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of message {self.message.id} at {self.edited_at}"
    
# Notification model linked to user and message
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - Message ID: {self.message.id}"