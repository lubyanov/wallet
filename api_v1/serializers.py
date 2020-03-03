from rest_framework import serializers
from wallet.models import Customer, Account, Transaction, DECIMAL_PARAMS


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('uuid', 'currency', 'amount')


class CustomerAccountSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name', 'accounts')


class TransactionSerializer(serializers.ModelSerializer):
    customer_from = CustomerSerializer()
    customer_to = CustomerSerializer()
    account_from = AccountSerializer()
    account_to = AccountSerializer()

    class Meta:
        model = Transaction
        fields = (
            'action',
            'amount',
            'customer_from',
            'account_from',
            'customer_to',
            'account_to',
            'created_at'
        )


class TransferSerializer(serializers.Serializer):
    customer_from = serializers.IntegerField()
    customer_to = serializers.IntegerField(required=False)
    account_from = serializers.UUIDField()
    account_to = serializers.UUIDField()
    amount = serializers.DecimalField(**DECIMAL_PARAMS)
