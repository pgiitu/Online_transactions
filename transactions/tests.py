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
    
    
    def setUp(self):
      
        """
        creating banks
        """
        name="SBI"
        self.bank1=Bank.objects.create(bank_name=name)
      
        s_name="punjab"
        self.state1=self.bank1.state_set.create(state_name=s_name)
      
        
        b_name="ropar"
        b_ifsc="101"
      
        self.state1.branch_set.create(branch_name=b_name,ifsc_code=b_ifsc)
        b_name="ropar"
        b_ifsc="102"
        self.state1.branch_set.create(branch_name=b_name,ifsc_code=b_ifsc)

        b_name="ropar"
        b_ifsc="201"
        self.state1.branch_set.create(branch_name=b_name,ifsc_code=b_ifsc)

        b_name="ropar"
        b_ifsc="202"
        self.state1.branch_set.create(branch_name=b_name,ifsc_code=b_ifsc)
      
        b_name="ropar"
        b_ifsc="801"
        self.state1.branch_set.create(branch_name=b_name,ifsc_code=b_ifsc)
      
        b_name="ropar"
        b_ifsc="802"
        self.state1.branch_set.create(branch_name=b_name,ifsc_code=b_ifsc)
      
        b_name="ropar"
        b_ifsc="901"
        self.state1.branch_set.create(branch_name=b_name,ifsc_code=b_ifsc)
      
      
        """
        Sets up the data base for the test cases
        """
        
        user1 = 'test_user1'
        passwd1 = 'test_passwd'
        mobno1 = '7814681937'
        userid1= '1001'
        self.user1 = Account.objects.create(username=user1, password=passwd1, mobile_no=mobno1,user_id=userid1)
	usr1=Account.objects.get(user_id=userid1)
        user2 = 'test_user2'
        passwd2 = 'test_passwd'
        mobno2 = '9646318665'
        userid2= '2001'
        self.user2 = Account.objects.create(username=user2, password=passwd2, mobile_no=mobno2,user_id=userid2)
	usr2=Account.objects.get(user_id=userid2)
        
