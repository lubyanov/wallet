from django.db import models


DECIMAL_PARAMS = {'decimal_places': 2, 'max_digits': 10}


class Currency(models.TextChoices):
    USD = 'USD'
    EUR = 'EUR'
    CNY = 'CNY'


class Action(models.TextChoices):
    INITIAL = 'INITIAL'
    TRANSFER = 'TRANSFER'
    CHARGE = 'CHARGE'


class Customer(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)


class Account(models.Model):
    uuid = models.UUIDField()
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='accounts')
    currency = models.CharField(max_length=3, choices=Currency.choices)
    amount = models.DecimalField(**DECIMAL_PARAMS)


class Transaction(models.Model):
    customer_from = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='tx_from')
    customer_to = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='tx_to')
    account_from = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='tx_from')
    account_to = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='tx_to')
    amount = models.DecimalField(**DECIMAL_PARAMS)
    action = models.CharField(max_length=128, choices=Action.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
