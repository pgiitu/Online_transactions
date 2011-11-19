"""
All the functionality for the online_transaction moduel is impelemented in this file
"""
# Create your views here.
from django.shortcuts import render_to_response
from transactions.models import Transaction
from transactions.models import Connected_Account
from transactions.models import Connected_Account_Interbank
from transactions.models import Bank
from transactions.models import State
from transactions.models import Branch
from transactions.models import Account
from transactions.models import Bank_Account
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import HttpResponse
from decimal import Decimal
import datetime
import random
import urllib
import unicodedata

def login(request):
    """
    Function to redirect to login page
    """
    return render_to_response("login.html")

def interbankoption(request):
    """
    Fucntion to redirect to interbank transfer page which shows the option of RTGS and NEFT
    """
    return render_to_response("interbank_transfer2.html")

def home(request):
  """
  function to redirect to home page after logging in which contains the options of interbank transfer,
  funds transfer,and third party transfer
  """
  try:
    user_id = request.POST["user_id"]
    user = Account.objects.get(username=user_id)
    if user.password == request.POST["passwd"]:
        request.session['user_id'] = user.user_id
        request.session['username'] = user.username
	request.session['t_type']=0
	request.session['verification']=0
	request.session['sms_code']=0
        request.session.set_expiry(300)
        
        ifsc_code=request.session.get('ifsc_code')
        if ifsc_code:
