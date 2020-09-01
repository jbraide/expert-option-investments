from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Withdraw, VerificationDocument


# get_user_model
from django.contrib.auth import get_user_model

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=50)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')



# django countries & phone field
from django_countries.widgets import CountrySelectWidget
# from phone_field import PhoneField
class ProfileForm(forms.ModelForm):
    class Meta: 
        model = Profile
        fields = ('first_name', 'last_name','phone_number','street_address','city', 'state', 'postal_or_zip_code', 'profile_picture', 'country', 'select_plan')
        widgets = {
            'country': CountrySelectWidget(),
            # 'phone_number':
        }

class WithdrawalForm(forms.ModelForm):
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
     
    class Meta: 
        model = Withdraw
        fields = ('amount', 'password')

class VerificationDocumentForm(forms.ModelForm):    
    class Meta:
        model = VerificationDocument
        fields = ('document_type','front_document', 'back_document')
