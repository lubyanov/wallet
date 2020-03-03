from django_filters.rest_framework import (
    FilterSet,
    UUIDFilter,
    CharFilter
)


class TransactionFilters(FilterSet):
    action = CharFilter(field_name='action')
    account_to = UUIDFilter(field_name='account_to__uuid')
    account_from = UUIDFilter(field_name='account_from__uuid')
