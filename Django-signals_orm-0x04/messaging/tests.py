from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class NotificationSignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass')
        self.receiver = User.objects.create_user(username='receiver', password='pass')

    def test_notification_created_on_message_send(self):
        # Create a message instance
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello!')

        # Check that a notification was created
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)

def test_message_edit_creates_history(self):
        # Create initial message
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Initial')
        # Edit message
        message.content = 'Updated'
        message.save()

        # Check MessageHistory was created
        self.assertEqual(MessageHistory.objects.count(), 1)
        history = MessageHistory.objects.first()
        self.assertEqual(history.old_content, 'Initial')
        self.assertTrue(message.edited)

def test_user_delete_removes_related_data(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Bye')
        Notification.objects.create(user=self.receiver, message=message)

        self.sender.delete()

        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)
        self.assertEqual(MessageHistory.objects.count(), 0)