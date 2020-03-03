from django_filters.rest_framework import (
    FilterSet,
    UUIDFilter,
    CharFilter
)


class TransactionFilters(FilterSet):
    action = CharFilter(field_name='action')
    account_to_uuid = UUIDFilter(field_name='account_to_uuid')
    account_from_uuid = UUIDFilter(field_name='account_from_uuid')
