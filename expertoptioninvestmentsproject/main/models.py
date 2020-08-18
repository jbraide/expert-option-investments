from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


# balance
class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

# invested amount
class InvestedAmount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

# forex signals 
class Signals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=30, choices=account_types)

# Notifications
class Notification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    details = models.CharField(max_length=40)
    amount = models.PositiveIntegerField()


# profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=23, default='', blank=True)
    last_name = models.CharField(max_length=23, default='', blank=True)
    email = models.EmailField(max_length=50)
    street_address = models.CharField(max_length=150, default='', blank=True)
    city =  models.CharField(max_length = 100, default=False, blank=True)
    state = models.CharField(max_length=30, default= '', blank=True)
    postal_or_zip_code = models.CharField(max_length=6, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    status = models.BooleanField(default=False)
    country = CountryField(blank_label='(select country)', blank=True, null=True)
    def __str__(self):
        return self.user.username
    
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         profile = Profile(user=instance)
#         # Profile.objects.create(user=instance)
#     instance.profile.save()
# post_save.connect(create_user_profile, sender=User)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Deposit(models.Model):
    deposit_choices = [
        ('Bitcoin', 'bitcoin'),
    ]
    currency = [
        ('usd', 'USD'), 
        ('eur', 'EUR'), 
        ('pounds', 'GBP')
    ]
    select_payment_method = models.CharField(max_length=20, choices=deposit_choices)
    select_currency = models.CharField(max_length=20, choices=currency)
    amount = models.BigIntegerField(default='')

    class Meta:
        verbose_name = 'Signal'
        verbose_name_plural = 'Signals'


class Withdraw(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)    
    password = models.CharField(max_length=30, default = '')

class BTCAddress(models.Model):
    address = models.CharField(max_length=40, default='')