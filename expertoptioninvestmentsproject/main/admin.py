from django.contrib import admin
from .models import Profile, Balance, Deposit, InvestedAmount, AccountType, Signals, BTCAddress

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', ]

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount']

# @admin.register(Deposit)
# class DepositAdmin(admin.ModelAdmin):
#     list_display = ['user','amount',]

@admin.register(InvestedAmount)
class InvestedAmountAdmin(admin.ModelAdmin):
    list_display = ['user','amount',]
    
@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ['user', 'type']

@admin.register(Signals)
class SignalsAdmin(admin.ModelAdmin):
    list_display = ['user','amount',]

@admin.register(BTCAddress)
class BTCAddressAdmin(admin.ModelAdmin):
    list_display = ['address', ]
    




