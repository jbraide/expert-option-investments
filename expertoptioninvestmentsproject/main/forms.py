from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Deposit, Withdraw

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        # labels = {
        #     'password2', 'Confirmation:'
        # }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


# django countries 
from django_countries.widgets import CountrySelectWidget
class ProfileForm(forms.ModelForm):
    class Meta: 
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'street_address','city', 'state', 'postal_or_zip_code', 'profile_picture', 'country')
        widgets = {
            'country': CountrySelectWidget()
        }


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ('select_payment_method','select_currency','amount')

class WithdrawalForm(forms.ModelForm):
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
     
    class Meta: 
        model = Withdraw
        fields = ('amount', 'password')
