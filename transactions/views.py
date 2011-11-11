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
import datetime

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
#  if(request.session)
    id=request.session.get('user_id')
    user_accounts = Bank_Account.objects.filter(ba_user_id=id)
    return render_to_response("funds_transfer.html",{'user_accounts':user_accounts})
#  endif
#  return render_to_response("login.html")

def show_interbank_transfer(request):
    id=request.session.get('user_id')
    user_accounts = Bank_Account.objects.filter(ba_user_id=id)
    connected_accounts = Connected_Account_Interbank.objects.filter(ca_host_acc_no=id)
    return render_to_response("interbank_transfer.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts})
#    return render_to_response("login.html")

def add_third_party(request):
    return render_to_response("add_third_party.html")
def add_other_bank_account(request):
    return render_to_response("add_other_bank_account.html")

def show_thirdparty_transfer(request):
    id=request.session.get('user_id')
    user_accounts = Bank_Account.objects.filter(ba_user_id=id)
    connected_accounts = Connected_Account.objects.filter(ca_host_acc_id=id)
    return render_to_response("third_party.html",{'user_accounts':user_accounts,'connected_accounts':connected_accounts})

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
