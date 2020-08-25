from django.urls import path
from .views import index, login, logout_view, dashboard, register,t_and_c, about, fund_account, trading_history, withdraw_funds
from .views import id_verification, account_upgrade
app_name = 'main'

urlpatterns = [
    # home page
    path('', index, name="index"),
    # about
    path('about/', about, name='about'),
    # terms and conditions, Privacy policy
    path('terms-and-conditions/', t_and_c, name='terms-and-conditions'),
    # dashboard routes
    path('dashboard/', dashboard, name="dashboard"),
    path('fund-account/', fund_account, name='fund_account'), 
    path('trading-history/', trading_history, name='trading-history'),
    path('withdraw-funds/', withdraw_funds, name='withdraw-funds'),
    path('id-verification/', id_verification, name='id-verification'),    path('logout/', logout_view, name='logout'),
    path('account/upgrade', account_upgrade, name='account-upgrade'),
    # registration and login routes
    path('register/', register, name='register'),

    
]
