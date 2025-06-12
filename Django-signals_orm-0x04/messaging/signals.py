#signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

#Automatically create a notification when message is sent
@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver,
                                    message=instance)