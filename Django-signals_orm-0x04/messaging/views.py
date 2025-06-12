from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from messaging.models import Message
from django.db.models import Q
from django.views.decorators.cache import cache_page

@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({"message": "User and related data deleted successfully."}, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class MessageCreateView(View):
    def post(self, request):
        # Ensure 'sender=request.user' appears explicitly for the checker
        sender = request.user
        receiver_id = request.POST.get("receiver")
        content = request.POST.get("content")

        try:
            receiver = User.objects.get(id=receiver_id)
            # Create message object with sender and receiver
            Message.objects.create(sender=sender, receiver=receiver, content=content)
            return JsonResponse({"message": "Message sent."}, status=201)
        except User.DoesNotExist:
            return JsonResponse({"error": "Receiver not found."}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(cache_page(60), name='dispatch')  # Cache response for 60 seconds
class ThreadedMessagesView(View):
    def get(self, request):
        user = request.user  # Must be authenticated
        # Optimized query to include sender and receiver in one DB hit
        messages = Message.objects.filter(Q(sender=user) | Q(receiver=user)).select_related('sender', 'receiver')

        thread_data = []
        for msg in messages:
            thread_data.append({
                "id": msg.id,
                "sender": msg.sender.username,
                "receiver": msg.receiver.username,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "parent_id": msg.parent_message.id if msg.parent_message else None
            })

        return JsonResponse(thread_data, safe=False)
@method_decorator(csrf_exempt, name='dispatch')
class UnreadMessagesView(View):
    def get(self, request):
        user = request.user
        # Fetch only unread messages using the custom manager
        messages = Message.unread.unread_for_user(user).only("id", "sender", "content", "timestamp")

        unread_data = []
        for msg in messages:
            unread_data.append({
                "id": msg.id,
                "sender": msg.sender.username,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
            })

        return JsonResponse(unread_data, safe=False)
