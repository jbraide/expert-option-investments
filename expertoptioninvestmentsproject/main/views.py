from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import login as auth_login


from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm, ProfileForm, WithdrawalForm

# models
from .models import Balance, Signals, AccountType, InvestedAmount, BTCAddress
from django.db.models import Sum

# password reset 
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# time, dateteime
# import time
import datetime


''' views with no logic  '''

# homepage
def index(request):
    return render(request, 'main/index.html')

# About us page
def about(request):
    return render(request, 'main/about.html')

# account types
def account_type(request):
    return render(request, 'main/account-types.html')  

def payment_policy(request):
    return render(request, 'main/payment-policy.html') #not completed

# terms and conditions
def t_and_c(request):
    return render(request,'main/terms-and-conditions.html') #not completed


''' views with logic '''

'''             dashboard things             '''

# dashboard homepage / trading center
@login_required(login_url='/login')
def dashboard(request):
    user = request.user
    balance = Balance.objects.filter(user=user).aggregate(amount=Sum('amount'))
    # signals_amount = Signals.objects.filter(user=user).aggregate(amount=Sum('amount'))
    # invested = InvestedAmount.objects.filter(user=user).aggregate(amount=Sum('amount'))
    # type = AccountType.objects.filter(user=user)

   
    context = {
        'balance': balance, 
        # 'signals': signals_amount, 
        # 'invested': invested, 
        # 'type': type
    }
    return render(request, 'main/dashboard.html', context)

# fund account
from django.contrib import messages
@login_required(login_url='/login')
def fund_account(request):
    return render(request, 'main/fund-account.html')

# transactions view 
def trading_history(request):
    return render(request, 'main/trading-history.html')

# withdrawal fn
from django.contrib.auth.hashers import check_password

@login_required(login_url='/login')
def withdraw_funds(request): 
    user = request.user
    balance = Balance.objects.filter(user=user).aggregate(amount=Sum('amount'))
    form = WithdrawalForm(request.POST)
    userPassword = request.user.password
    if request.method == 'POST':
        messages.success(request, 'Withdrawal pending please wait a shortwhile')
        
        
        if form.is_valid():
            form.save(commit=False)
            password = form.cleaned_data.get('password')

            match_password = check_password(password, userPassword)
            # messages.success(request, 'Withdraw Successful')
            
            if match_password:
                print('passwords matched')
                form.save()
                return redirect('main:dashboard')
            else:
                print('problem with matching password')
        else: 
            print('error')
    else:
        form = WithdrawalForm()

    context = {
        'form': form,
        'balance': balance,
    }

    return render(request, 'main/withdraw-funds.html', context )

def id_verification(request):
    # change file location to the verification document
    return render(request, 'main/id-verification.html')

def account_upgrade(request):
    return render(request, 'main/account-upgrade.html')
'''         registration / logout            '''
# registration route
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user_login = authenticate(request,username=username, password=password)
            auth_login(request, user_login)

            profile = ProfileForm(request.POST, instance=request.user.profile, files=request.FILES)
            if profile.is_valid():
                user.profile.first_name = form.cleaned_data.get('first_name')
                user.profile.last_name = form.cleaned_data.get('last_name')
                user.profile.email = form.cleaned_data.get('email')
                user.profile.profile_picture = form.cleaned_data.get('profile_picture')
                user.profile.country = form.cleaned_data.get('country')

                user.save()
                profile.save()
                return redirect('main:dashboard')
        
            else:
                print('Something went wrong')
                print(form.errors)
                print(profile.errors)


    else:
        form = RegistrationForm()
        profile = ProfileForm()
    context = {
        'form': form, 
        'profile': profile
    }
    return render(request, 'main/register.html', context)

# logout route
@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('main:index')

