from django_filters import rest_framework as filters
from .models import Message
from typing import Type
from django.contrib.auth.models import User

class MessageFilter(filters.FilterSet):
    User = filters.ModelChoiceFilter(
        field_name='sender',
        queryset=User.objects.all(),
        label='Sender',
    )
    start_date = filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Start Date',
    )
    end_date = filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='End Date',
    )

    class Meta:
        model = Message
        fields = ['user', 'start_date', 'end_date']