#        bac_user_id1=
        bac_acc_no1="10001"
        bac_ifsc_code1="101"
        bac_acc_type1="1"
        bac_transaction_limit1=10000
        bac_no_transactions1=3
        bac_acc_bal1=30000
        
        self.user1.bank_account_set.create(ba_acc_no=bac_acc_no1,ba_ifsc_code=bac_ifsc_code1,ba_acc_type=bac_acc_type1,ba_transaction_limit=bac_transaction_limit1,ba_no_transactions=bac_no_transactions1,ba_acc_bal=bac_acc_bal1)
        #self.bank_accoun1=Bank_Account.objects.create(ba_user_id=usr1,ba_acc_no=bac_acc_no1,ba_ifsc_code=bac_ifsc_code1,ba_acc_type=bac_acc_type1,ba_transaction_limit=bac_transaction_limit1,ba_no_transactions=bac_no_transactions1,ba_acc_bal=bac_acc_bal1)

        bac_acc_no2="10002"
        bac_ifsc_code2="102"
        bac_acc_type2="2"
        bac_transaction_limit2=10000
        bac_no_transactions2=3
        bac_acc_bal2=20000

	self.user1.bank_account_set.create(ba_acc_no=bac_acc_no2,ba_ifsc_code=bac_ifsc_code2,ba_acc_type=bac_acc_type2,ba_transaction_limit=bac_transaction_limit2,ba_no_transactions=bac_no_transactions2,ba_acc_bal=bac_acc_bal2)
        #self.bank_accoun2=Bank_Account.objects.create(ba_user_id=usr1,ba_acc_no=bac_acc_no2,ba_ifsc_code=bac_ifsc_code2,ba_acc_type=bac_acc_type2,ba_transaction_limit=bac_transaction_limit2,ba_no_transactions=bac_no_transactions2,ba_acc_bal=bac_acc_bal2)
        
	#mapping account for the second user2
        
        bac_acc_no3="20001"
        bac_ifsc_code3="201"
        bac_acc_type3="1"
        bac_transaction_limit3=10000
        bac_no_transactions3=3
        bac_acc_bal3=40000
        	
	self.user2.bank_account_set.create(ba_acc_no=bac_acc_no3,ba_ifsc_code=bac_ifsc_code3,ba_acc_type=bac_acc_type3,ba_transaction_limit=bac_transaction_limit3,ba_no_transactions=bac_no_transactions3,ba_acc_bal=bac_acc_bal3)

        bac_acc_no4="20002"
        bac_ifsc_code4="202"
        bac_acc_type4="2"
        bac_transaction_limit4=10000
        bac_no_transactions4=3
        bac_acc_bal4=60000
        	
	self.user2.bank_account_set.create(ba_acc_no=bac_acc_no4,ba_ifsc_code=bac_ifsc_code4,ba_acc_type=bac_acc_type4,ba_transaction_limit=bac_transaction_limit4,ba_no_transactions=bac_no_transactions4,ba_acc_bal=bac_acc_bal4)


	#      Adding the connected accounts
	
	
	cac_host_acc_no1 = "1001"
        cac_acc_no1 = "20001"
        cac_addition_date1 = datetime.datetime.now()
	cac_name1 = "connected_1"
	cac_limit1=10000
	cac_ifsc_code1="201"
	self.connected_acc1=Connected_Account.objects.create(ca_host_acc_id=cac_host_acc_no1,ca_connected_acc_no=cac_acc_no1,ca_addition_date=cac_addition_date1,ca_name=cac_name1,ca_transfer_limit=cac_limit1,ca_ifsc=cac_ifsc_code1)
	

	cac_host_acc_no2 = "2001"
        cac_acc_no2 = "10001"
        cac_addition_date2 = datetime.datetime.now()
	cac_name2 = "connected_2"
	cac_limit2=10000
	cac_ifsc_code2="101"
	self.connected_acc2=Connected_Account.objects.create(ca_host_acc_id=cac_host_acc_no2,ca_connected_acc_no=cac_acc_no2,ca_addition_date=cac_addition_date2,ca_name=cac_name2,ca_transfer_limit=cac_limit2,ca_ifsc=cac_ifsc_code2)

	#self.connected_acc2=Connected_Account.objects.create(ca_host_acc_no=cac_host_acc_no2,ca_acc_no=cac_acc_no2,ca_addition_date=cac_addition_date2,ca_name=cac_name1,ca_addressline=cac_addressline12,ca_addressline2=cac_addressline22,ca_addressline3=cac_addressline32,ca_transfer_limit=cac_limit2,ca_ifsc_code=cac_ifsc_code2)
	#adding the connected accounts for interbank
	in_cac_host_acc_no1 = "1001"
        in_cac_acc_no1 = "9001"
        in_cac_addition_date1 = datetime.datetime.now()
	in_cac_name1 = "connected_1"
	in_cac_addressline11="a"
	in_cac_addressline21="b"
	in_cac_addressline31="c"
	in_cac_limit1=10000
	in_cac_ifsc_code1="801"
	self.in_connected_acc1=Connected_Account_Interbank.objects.create(ca_host_acc_no=in_cac_host_acc_no1,ca_acc_no=in_cac_acc_no1,ca_addition_date=in_cac_addition_date1,ca_name=in_cac_name1,ca_addressline1=in_cac_addressline11,ca_addressline2=in_cac_addressline21,ca_addressline3=in_cac_addressline31,ca_limit=in_cac_limit1,ca_ifsc_code=in_cac_ifsc_code1)
	

	in_cac_host_acc_no2 = "2001"
        in_cac_acc_no2 = "9002"
        in_cac_addition_date2 = datetime.datetime.now()
	in_cac_name2 = "connected_2"
	in_cac_addressline12="a"
	in_cac_addressline22="b"
	in_cac_addressline32="c"
	in_cac_limit2=10000
	in_cac_ifsc_code2="802"
	self.in_connected_acc2=Connected_Account_Interbank.objects.create(ca_host_acc_no=in_cac_host_acc_no2,ca_acc_no=in_cac_acc_no2,ca_addition_date=in_cac_addition_date2,ca_name=in_cac_name2,ca_addressline1=in_cac_addressline12,ca_addressline2=in_cac_addressline22,ca_addressline3=in_cac_addressline32,ca_limit=in_cac_limit2,ca_ifsc_code=in_cac_ifsc_code2)
    
	#entering the bank
	
    
	#entering the ifsc codes in the database
	
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
        
   
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
	
	c = Client()
        response = c.post('/funds_transfer',{'account1':'10001', 'account2':'10002','amount_to_transfer':5000})
        #self.assertEqual(response.status_code,301)
        account = Bank_Account.objects.get(ba_acc_no="10001")
        #self.assertEqual(account.ba_acc_bal,Decimal(18000))
        
        account2 = Bank_Account.objects.get(ba_acc_no="10002")
        #self.assertEqual(account2.ba_acc_bal,Decimal(68000))


    def test_Thirdparty_transfer(self):
        """
        Check the third party
        """
	
	c = Client()
        response = c.post('/home_page',{'user_id':'test_user1', 'passwd':'test_passwd'})
        self.assertEqual(response.status_code, 301)
        
        response=c.post('/third_party_transfer/')
	
        response = c.post('/third_party_transfer/',{'user_id':'1001','account1':'10001', 'account2':'20001','amount_to_transfer':5000})
        account = Bank_Account.objects.get(ba_acc_no="10001")
        self.assertEqual(account.ba_acc_bal,Decimal(25000))
  
    def test_Thirdparty_transfer_transaction_limit_exceed(self):
        """
        Check the third party
        """
	
	c = Client()
        response = c.post('/home_page',{'user_id':'test_user1', 'passwd':'test_passwd'})
        self.assertEqual(response.status_code, 301)
        
        response=c.post('/third_party_transfer/')
	
        response = c.post('/third_party_transfer/',{'user_id':'1001','account1':'10001', 'account2':'20001','amount_to_transfer':15000})
	self.assertEqual(response.status_code,200)
#	print "\n\n\n\n"
#        print response.status_code
#        print response.content
#        print "\n\n"
#        print response.__getitem__('error')
        #self.assertEqual(response.error,"You entered amount more than your account's transaction limit")
#        account = Bank_Account.objects.get(ba_acc_no="10001")
#        self.assertEqual(account.ba_acc_bal,Decimal(25000))

#       self.assertEqual(response.status_code,301)
 #       account = Bank_Account.objects.get(ba_acc_no=1234)
 #       self.assertEqual(account.ba_acc_bal,Decimal(18000))
        
  #      account2 = Bank_Account.objects.get(ba_acc_no=1235)
   #     self.assertEqual(account2.ba_acc_bal,Decimal(68000))

    def test_interbank_transfer(self):
        """
        Check the interbank transafer party
        """
	
	c = Client()
        response = c.post('/home_page',{'user_id':'test_user1', 'passwd':'test_passwd'})
        self.assertEqual(response.status_code, 301)
        
        response=c.post('/interbank_transfer2/')
	
        response = c.post('/interbank_transfer/',{'user_id':'1001','account1':'10002', 'account2':'9001','amount_to_transfer':5000})
        account = Bank_Account.objects.get(ba_acc_no="10002")
        self.assertEqual(account.ba_acc_bal,Decimal(15000))
