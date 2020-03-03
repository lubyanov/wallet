from uuid import uuid4
from copy import deepcopy
from decimal import Decimal
from unittest import TestCase
from dataclasses import dataclass

from wallet.models import Account, Customer, Currency
from api_v1.validations import transfer_data_validate
from api_v1.serializers import TransferSerializer


@dataclass
class TestData:
    customer_from: Customer
    customer_to: Customer
    account_from: Account
    account_to_s2s: Account
    account_to_s2a: Account
    data_s2s: TransferSerializer
    data_s2a: TransferSerializer
    data_same_customers: TransferSerializer
    amount: Decimal


class TransferDataValidationCase(TestCase):

    def __init__(self, *args, **kwargs):
        super(TransferDataValidationCase, self).__init__(*args, **kwargs)
        self._data = self._get_transfer_data()

    @staticmethod
    def _get_transfer_data():
        amount = Decimal(10)
        customer_from = Customer(id=1, first_name='John', last_name='Doe')
        customer_to = Customer(id=2, first_name='Jane', last_name='Doe')
        account_from = Account(
            uuid=uuid4(),
            customer=customer_from,
            currency=Currency.USD,
            amount=Decimal(100)
        )
        account_to_s2s = Account(
            uuid=uuid4(),
            customer=customer_from,
            currency=Currency.EUR,
            amount=Decimal(0)
        )
        account_to_s2a = Account(
            uuid=uuid4(),
            customer=customer_to,
            currency=Currency.EUR,
            amount=Decimal(0)
        )
        data_s2s = TransferSerializer({
            'customer_from': customer_from.id,
            'account_from': None,
            'account_to': None,
            'amount': None
        })
        data_s2a = TransferSerializer({
            'customer_from': customer_from.id,
            'customer_to': customer_to.id,
            'account_from': None,
            'account_to': None,
            'amount': None
        })
        data_same_customers = TransferSerializer({
            'customer_from': customer_from.id,
            'customer_to': customer_from.id,
            'account_from': None,
            'account_to': None,
            'amount': None
        })

        return TestData(
            customer_from=customer_from,
            customer_to=customer_to,
            account_from=account_from,
            account_to_s2s=account_to_s2s,
            account_to_s2a=account_to_s2a,
            data_s2s=data_s2s.data,
            data_s2a=data_s2a.data,
            data_same_customers=data_same_customers.data,
            amount=amount
        )

    def test_is_enough_amount(self):
        # self to self transfer case: when everything is ok
        errors = transfer_data_validate(
            self._data.account_from,
            self._data.account_to_s2s,
            self._data.data_s2s,
            self._data.amount
        )
        self.assertFalse(errors['errors'])

        errors = transfer_data_validate(
            self._data.account_from,
            self._data.account_to_s2s,
            self._data.data_s2s,
            self._data.account_from.amount * 2
        )
        self.assertTrue(errors['errors'])
        self.assertEqual(len(errors['errors']), 1)

        # self to another transfer case: when everything is ok
        errors = transfer_data_validate(
            self._data.account_from,
            self._data.account_to_s2a,
            self._data.data_s2a,
            self._data.amount
        )
        self.assertFalse(errors['errors'])

        errors = transfer_data_validate(
            self._data.account_from,
            self._data.account_to_s2a,
            self._data.data_s2a,
            self._data.account_from.amount * 2
        )
        self.assertTrue(errors['errors'])
        self.assertEqual(len(errors['errors']), 1)

    def test_is_different_customers(self):
        # self to another transfer case: when everything is ok
        errors = transfer_data_validate(
            self._data.account_from,
            self._data.account_to_s2a,
            self._data.data_s2a,
            self._data.amount
        )
        self.assertFalse(errors['errors'])

        errors = transfer_data_validate(
            self._data.account_from,
            self._data.account_to_s2a,
            self._data.data_same_customers,
            self._data.amount
        )
        self.assertTrue(errors['errors'])
        self.assertEqual(len(errors['errors']), 2)

    def test_is_account_belongs_to_customer(self):
        # self to self transfer case: when everything is ok
        errors = transfer_data_validate(
            self._data.account_from,
            self._data.account_to_s2s,
            self._data.data_s2s,
            self._data.amount
        )
        self.assertFalse(errors['errors'])

        # self to self transfer case:
        # let's change 'account_from' belongings to another customer
        account_from_with_another_customer = deepcopy(self._data.account_from)
        account_from_with_another_customer.customer = self._data.customer_to
        errors = transfer_data_validate(account_from_with_another_customer,
                                        self._data.account_to_s2s,
                                        self._data.data_s2s,
                                        self._data.amount)
        self.assertTrue(errors['errors'])
        self.assertEqual(len(errors['errors']), 1)

        # self to self transfer case:
        # let's change 'account_to' belongings to another customer
        account_to_with_another_customer = deepcopy(self._data.account_to_s2s)
        account_to_with_another_customer.customer = self._data.customer_to
        errors = transfer_data_validate(self._data.account_from,
                                        account_to_with_another_customer,
                                        self._data.data_s2s,
                                        self._data.amount)
        self.assertTrue(errors['errors'])
        self.assertEqual(len(errors['errors']), 1)

        # self to another transfer case: when everything is ok
        errors = transfer_data_validate(
            self._data.account_from,
            self._data.account_to_s2a,
            self._data.data_s2a,
            self._data.amount
        )
        self.assertFalse(errors['errors'])

        # self to another transfer case:
        # let's change 'account_to' belongings to another customer
        account_to_with_another_customer = deepcopy(self._data.account_to_s2a)
        account_to_with_another_customer.customer = self._data.customer_from
        errors = transfer_data_validate(self._data.account_from,
                                        account_to_with_another_customer,
                                        self._data.data_s2a,
                                        self._data.amount)
        self.assertTrue(errors['errors'])
        self.assertEqual(len(errors['errors']), 1)
