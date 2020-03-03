from decimal import Decimal
from typing import Dict

from wallet.models import Account, Action, Transaction
from app.settings import TRANSFER_FEE_PERCENT
from api_v1.serializers import TransferSerializer, AccountSerializer


CUSTOMER_TO = 'customer_to'


def calculate_fee(amount: Decimal) -> Decimal:
    return Decimal(amount / 100 * TRANSFER_FEE_PERCENT)


def is_account_belongs_to_customer(account_customer: int,
                                   customer: int) -> bool:
    return account_customer == customer


def is_self_transfer(data: TransferSerializer) -> bool:
    return False if CUSTOMER_TO in data else True


def is_enough_amount(account: Decimal,
                     amount: Decimal, fee: Decimal = 0) -> bool:
    return True if account - amount - fee > 0 else False


def is_different_customers(customer_to: int, customer_from) -> bool:
    return customer_to != customer_from


def get_success_response(account_from: Account, account_to: Account) -> Dict:
    return {
        'from': {
            'id': account_from.customer.id,
            'first_name': account_from.customer.first_name,
            'last_name': account_from.customer.last_name,
            'account': AccountSerializer(account_from).data
        },
        'to': {
            'id': account_to.customer.id,
            'first_name': account_to.customer.first_name,
            'last_name': account_to.customer.last_name,
            'account': AccountSerializer(account_to).data
        },
    }


def get_history_tx(account_from: Account, account_to: Account,
                   amount: Decimal, action: Action) -> Transaction:
    """ Prepare history transaction object """
    return Transaction(
        customer_from=account_from.customer,
        customer_to=account_to.customer,
        account_from=account_from,
        account_from_uuid=account_from.uuid,
        account_from_currency=account_from.currency,
        account_from_amount=account_from.amount,
        account_to=account_to,
        account_to_uuid=account_to.uuid,
        account_to_currency=account_to.currency,
        account_to_amount=account_to.amount,
        amount=amount,
        action=action
    )
