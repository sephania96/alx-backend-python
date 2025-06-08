from django.contrib.auth.models import AbstractUser 
import uuid
from django.db import models

# Create your models here.

class User(models.AbstractUser):
    first_name=models.CharField(max_length=15, blank=True, null=True)
    last_name=models.CharField(max_length=15, blank=True, null=True)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField()
    

class Conversation(models.Model):
    participants=models.CharField(max_length=15, blank=True, null=True)
    conversattion = models.CharField(max_length=100)
    conversation_id = models.CharField(editable=False, unique=True)


class Message(models.Model):
    message_body = models.CharField()
    sent_at = models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    message_id = models.CharField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return self.name
