#!/usr/bin/env python3
"""Main URL routing for the messaging_app project."""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from chats.auth import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),
    path('api-auth/', include('rest_framework.urls')),  # For login/logout in browsable API
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/chats/', include('chats.urls')),  # Include chat app URLs
]
