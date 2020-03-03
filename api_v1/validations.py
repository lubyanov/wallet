from decimal import Decimal
from typing import Mapping

from wallet.models import Account
from api_v1.serializers import TransferSerializer
from api_v1.utils import (
    is_self_transfer,
    is_enough_amount,
    is_different_customers,
    is_account_belongs_to_customer,
    calculate_fee
)


SAME_CUSTOMERS = "customers can't be with same id = %s"
NOT_ENOUGH_AMOUNT = "not enough amount to transfer - %s vs %s"
NOT_ENOUGH_AMOUNT_FEE = "not enough amount to transfer with fee - %s + %s vs %s"
ACCOUNT_DOESNT_BELONG = "account '%s' doesn't belong to customer with id = %s"


def transfer_data_validate(account_from: Account,
                           account_to: Account,
                           data: TransferSerializer,
                           amount: Decimal) -> Mapping[str, list]:
    """
    Validates incoming transfer request

    Must assure that accounts belongs to their customers and
    accounts have enough amount to transfer with fee or not

    Returns:
        Mapping[str, str] - dict with errors if they are exist
    """

    errors = {'errors': []}

    if not is_account_belongs_to_customer(account_from.customer.id,
                                          data['customer_from']):
        errors.get('errors').append(
            ACCOUNT_DOESNT_BELONG %
            (account_from.uuid, data['customer_from'])
        )

    if is_self_transfer(data):
        if not is_enough_amount(account_from.amount, amount):
            errors.get('errors').append(
                NOT_ENOUGH_AMOUNT % (amount, account_from.amount)
            )

        if not is_account_belongs_to_customer(account_to.customer.id,
                                              data['customer_from']):
            errors.get('errors').append(
                ACCOUNT_DOESNT_BELONG %
                (account_to.uuid, data['customer_from'])
            )
    else:
        if not is_different_customers(data['customer_to'],
                                      data['customer_from']):
            errors.get('errors').append(
                SAME_CUSTOMERS % data['customer_to']
            )

        if not is_account_belongs_to_customer(account_to.customer.id,
                                              data['customer_to']):
            errors.get('errors').append(
                ACCOUNT_DOESNT_BELONG %
                (account_to.uuid, data['customer_to'])
            )

        fee = calculate_fee(amount)

        if not is_enough_amount(account_from.amount, amount, fee):
            errors.get('errors').append(
                NOT_ENOUGH_AMOUNT_FEE % (amount, fee, account_from.amount)
            )

    return errors
