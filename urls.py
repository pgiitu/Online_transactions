from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Online_transactions.views.home', name='home'),
    # url(r'^Online_transactions/', include('Online_transactions.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^Online_transactions/','transactions.views.login'),
    url(r'^home_page/','transactions.views.home'),
    url(r'^funds_transfer/','transactions.views.show_funds_transfer'),
    url(r'^interbank_transfer/','transactions.views.show_interbank_transfer'),
    url(r'^interbank_transfer2/','transactions.views.interbankoption'),
    url(r'^third_party_transfer/','transactions.views.show_thirdparty_transfer'),
    url(r'^add_third_party/','transactions.views.add_third_party'),
    url(r'^add_other_bank_account/','transactions.views.add_other_bank_account'),
    url(r'^logout/','transactions.views.logout'),
    url(r'^complete_payment_goods/','transactions.views.transfer_goods'),
    url(r'^transaction_status/','transactions.views.transaction_status'),
    url(r'^verify_sms/','transactions.views.verify_sms'),
    url(r'^merchant/amount=(?P<amount>.+)/account_no=(?P<acc_no>\d+)/ifsc_code=(?P<ifsc_code>\d+)/ref_no=(?P<ref_no>\d+)$','transactions.views.goods_and_services'),
    url(r'^transaction_api/account_id=(?P<source_acc_id>\d+)/account_no=(?P<source_acc_no>\d+)/account_id2=(?P<dest_acc_id>\d+)/account_no2=(?P<dest_acc_no>\d+)/ifsc_code=(?P<ifsc_code>.+)/amount=(?P<amount>\d+)','transactions.views.api_working'),
    url(r'^sms_api/number=(?P<number>\d+)/message=(?P<message>.+)','transactions.views.sms_api'),
)
