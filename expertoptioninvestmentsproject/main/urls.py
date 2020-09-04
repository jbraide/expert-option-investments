from django.urls import path

'''
home, privacy policy, Payment Policy views
'''

from .views import index, logout_view, about, register,terms_and_condition, privacy_policy, payment_policy

# dashboard routes
from .views import dashboard, id_verification, account_upgrade, account_type, create_profile, fund_account, trading_history, withdraw_funds

app_name = 'main'

urlpatterns = [
    # home page
    path('', index, name="index"),
    # about
    path('about/', about, name='about'),
    path('account-types', account_type, name='account-type'),
    # terms and conditions, Privacy policy
    path('terms-and-conditions/', terms_and_condition, name='terms-and-conditions'),
    path('privacy-policy', privacy_policy, name='privacy-policy'),
    path('payment-policy', payment_policy, name='payment-policy'),
    # dashboard routes
    path('dashboard/', dashboard, name="dashboard"),
    path('fund-account/', fund_account, name='fund_account'), 
    path('trading-history/', trading_history, name='trading-history'),
    path('withdraw-funds/', withdraw_funds, name='withdraw-funds'),
    path('id-verification/', id_verification, name='id-verification'), 
    path('logout/', logout_view, name='logout'),
    path('account/upgrade', account_upgrade, name='account-upgrade'),
    # registration and login routes
    path('register/', register, name='register'),
    path('profile/create', create_profile, name='profile-form' )
    
]
