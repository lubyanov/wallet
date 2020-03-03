from uuid import uuid4
from decimal import Decimal
from typing import Dict, Tuple

from django.db import transaction, Error
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR
)

from wallet.models import Account, Currency, Transaction, Action
from api_v1.validations import transfer_data_validate
from api_v1.utils import is_self_transfer, calculate_fee, get_success_response
from api_v1.serializers import CustomerAccountSerializer, TransferSerializer


INITIAL_ACCOUNT_DATA = (
    (Currency.USD, 100),
    (Currency.EUR, 0),
    (Currency.CNY, 0),
)


def transfer(data: TransferSerializer) -> Tuple[Dict, int]:
    """
    Transfers from one customers account to another

    Method is using for transfer between self customer'a accounts
    and also to transfer between one customer to another

    To provide consistency method uses database transaction mechanism

    Arguments:
        data: TransferSerializer - uses to get request data

    Returns:
        Tuple[Dict, int]: response json data with HTTP status
    """
    amount, fee = Decimal(data['amount']), Decimal(0)

    with transaction.atomic():

        account_from = Account.objects.select_for_update().select_related() \
            .get(uuid=data['account_from'])
        account_to = Account.objects.select_for_update().select_related() \
            .get(uuid=data['account_to'])

        errors = transfer_data_validate(account_from, account_to, data, amount)

        if not errors.get('errors'):

            if not is_self_transfer(data):
                fee = calculate_fee(amount)

            account_from.amount = account_from.amount - amount - fee
            account_from.save()
            account_to.amount = account_to.amount + amount
            account_to.save()

            Transaction(
                customer_from=account_from.customer,
                customer_to=account_to.customer,
                account_from=account_from,
                account_to=account_to,
                amount=amount,
                action=Action.TRANSFER
            ).save()

            result = get_success_response(account_from, account_to)

        else:
            return dict(errors), HTTP_400_BAD_REQUEST

    return result, HTTP_200_OK


def create_customer_with_wallet(
        serializer: CustomerAccountSerializer) -> Tuple[Dict, int]:
    """
    Creates customer account with wallet

    Method uses default serializer mechanism to store Customer instance
    and also create related wallet with balance and history transaction

    To provide consistency method uses database transaction mechanism

    Arguments:
        serializer: CustomerSerializer - uses to pass data to View

    Returns:
        Tuple[Dict, int]: response json data with HTTP status
    """
    try:
        with transaction.atomic():
            customer = serializer.save()
            for currency, amount in INITIAL_ACCOUNT_DATA:
                account = Account(
                    uuid=uuid4(),
                    customer=customer,
                    currency=currency,
                    amount=amount
                )
                account.save()
                Transaction(
                    customer_from=customer,
                    customer_to=customer,
                    account_from=account,
                    account_to=account,
                    amount=amount,
                    action=Action.INITIAL
                ).save()
    except Error as err:
        errors = {'errors': [{'database': str(err)}]}
        return errors, HTTP_500_INTERNAL_SERVER_ERROR

    return serializer.data, HTTP_201_CREATED
