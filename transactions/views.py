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
import unicodedata

def login(request):
    return render_to_response("login.html")

def interbankoption(request):
    return render_to_response("interbank_transfer2.html")

def home(request):
  try:
    user_id = request.POST["user_id"]
    user = Account.objects.get(username=user_id)
    if user.password == request.POST["passwd"]:
        request.session['user_id'] = user.user_id
        request.session['username'] = user.username
        request.session.set_expiry(300)
        return render_to_response("home.html",context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/Online_transactions/")
  except Account.DoesNotExist:
        return HttpResponseRedirect("/Online_transactions/")
        
        
def show_funds_transfer(request):
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

def transaction_status(request):
    return render_to_response("transaction_status.html")

def show_interbank_transfer(request):
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
    try:
        del request.session['user_id']
        del request.session['user_name']
    except KeyError:
        pass
    return render_to_response("logout.html")

def goods_and_services(request,amount,acc_no,ifsc_code,ref_no):
    if request.session:
      id=request.session.get('user_id')
      user_accounts = Bank_Account.objects.filter(ba_user_id=id)
      return render_to_response("goods_and_services.html",{'user_accounts':user_accounts,'amount':amount,'acc_no':acc_no,'ifsc_code':ifsc_code,'ref_no':ref_no})
    endif
    return render_to_response("login.html")