#	  print "helllll"
	  id=request.session.get('user_id')
	  user_accounts = Bank_Account.objects.filter(ba_user_id=id)
	  return render_to_response("goods_and_services.html",{'user_accounts':user_accounts,},context_instance=RequestContext(request))
	else:	  
	  return render_to_response("home.html",context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/Online_transactions/")
  except Account.DoesNotExist:
        return HttpResponseRedirect("/Online_transactions/")
        
def verify_sms(request):
        """
  	fucntion to validate if the code which user enters matches the code sent on his mobile number
  
  	"""
	try:
	  code=request.POST["sms_code"]
	  code1=request.session.get('sms_code')
	  code2=unicodedata.normalize('NFKD', code).encode('ascii','ignore')
#	  print "i am here"
	  t_type=request.session.get('t_type')
	  print code1
	  print code2
	  if(Decimal(code1)==Decimal(code2)):
		request.session['verification']=1
	        id1=request.session.get('user_id')
	        user_accounts = Bank_Account.objects.filter(ba_user_id=id1)
	        connected_accounts = Connected_Account_Interbank.objects.filter(ca_host_acc_no=id1)
		return render_to_response(t_type,{'user_accounts':user_accounts,'connected_accounts':connected_accounts,'error':""})
	  else:
		return render_to_response("sms_verification.html",{'error':"confirmation unsuccessful"})
	except (KeyError):
	  print "i am here2"
	  return render_to_response("sms_verification.html",{'error':"confirmation unsuccessful"})
		
def show_funds_transfer(request):
  """
  it does sms validation and then show all the accounts of the user and gives the option
  to transfer from one account to his another account.
  It also performs various checks like whether the amount entered is within limits etc.
  """
  verification=request.session.get('verification')
  t_type1=request.session.get('t_type')
  if (verification==1):
	if(t_type1=="funds_transfer.html"):
	  try:
	    id=request.session.get('user_id')
	    user_accounts = Bank_Account.objects.filter(ba_user_id=id)
	    source_acc=request.POST["account1"]
	    destination_acc=request.POST["account2"]
	    amount1=request.POST["amount_to_transfer"]
	    amount=unicodedata.normalize('NFKD', amount1).encode('ascii','ignore')
	    account1=Bank_Account.objects.filter(ba_acc_no=source_acc)
	    account2=Bank_Account.objects.filter(ba_acc_no=destination_acc)
	    error1="Not enough money in your account"
	    error2="Please enter valid amount"
	    error3="Please enter amount in numeric only"
	    error4="Please choose different source and destination accounts" 
	    error5="You entered amount more than your account's transaction limit"
	    if (source_acc==destination_acc):
	    	return render_to_response("funds_transfer.html",{'user_accounts':user_accounts,'error':error4})	
	    try:
	    	i = float(amount)
	    except ValueError, TypeError:
	    	return render_to_response("funds_transfer.html",{'user_accounts':user_accounts,'error':error3})
	    else:
	    	if (i<=0 ):
			return render_to_response("funds_transfer.html",{'user_accounts':user_accounts,'error':error2})
	    for acc in account1:	
	    	if ((acc.ba_acc_bal)<Decimal(amount)):
		    return render_to_response("funds_transfer.html",{'user_accounts':user_accounts,'error':error1})
		elif(acc.ba_transaction_limit<Decimal(amount)):
		    return render_to_response("funds_transfer.html",{'user_accounts':user_accounts,'error':error5})
	    	else:
		    acc.ba_acc_bal=acc.ba_acc_bal-Decimal(amount)
		    print acc.ba_acc_bal
		    acc.save()
	    for acc in account2:
		ifsc_code1=acc.ba_ifsc_code
		acc.ba_acc_bal=acc.ba_acc_bal+Decimal(amount)
		acc.save();
		print acc.ba_acc_bal
	    tran=Transaction(t_amount=amount,t_sender_acc_no=source_acc,t_receiver_acc_no=destination_acc,t_rec_ifsc_code=ifsc_code1,t_start_date=datetime.datetime.now(),t_end_date=datetime.datetime.now(),t_status=1,t_transaction_type=0)
	    tran.save()
	    return render_to_response("transaction_status.html")
	  except (KeyError):
	    error3="Please select one source and destination account"
	    print "this was a key error"
	    id=request.session.get('user_id')
	    user_accounts = Bank_Account.objects.filter(ba_user_id=id)
	    return render_to_response("funds_transfer.html",{'user_accounts':user_accounts,'error':error3}) 

  else:
	id1=request.session.get('user_id')
        user_accounts = Account.objects.filter(user_id=id1)
	for acc in user_accounts:
		number=acc.mobile_no
		print number
	number=str(number)
	request.session['t_type']="funds_transfer.html"
	request.session['verification']=0
	n=random.randint(100000,200000)
	n=str(n)
	print "printing code"
	print n
	a=urllib.urlopen('http://ubaid.tk/sms/sms.aspx?uid=9779615166&pwd=mobilemessage&phone='+number+'&msg=This+is+the+verification+code+'+n+'&provider=way2sms').read()
	request.session['sms_code']=n
	return render_to_response("sms_verification.html",{'error':""})
	  
def transaction_status(request):
    """
    it redirects to the status of transaction done by user
    """
    return render_to_response("transaction_status.html")

def show_interbank_transfer(request):
  	  """
 	  function to transfer money to an account in differnt bank. It displays the accounts added previously by the
  	  user and also has the option of adding a new receiver. It performs various checks on ifsc code and transfer amount.
   	  """
	  try:
	    id1=request.session.get('user_id')
	    user_accounts = Bank_Account.objects.filter(ba_user_id=id1)
	    connected_accounts = Connected_Account_Interbank.objects.filter(ca_host_acc_no=id1)
	    source_acc=request.POST["account1"]
	    destination_acc=request.POST["account2"]
	    print source_acc
	    print destination_acc
	    amount1=request.POST["amount_to_transfer"]
	    amount=unicodedata.normalize('NFKD', amount1).encode('ascii','ignore')
	    account1=Bank_Account.objects.filter(ba_acc_no=source_acc)
	    account2=Connected_Account_Interbank.objects.filter(id=destination_acc)
	    error1="Not enough money in your account"
	    error2="Please enter valid amount"
	    error3="Please enter amount in numeric only"
	    error4="Please choose different source and destination accounts" 
	    error5="You entered amount more than your account's transaction limit"
	    error6="You entered amount more than connected account's transaction limit"
	    try:
	    	i = float(amount)
	    except ValueError, TypeError:
	    	return render_to_response("interbank_transfer.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts,'error':error3})
	    else:
	    	if (i<=0 ):
			return render_to_response("interbank_transfer.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts,'error':error2})
	    for acc in account2:
		destination_acc_no=acc.ca_acc_no
		ifsc_code1=acc.ca_ifsc_code
		if(acc.ca_limit<Decimal(amount)):
		    return render_to_response("interbank_transfer.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts,'error':error6})	
	    for acc in account1:	
	    	if ((acc.ba_acc_bal)<Decimal(amount)):
		    return render_to_response("interbank_transfer.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts,'error':error1})
		elif(acc.ba_transaction_limit<Decimal(amount)):
		    return render_to_response("interbank_transfer.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts,'error':error5})
	    	else:
		    acc.ba_acc_bal=acc.ba_acc_bal-Decimal(amount)
		    print acc.ba_acc_bal
		    acc.save()
	    tran=Transaction(t_amount=amount,t_sender_acc_no=source_acc,t_receiver_acc_no=destination_acc_no,t_rec_ifsc_code=ifsc_code1,t_start_date=datetime.datetime.now(),t_end_date=datetime.datetime.now(),t_status=1,t_transaction_type=2)
	    tran.save()
	    return render_to_response("transaction_status.html")
	  except (KeyError):
	    error3="Please select one source and destination account"
	    print "this was a key error"
	    id1=request.session.get('user_id')
	    user_accounts = Bank_Account.objects.filter(ba_user_id=id1)
	    connected_accounts = Connected_Account_Interbank.objects.filter(ca_host_acc_no=id1)
	    return render_to_response("interbank_transfer.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts,'error':error3})

def add_third_party(request):
  """
  function to add another party to which user wants to transfer the money.
  It fills in all the details of the receiver and also validates them.
  """
  try:
    cust_id=request.session.get('user_id')
    name=request.POST["name"]
    connected_acc_no1=request.POST["account_no"]
    confirm_acc_no=request.POST["account_no_2"]
    limit1=request.POST["limit"]
    error1="Account Confirmation Failed"
    error2="Please Enter Valid numbers in fields"
    error3="Please Enter numeral entries in fields"
    error4="Sorry The account you wish to connect does not exist"
    error6="Account Already Added"
    if(connected_acc_no1!=confirm_acc_no):
	return render_to_response("add_third_party.html",{'error':error1})
    limit=unicodedata.normalize('NFKD', limit1).encode('ascii','ignore')
    connected_acc_no=unicodedata.normalize('NFKD', connected_acc_no1).encode('ascii','ignore')
    try:
    	i = float(limit)
    except ValueError, TypeError:
    	return render_to_response("add_third_party.html",{'error':error3})
    else:
    	if (i<=0 ):
		return render_to_response("add_third_party.html",{'error':error2})
    try:
    	i = float(connected_acc_no)
    except ValueError, TypeError:
    	return render_to_response("add_third_party.html",{'error':error3})
    else:
    	if (i<=0 ):
		return render_to_response("add_third_party.html",{'error':error2})
    c_acc=Bank_Account.objects.filter(ba_acc_no=connected_acc_no)
    if (len(c_acc)==0):
	return render_to_response("add_third_party.html",{'error':error4})
    for acc in c_acc:
	ifsc_code1=acc.ba_ifsc_code
    c_acc=Connected_Account.objects.filter(ca_host_acc_id=cust_id)
    for acc in c_acc:
	if(acc.ca_connected_acc_no==connected_acc_no):
		return render_to_response("add_third_party.html",{'error':error6})
    instance=Connected_Account(ca_host_acc_id=cust_id,ca_name=name,ca_connected_acc_no=connected_acc_no,ca_addition_date=datetime.datetime.now(),ca_transfer_limit=limit,ca_ifsc=ifsc_code1)
    instance.save()
    return render_to_response("confirmation.html")
  except (KeyError):
    error5="Please Enter all the fields"
    return render_to_response("add_third_party.html",{'error':error5})

def add_other_bank_account(request):
  """
  function to add a receiver of another bank to which user wants to transfer the money.
  It fills in all the details of the receiver and also validates them.
  """
  try:
    cust_id=request.session.get('user_id')
    name=request.POST["name"]
    connected_acc_no1=request.POST["account_no"]
    confirm_acc_no=request.POST["account_no_2"]
    addressline1=request.POST["line1"]
    addressline2=request.POST["line2"]
    addressline3=request.POST["line3"]
    IFSC_code1=request.POST["IFSC"]
    limit1=request.POST["limit"]

    error1="Account Confirmation Failed"
    error2="Please Enter Valid numbers in fields"
    error3="Please Enter numeral entries in fields"
    error4="Sorry The account you wish to connect does not exist"
    error6="Account Already Added"
    error7="IFSC code does no exists"
    if(connected_acc_no1!=confirm_acc_no):
	return render_to_response("add_other_bank_account.html",{'error':error1})
    limit=unicodedata.normalize('NFKD', limit1).encode('ascii','ignore')
    connected_acc_no=unicodedata.normalize('NFKD', connected_acc_no1).encode('ascii','ignore')
    IFSC_code=unicodedata.normalize('NFKD', IFSC_code1).encode('ascii','ignore')
    try:
    	i = float(limit)
    except ValueError, TypeError:
    	return render_to_response("add_other_bank_account.html",{'error':error3})
    else:
    	if (i<=0.0 ):
		print "hel"
		return render_to_response("add_other_bank_account.html",{'error':error2})
    try:
    	i = float(connected_acc_no)
    except ValueError, TypeError:
    	return render_to_response("add_other_bank_account.html",{'error':error3})
    else:
    	if (i<=0.0 ):
		print "hello"
		return render_to_response("add_other_bank_account.html",{'error':error2})
    c_acc=Connected_Account_Interbank.objects.filter(ca_host_acc_no=cust_id)
    for acc in c_acc:
	if(acc.ca_acc_no==connected_acc_no):
		return render_to_response("add_other_bank_account.html",{'error':error6})
    bank=Branch.objects.filter(ifsc_code=IFSC_code)
    if(len(bank)!=1):
	 return render_to_response("add_other_bank_account.html",{'error':error7})
    instance=Connected_Account_Interbank(ca_host_acc_no=cust_id,ca_acc_no=connected_acc_no,ca_addition_date=datetime.datetime.now(),ca_limit=limit,ca_name=name,ca_addressline1=addressline1,ca_addressline2=addressline2,ca_addressline3=addressline3,ca_ifsc_code=IFSC_code)
    instance.save()
    return render_to_response("confirmation.html")
  except (KeyError):
    error5="Please Enter all the fields"
    return render_to_response("add_other_bank_account.html",{'error':error5})

def show_thirdparty_transfer(request):
  """
  this function transfer the amount to the receiver of same bank.
  It shows all the parties added by the user and also checkes teh transfer limit and other things
  """
  try:
    id1=request.session.get('user_id')
    user_accounts = Bank_Account.objects.filter(ba_user_id=id1)
    connected_accounts = Connected_Account.objects.filter(ca_host_acc_id=id1)
    source_acc=request.POST["account1"]
    destination_acc=request.POST["account2"]
    amount1=request.POST["amount_to_transfer"]
    amount=unicodedata.normalize('NFKD', amount1).encode('ascii','ignore')
    account1=Bank_Account.objects.filter(ba_acc_no=source_acc)
    account2=Connected_Account.objects.filter(id=destination_acc)
    error1="Not enough money in your account"
    error2="Please enter valid amount"
    error3="Please enter amount in numeric only"
    error4="Please choose different source and destination accounts" 
    error5="You entered amount more than your account's transaction limit"
    error6="You entered amount more than connected account's transaction limit"
    try:
    	i = float(amount)
    except ValueError, TypeError:
    	return render_to_response("third_party.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts,'error':error3})
    else:
    	if (i<=0 ):
		return render_to_response("third_party.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts,'error':error2})
    for acc in account2:
	destination_acc_no=acc.ca_connected_acc_no
	ifsc_code1=acc.ca_ifsc
	if(acc.ca_transfer_limit<Decimal(amount)):
	    return render_to_response("third_party.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts,'error':error6})	
    for acc in account1:	
    	if ((acc.ba_acc_bal)<Decimal(amount)):
	    return render_to_response("third_party.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts,'error':error1})
	elif(acc.ba_transaction_limit<Decimal(amount)):
	    return render_to_response("third_party.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts,'error':error5})
    	else:
            acc.ba_acc_bal=acc.ba_acc_bal-Decimal(amount)
	    print acc.ba_acc_bal
	    acc.save()
    tran=Transaction(t_amount=amount,t_sender_acc_no=source_acc,t_receiver_acc_no=destination_acc_no,t_rec_ifsc_code=ifsc_code1,t_start_date=datetime.datetime.now(),t_end_date=datetime.datetime.now(),t_status=1,t_transaction_type=1)
    tran.save()
    return render_to_response("transaction_status.html")
  except (KeyError):
    error3="Please select one source and destination account"
    print "this was a key error"
    id1=request.session.get('user_id')
    user_accounts = Bank_Account.objects.filter(ba_user_id=id1)
    connected_accounts = Connected_Account.objects.filter(ca_host_acc_id=id1)
    return render_to_response("third_party.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts,'error':error3})


def logout(request):
    """
    function for logging out and ending teh session
    """
    try:
        del request.session['user_id']
        del request.session['user_name']
        flush()
    except KeyError:
        pass
    return render_to_response("logout.html")

def goods_and_services(request,amount,acc_no,ifsc_code,ref_no):
      """
      fucntion to transfer the amount if a request for money transfer from soem website which sells 
      onlien goods and services come
      """
      request.session['amount'] = amount
      request.session['acc_no_services'] = acc_no
      request.session['ifsc_code'] = ifsc_code
      request.session['ref_no'] = ref_no
      try:
        id=request.session.get('user_id')
        if id:
	  user_accounts = Bank_Account.objects.filter(ba_user_id=id)
	  #print "hello"
	  return render_to_response("goods_and_services.html")
	else:
	  return render_to_response("login.html")	  
      except:
	#print "hello1"
	return render_to_response("login.html")
