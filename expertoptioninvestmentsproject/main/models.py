from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _

# use this instead of User
from django.contrib.auth import settings


# importing uuid for custom username ids
import uuid


'''
    creating custom user
'''

class UserManager (BaseUserManager):
    """ 
        Define a model manager for User Model with no usename field
    """
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('the given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        #  create and save a regular User with the given email and password.
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        #  create and save a regular User with the given email and password.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # validation errors
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff= True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser= True')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    user_id = models.UUIDField(primary_key = True, default= uuid.uuid4, editable=False)
    # username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

'''
    Other  models
'''
# balance
class Balance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

# invested amount
class InvestedAmount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

# forex signals 
class Signals(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

# Account type 
class AccountType(models.Model):
    account_types = [
        ('premium', 'premium'), 
        ('luxury', 'luxury'), 
        ('vip', 'VIP'), 
        ('vip luxury', 'vip luxury'), 
        ('silver', 'silver'), 
        ('gold', 'gold'), 
        ('platinum', 'platinum'), 
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=30, choices=account_types)

# Notifications
class Notification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    details = models.CharField(max_length=40)
    amount = models.PositiveIntegerField()


# profile
''' 
for phone field
'''
from phonenumber_field.modelfields import PhoneNumberField

plans = (
    ('Mini', 'Mini'),
    ('Entry', 'Entry'),
    ('Silver', 'Silver'),
    ('Gold', 'Gold'),
    ('Platinum', 'Platinum')
)
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=23, default='', blank=True)
    last_name = models.CharField(max_length=23, default='', blank=True)
    phone_number = PhoneNumberField(blank=True, help_text='Contact Phone Number')
    street_address = models.CharField(max_length=150, default='', blank=True)
    city =  models.CharField(max_length = 100, default=False, blank=True)
    state = models.CharField(max_length=30, default= '', blank=True)
    postal_or_zip_code = models.CharField(max_length=6, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    country = CountryField(blank_label='(select country)', blank=True, null=True)
    select_plan = models.CharField(max_length=40, choices=plans)
    def __str__(self):
        return self.user.username
    
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         profile = Profile(user=instance)
#         # Profile.objects.create(user=instance)
#     instance.profile.save()
# post_save.connect(create_user_profile, sender=User)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Withdraw(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)    
    password = models.CharField(max_length=30, default = '')

class BTCAddress(models.Model):
    address = models.CharField(max_length=40, default='')

class VerificationDocument(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=30)
    front_document = models.FileField(upload_to='doc/front_page/', blank=False, null=False)
    back_document = models.FileField(upload_to='doc/back_page/', blank=False, null=False)
    verified = models.BooleanField(default=False, blank=True)