# let's do the pagination for the chats
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class ChatPagination(PageNumberPagination):
    """
    Custom pagination class for chat messages.
    """
    page_size = 20  # Default number of messages per page
    page_size_query_param = 'page_size'  # Allow clients to set the page size
    max_page_size = 100  # Maximum allowed page size
    page_query_param = 'page'  # Query parameter for the page number

    def get_paginated_response(self, data):
        """
        Override to include additional metadata in the paginated response.
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })