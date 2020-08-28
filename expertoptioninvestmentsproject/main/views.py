from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import login as auth_login


from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, ProfileForm, WithdrawalForm

# models
from .models import Balance, Signals, AccountType, InvestedAmount, BTCAddress, Profile
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
@login_required(login_url='/accounts/login')
def fund_account(request):
    return render(request, 'main/fund-account.html')

# transactions view 
def trading_history(request):
    return render(request, 'main/trading-history.html')

# withdrawal fn
from django.contrib.auth.hashers import check_password

@login_required(login_url='/accounts/login')
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


''' account setup '''
'''         registration / logout            '''


# registration route
# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         # profile = ProfileForm(request.POST, instance=request.user.profile, files=request.FILES)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user_login = authenticate(request,username=username, password=password)
#             auth_login(request, user_login)

#             return redirect('main:profile-form')
#         else:
#             print(form.errors)


#             # # profile creation test
#             # first_name = form.cleaned_data.get('first_name')
#             # last_name = form.cleaned_data.get('last_name')
#             # email = form.cleaned_data.get('email')
#             # profile_picture = form.cleaned_data.get('profile_picture')
#             # country = form.cleaned_data.get('country') 


#             # Profile.objects.create()

#             # if profile.is_valid():
#             #     user.profile.first_name = form.cleaned_data.get('first_name')
#             #     user.profile.last_name = form.cleaned_data.get('last_name')
#             #     user.profile.email = form.cleaned_data.get('email')
#             #     user.profile.profile_picture = form.cleaned_data.get('profile_picture')
#             #     user.profile.country = form.cleaned_data.get('country')

#             #     user.save()
#             #     profile.save()
#             #     return redirect('main:dashboard')
        
#             # else:
#             #     print('Something went wrong')
#             #     print(form.errors)
#             #     print(profile.errors)


#     else:
#         form = RegistrationForm()
#         # profile = ProfileForm()
#     context = {
#         'form': form, 
#         # 'profile': profile
#     }
#     return render(request, 'main/register.html', context)


# custom registration route
from django.contrib.auth.forms import UserCreationForm
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        # form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user_login = authenticate(request,username=username, password=password)
            auth_login(request, user_login)
            return redirect('main:profile-form')
        else:
            print(form.errors)
    else:
        # form = UserCreationForm()
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'main/register.html', context)

def create_profile(request):
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if reg_form.is_valid() and profile_form.is_valid():
            user = reg_form.save(commit=False)
            user.refresh_from_db()

            # # TESTING w/ profile model
            # user = request.user
            # print(user)
            # first_name = profile_form.cleaned_data.get('first_name')
            # last_name = profile_form.cleaned_data.get('last_name')
            # phone_number = profile_form.cleaned_data.get('phone_number')
            # street_address = profile_form.cleaned_data.get('street_address')
            # city = profile_form.cleaned_data.get('city')
            # state = profile_form.cleaned_data.get('state')
            # postal_or_zip_code = profile_form.cleaned_data.get('postal_or_zip_code')
            # profile_picture = profile_form.cleaned_data.get('profile_picture')
            # country = profile_form.cleaned_data.get('country')

            # Profile.objects.create(
            #     user=user.user_id, 
            #     first_name = first_name,
            #     last_name = last_name,
            #     phone_number = phone_number, 
            #     street_address=street_address,
            #     city = city,
            #     state = state, 
            #     postal_or_zip_code = postal_or_zip_code,
            #     profile_picture = profile_picture,
            #     country  = country 
            # )            

            user.profile.first_name = profile_form.cleaned_data.get('first_name')
            user.profile.last_name = profile_form.cleaned_data.get('last_name')
            user.profile.phone_number = profile_form.cleaned_data.get('phone_number')
            user.profile.street_address = profile_form.cleaned_data.get('street_address')
            user.profile.city = profile_form.cleaned_data.get('city')
            user.profile.state = profile_form.cleaned_data.get('state')
            user.profile.postal_or_zip_code = profile_form.cleaned_data.get('postal_or_zip_code')
            user.profile.profile_picture = profile_form.cleaned_data.get('profile_picture')
            user.profile.country = profile_form.cleaned_data.get('country')

            profile_form.save()
            return redirect('main:dashboard')
        else:
            print(reg_form.errors)
            print(profile_form.errors)
    else:
        print(request.user.first_name)
        profile_form = ProfileForm()
    context = {
        'profile_form': profile_form
    }
    return render(request, 'main/profile.html', context)
# logout route
@login_required(login_url='/accounts/login')
def logout_view(request):
    logout(request)
    return redirect('main:index')

