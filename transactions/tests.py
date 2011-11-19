"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test import Client
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
        
    def setUp(self):
        pass        
   
    def test_NavigationHome(self):
        """
        Checks whether all the pages are navigable or not.
        """
        c = Client()
        response = c.post('/Online_transactions/')
        self.assertEqual(response.status_code, 200)
        
    def test_simple_funds_transfer(self):
        """
        Check the simple funds transfer
        """
        user = 'test_user'
        passwd = 'test_passwd'
        mobno = '7814681937'
        userid= '1001'
        newuser = Account(username=user, password=passwd, mobile_no=mobno,user_id=userid)
	newuser.save()
	
	bankaccount1=Bank_Account(ba_user_id=newuser,ba_acc_no='1234',ba_ifsc_code='100001',ba_acc_type=1,ba_transaction_limit=10000,ba_no_transactions=5,ba_acc_bal=23000)
	bankaccount1.save()

	bankaccount2=Bank_Account(ba_user_id=newuser,ba_acc_no='1235',ba_ifsc_code='100001',ba_acc_type=2,ba_transaction_limit=20000,ba_no_transactions=6,ba_acc_bal=63000)
	bankaccount2.save()
	
	c = Client()
        response = c.post('/funds_transfer',{'account1':'1234', 'account2':'1235','amount_to_transfer':5000})
        self.assertEqual(response.status_code,301)
        account = Bank_Account.objects.get(ba_acc_no=1234)
        self.assertEqual(account.ba_acc_bal,Decimal(18000))
        
        account2 = Bank_Account.objects.get(ba_acc_no=1235)
        self.assertEqual(account2.ba_acc_bal,Decimal(68000))
	