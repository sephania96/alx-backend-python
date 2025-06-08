import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
# Set up a logger
logger = logging.getLogger("request_logger")
handler = logging.FileHandler("user_requests.log")
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_entry)
        response = self.get_response(request)
        return response
        
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        start_time = time(18, 0)  # 6:00 PM
        end_time = time(21, 0)    # 9:00 PM

        if not (start_time <= now <= end_time):
            return HttpResponseForbidden("Access to the messaging app is restricted outside 6 PM to 9 PM.")

        return self.get_response(request)
        
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store structure: {ip: [timestamp1, timestamp2, ...]}
        self.ip_message_log = defaultdict(list)
        self.time_window = 60  # seconds
        self.message_limit = 5

    def __call__(self, request):
        if request.method == 'POST' and '/messages/' in request.path:
            ip = self.get_client_ip(request)
            current_time = time.time()

            # Clean up old timestamps
            recent_times = [
                t for t in self.ip_message_log[ip] if current_time - t < self.time_window
            ]
            self.ip_message_log[ip] = recent_times

            if len(recent_times) >= self.message_limit:
                return HttpResponseForbidden("Rate limit exceeded: Max 5 messages per minute allowed.")

            self.ip_message_log[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        # Handles proxies and direct connections
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
        
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Restrict only for modifying requests
        if request.method in ['POST', 'PATCH', 'DELETE']:
            user = request.user

            if not user.is_authenticated:
                return HttpResponseForbidden("Access denied: Authentication required.")

            # Check for role: superuser or staff (admin/moderator)
            if not (user.is_superuser or user.is_staff):
                return HttpResponseForbidden("Access denied: You do not have the required role.")

        return self.get_response(request)