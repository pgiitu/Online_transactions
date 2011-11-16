"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from transactions.models import Transaction
from transactions.models import Connected_Account
from transactions.models import Connected_Account_Interbank
from transactions.models import Bank
from transactions.models import State
from transactions.models import Branch
from transactions.models import Account
from transactions.models import Bank_Account
from decimal import Decimal
import datetime
import unicodedata


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
