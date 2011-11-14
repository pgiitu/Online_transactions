from django.db import models

class Account(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=10)
    user_id = models.CharField(max_length=15,primary_key=True)  # i have put it a char if needed we can change it to integer
    def __unicode__(self):
        return self.username

class Transaction(models.Model):
    t_amount=models.CharField(max_length=10)
    t_sender_acc_no = models.CharField(max_length=10)
    t_receiver_acc_no = models.CharField(max_length=10)
    t_rec_ifsc_code = models.CharField(max_length=10)
    t_start_date = models.DateTimeField('Start Date')  #date on which the transactions was requested
    t_end_date = models.DateTimeField('End Date')    #date on which the transactions was completed
    t_status=models.IntegerField()                  # we can define the various staus code for the successful and unsuccessful transactions
    t_transaction_type = models.IntegerField()     # 0 for funds transfer   1 for Third party  2 for Inter bank
    def __unicode__(self):
        return self.t_sender_acc_no

class Connected_Account(models.Model):
    ca_host_acc_id = models.CharField(max_length=10)
    ca_name=models.CharField(max_length=25)
    ca_connected_acc_no = models.CharField(max_length=10)
    ca_ifsc=models.CharField(max_length=10)
    ca_addition_date = models.DateTimeField('Date Of Addition')   
    ca_transfer_limit=models.IntegerField()   #transfer limit for the connected account
    def __unicode__(self):
        return self.ca_host_acc_id

class Connected_Account_Interbank(models.Model):
    ca_host_acc_no = models.CharField(max_length=10)
    ca_acc_no = models.CharField(max_length=10)
    ca_addition_date = models.DateTimeField('Date of Addition')
    ca_name = models.CharField(max_length=30)
    ca_addressline1=models.CharField(max_length=25)
    ca_addressline2=models.CharField(max_length=25)
    ca_addressline3=models.CharField(max_length=25)
    ca_limit=models.IntegerField()
    ca_ifsc_code=models.CharField(max_length=10)
    def __unicode__(self):
        return self.ca_host_acc_no

class Bank(models.Model):
    bank_name = models.CharField(max_length=10)
    def __unicode__(self):
        return self.bank_name

class State(models.Model):			# i have used the state instead of State as proposed by us in the class diagram
    bank = models.ForeignKey(Bank)
    state_name = models.CharField(max_length=20)
    def __unicode__(self):
        return self.state_name


class Branch(models.Model):
    branch = models.ForeignKey(State)
    branch_name = models.CharField(max_length=10)
    ifsc_code = models.CharField(max_length=10)  # i have put it a char if needed we can change it to integer
    def __unicode__(self):
        return self.branch_name

class Bank_Account(models.Model):
    ba_user_id = models.ForeignKey(Account)
    ba_acc_no = models.CharField(max_length=15)
    ba_ifsc_code = models.CharField(max_length=10)  # i have put it a char if needed we can change it to integer
    ba_acc_type = models.IntegerField()   # 1 represents savings acoount 2 represents current account and so on
    ba_transaction_limit= models.DecimalField(max_digits=11, decimal_places=3)  # transaction limit
    ba_no_transactions = models.IntegerField()  #limit on the number of transactions per day
    ba_acc_bal= models.DecimalField(max_digits=11, decimal_places=3)  #account bal
    def __unicode__(self):
        return self.ba_acc_no
    

# Create your models here.
