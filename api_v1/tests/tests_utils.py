from decimal import Decimal

from django.test import TestCase

from app.settings import TRANSFER_FEE_PERCENT
from api_v1.utils import calculate_fee


class UtilsTestCase(TestCase):

    def test_calculate_fee(self):
        amount = Decimal(100)

        result = calculate_fee(amount)
        expected = Decimal(amount / 100 * TRANSFER_FEE_PERCENT)

        self.assertEqual(expected, result)
        self.assertNotEqual(expected + 1, result)
        self.assertNotEqual(expected - 1, result)

    def test_is_account_belongs_to_customer(self):
        # TODO: implement
        pass

    def test_is_self_transfer(self):
        # TODO: implement
        pass

    def test_is_enough_amount(self):
        # TODO: implement
        pass

    def test_is_different_customers(self):
        # TODO: implement
        pass
