# Django-Middleware-0x03/chats/middleware.py

import logging
from datetime import datetime, timedelta
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from typing import Callable, Dict, List
from collections import defaultdict

# Configure logging to write to a file
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s'
)


class RequestLoggingMiddleware:
    """Middleware to log user requests with timestamp, user, and path information."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initialize middleware with get_response callable."""
        self.get_response = get_response
        self.logger = logging.getLogger('request_logger')
    
    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process each request and log details."""
        # Get the current timestamp for the log entry
        timestamp = datetime.now()

        # Get the user, default to 'Anonymous' if not authenticated
        user = request.user if request.user.is_authenticated else 'Anonymous'

        # Get the request path (e.g., /api/chats/messages/)
        path = request.path

        # Log the request details in the specified format
        self.logger.info(f"{timestamp} - User: {user} - Path: {path}")

        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    """Middleware to restrict access to messaging app during certain hours."""
    
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initialize middleware with get_response callable."""
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Check current time and deny access if outside allowed hours."""
        # Get current hour (0-23 format)
        current_hour = datetime.now().hour

            # Allow access only between 6 AM (6) and 9 PM (21)
            # Deny access between 9 PM and 6 AM (21-23 and 0-5)
        if current_hour >= 21 or current_hour < 6:
            if '/api/chats/' in request.path or '/chats/' in request.path:
                return HttpResponseForbidden(
                    "Access to messaging services is restricted between 9 PM and 6 AM. "
                    "Please try again during allowed hours (6 AM - 9 PM)."
                )

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    """Middleware to limit the number of chat messages per IP address within a time window."""
    
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initialize middleware with get_response callable."""
        self.get_response = get_response
        # Dictionary to store message timestamps for each IP address
        # Format: {ip_address: [timestamp1, timestamp2, ...]}
        self.ip_message_history: Dict[str, List[datetime]] = defaultdict(list)
        # Rate limit settings
        self.max_messages = 5  # Maximum messages allowed
        self.time_window_minutes = 1  # Time window in minutes
    
    def _get_client_ip(self, request: HttpRequest) -> str:
        """Get the client's IP address from the request."""
        # Check for IP in headers (for proxy/load balancer scenarios)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return (
            x_forwarded_for.split(',')[0].strip()
            if x_forwarded_for
            else request.META.get('REMOTE_ADDR', 'unknown')
        )
    
    def _clean_old_timestamps(self, timestamps: List[datetime]) -> List[datetime]:
        """Remove timestamps older than the time window."""
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(minutes=self.time_window_minutes)
        
        # Keep only timestamps within the time window
        return [ts for ts in timestamps if ts > cutoff_time]
    
    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Check message rate limit for POST requests to chat endpoints."""
        # Check if this is a POST request to messaging endpoints
        is_message_request = (
            request.method == 'POST' and 
            ('/api/chats/messages/' in request.path or '/chats/messages/' in request.path)
        )

        if is_message_request:
            # Get client IP address
            client_ip = self._get_client_ip(request)
            current_time = datetime.now()

            # Get message history for this IP and clean old timestamps
            self.ip_message_history[client_ip] = self._clean_old_timestamps(
                self.ip_message_history[client_ip]
            )

            # Check if user has exceeded the rate limit
            message_count = len(self.ip_message_history[client_ip])

            if message_count >= self.max_messages:
                return HttpResponseForbidden(
                    f"Rate limit exceeded. You can only send {self.max_messages} messages "
                    f"per {self.time_window_minutes} minute(s). Please wait before sending more messages."
                )

            # Add current timestamp to the history
            self.ip_message_history[client_ip].append(current_time)

        return self.get_response(request)


class RolepermissionMiddleware:
    """Middleware to check user roles before allowing access to specific admin/moderator actions."""
    
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initialize middleware with get_response callable."""
        self.get_response = get_response
        
        # Define protected endpoints that require admin/moderator access
        self.protected_endpoints = [
            '/admin/',                           # Django admin panel
            '/api/admin/',                       # Admin API endpoints
            '/api/chats/conversations/delete/',  # Delete conversations
            '/api/chats/messages/delete/',       # Delete messages
            '/api/users/ban/',                   # Ban users
            '/api/users/unban/',                 # Unban users
            '/api/reports/',                     # View reports
            '/api/settings/',                    # Modify app settings
        ]
        
        # Define allowed roles
        self.allowed_roles = ['admin', 'moderator']
    
    def _is_protected_endpoint(self, path: str) -> bool:
        """Check if the requested path is a protected endpoint."""
        return any(protected in path for protected in self.protected_endpoints)
    
    def _get_user_role(self, user) -> str:
        """Get the user's role. Assumes user has a 'role' attribute or is_staff/is_superuser."""
        if not user.is_authenticated:
            return 'anonymous'
        
        # Check if user is Django superuser (highest level admin)
        if hasattr(user, 'is_superuser') and user.is_superuser:
            return 'admin'
        
        # Check if user is Django staff (can access admin panel)
        if hasattr(user, 'is_staff') and user.is_staff:
            return 'admin'
        
        # Check if user has a custom role attribute
        if hasattr(user, 'role'):
            return user.role.lower()
        
        # Check if user has groups (Django groups system)
        if hasattr(user, 'groups'):
            user_groups = [group.name.lower() for group in user.groups.all()]
            if 'admin' in user_groups or 'administrator' in user_groups:
                return 'admin'
            elif 'moderator' in user_groups or 'mod' in user_groups:
                return 'moderator'
        
        # Default to regular user
        return 'user'
    
    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Check user role before allowing access to protected endpoints."""
        # Check if this is a request to a protected endpoint
        if self._is_protected_endpoint(request.path):
            # Get user role
            user_role = self._get_user_role(request.user)

            # Check if user has sufficient permissions
            if user_role not in self.allowed_roles:
                return HttpResponseForbidden(
                    f"Access denied. This action requires {' or '.join(self.allowed_roles)} privileges. "
                    f"Your current role: {user_role}"
                )

        return self.get_response(request)