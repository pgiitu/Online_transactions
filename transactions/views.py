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
    	if (amount<=0 ):
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
        acc.ba_acc_bal=acc.ba_acc_bal+Decimal(amount)
	acc.save();
	print acc.ba_acc_bal
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
    	if (amount<=0 ):
		return render_to_response("interbank_transfer.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts,'error':error2})
    for acc in account2:
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
    return render_to_response("transaction_status.html")
  except (KeyError):
    error3="Please select one source and destination account"
    print "this was a key error"
    id1=request.session.get('user_id')
    user_accounts = Bank_Account.objects.filter(ba_user_id=id1)
    connected_accounts = Connected_Account_Interbank.objects.filter(ca_host_acc_no=id1)
    return render_to_response("interbank_transfer.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts,'error':error3})

def add_third_party(request):
    return render_to_response("add_third_party.html")
def add_other_bank_account(request):
    return render_to_response("add_other_bank_account.html")

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
    	if (amount<=0 ):
		return render_to_response("third_party.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts,'error':error2})
    for acc in account2:
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
    return render_to_response("transaction_status.html")
  except (KeyError):
    error3="Please select one source and destination account"
    print "this was a key error"
    id1=request.session.get('user_id')
    user_accounts = Bank_Account.objects.filter(ba_user_id=id1)
    connected_accounts = Connected_Account.objects.filter(ca_host_acc_id=id1)
    return render_to_response("third_party.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts,'error':error3})

def add_account_confirmation(request):
    cust_id=request.session.get('user_id')
    name=request.POST["name"]
    connected_acc_no=request.POST["account_no"]
    addressline1=request.POST["line1"]
    addressline2=request.POST["line2"]
    addressline3=request.POST["line3"]
    IFSC_code=request.POST["IFSC"]
    limit=request.POST["limit"]
    instance=Connected_Account_Interbank(ca_host_acc_no=cust_id,ca_acc_no=connected_acc_no,ca_addition_date=datetime.datetime.now(),ca_limit=limit,ca_name=name,ca_addressline1=addressline1,ca_addressline2=addressline2,ca_addressline3=addressline3,ca_ifsc_code=IFSC_code)
    instance.save()
    return render_to_response("confirmation.html")

def add_account_confirmation2(request):
    cust_id=request.session.get('user_id')
    name=request.POST["name"]
    connected_acc_no=request.POST["account_no"]
    limit=request.POST["limit"]
    instance=Connected_Account(ca_host_acc_id=cust_id,ca_connected_acc_no=connected_acc_no,ca_addition_date=datetime.datetime.now(),ca_transfer_limit=limit,ca_ifsc_code=0)
    instance.save()
    return render_to_response("confirmation2.html")
    
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
