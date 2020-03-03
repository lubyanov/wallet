from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from api_v1.filters import TransactionFilters
from api_v1.services import create_customer_with_wallet, transfer
from wallet.models import Customer, Transaction
from api_v1.serializers import (
    CustomerAccountSerializer,
    TransactionSerializer,
    TransferSerializer
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().prefetch_related('accounts')
    serializer_class = CustomerAccountSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response_data, response_status = create_customer_with_wallet(
            serializer
        )

        return Response(
            response_data,
            status=response_status,
        )


class Transfer(APIView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response_data, response_status = transfer(serializer.data)

        return Response(
            response_data,
            status=response_status
        )


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().select_related().order_by('-created_at')
    serializer_class = TransactionSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('action', 'created_at')
    filterset_class = TransactionFilters
