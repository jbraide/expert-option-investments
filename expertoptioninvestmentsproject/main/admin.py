from django.contrib import admin
from .models import Profile, Balance, InvestedAmount, Signals, BTCbalance, VerificationDocument
from .models import DailyInvestments

'''
    custom user admin fieldset
'''
"""Integrate with admin module."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import CustomUser
from .forms  import RegistrationForm


@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    DjangoUserAdmin.fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ()}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_form = RegistrationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    # add_form = RegistrationForm
    # CUSTOM USER 1
    list_display = ('email',)
    search_fields = ('email',)
    ordering = ('email',)

    # CUSTOM USER 2
    # list_display = ('email', 'first_name', 'last_name', 'is_staff')
    # search_fields = ('email', 'first_name', 'last_name')
    # ordering = ('email',)


''' 
    Other fields
'''

# profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', ]

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount']

@admin.register(InvestedAmount)
class InvestedAmountAdmin(admin.ModelAdmin):
    list_display = ['user','amount',]

@admin.register(Signals)
class SignalsAdmin(admin.ModelAdmin):
    list_display = ['user','amount',]

@admin.register(BTCbalance)
class BTCbalanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount']

# verfication documents
@admin.register(VerificationDocument)
class VerificationDocumentAdmin(admin.ModelAdmin):
    list_display = ['user',]

# btc balance
@admin.register(DailyInvestments)
class DailyInvestmentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount']
    

    

    




