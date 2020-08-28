from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Withdraw


# get_user_model
from django.contrib.auth import get_user_model

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=50)

    class Meta:
        model = get_user_model()
        fields = ('email','username', 'first_name', 'last_name', 'password1', 'password2')
        # labels = {
        #     'password2', 'Confirmation:'
        # }



# django countries & phone field
from django_countries.widgets import CountrySelectWidget
# from phone_field import PhoneField
class ProfileForm(forms.ModelForm):
    class Meta: 
        model = Profile
        fields = ('first_name', 'last_name','phone_number','street_address','city', 'state', 'postal_or_zip_code', 'profile_picture', 'country')
        widgets = {
            'country': CountrySelectWidget(),
            # 'phone_number':
        }

class WithdrawalForm(forms.ModelForm):
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
     
    class Meta: 
        model = Withdraw
        fields = ('amount', 'password')
