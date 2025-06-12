from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({"message": "User and related data deleted successfully."}, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)