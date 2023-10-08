from django_filters import rest_framework as filters
from datetime import datetime


class DomainsFilter(filters.FilterSet):
    from_sec = filters.NumberFilter(method='filter_by_seconds_from_epoch')
    to_sec = filters.NumberFilter(method='filter_by_seconds_to_epoch')

    def filter_by_seconds_from_epoch(self, queryset, name, value):
        try:
            from_datetime = datetime.utcfromtimestamp(value)
            return queryset.filter(time_transition__gte=from_datetime)
        except (TypeError, ValueError):
            return queryset

    def filter_by_seconds_to_epoch(self, queryset, name, value):
        try:
            to_datetime = datetime.utcfromtimestamp(value)
            return queryset.filter(time_transition__lte=to_datetime)
        except (TypeError, ValueError):
            return queryset
