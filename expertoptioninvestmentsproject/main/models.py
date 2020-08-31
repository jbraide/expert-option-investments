from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _

''' custom user stuff '''
# timezone for custom user model
from django.utils import timezone

# importing uuid for custom username ids
import uuid

# use this instead of User
from django.contrib.auth import settings

''' 
for phone field
'''
from phonenumber_field.modelfields import PhoneNumberField


'''
    creating custom user
'''
# CUSTOM user first design

class CustomUserManager(BaseUserManager):
    ''' custom user model manager wher email is the unique identifiers for authentication instead of usernames '''

    def _create_user(self, email, password,is_staff, is_superuser, **extra_fields):
        ''' create and save a User with the given email and password '''
        if not email:
            raise ValueError(_('The email must be set'))
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)
    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email  


# CUSTOM user second design

""" class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, commit=True):
        ''' 
            # creates and saves a User with the given email, first name, last name and password.
        '''
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not first_name:
            raise ValueError(_('Users Must have a first name'))
        if not last_name:
            raise ValueError(_('Users Must have a last name'))

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name, 
            last_name = last_name,
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        ''' 
        # creates and saves a superuser with the given email, first name, last name and password.
        '''
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
# timezone
from django.utils import timezone

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('email address'), max_length=255, unique=True
    )
    # password field supplied by AbstractUser
    # last login supplied by AbstractUser
    first_name = models.CharField(_('first_name'), max_length=30, blank=True)
    last_name = models.CharField(_('last_name'), max_length=150, blank=True)

    is_active = models.BooleanField(
        _('active'),
        default=True, 
        help_text = _(
            'Designate whether this user should be treated as active. '
            'unselect this instead of deleting accounts'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'), 
        default=False,
        help_text = _(
            'Designates whether the user can log into this admin site'
        )
    )
    # is_superuser field provided by PermissionsMixin
    # group fields provided by permissions MIxin
    # user_permissions field provided by PermissionsMixin
    date_joined = models.DateTimeField(_("date joined"), default= timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    def get_full_name(self):
        ''' 
        # return the first_name plus the last)name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    def __str__(self):
        return '{} <{}'.format(self.get_full_name(), self.email)

    def has_perm(self,perm, obj=None):
        # Does the user have a specific permission?
        # simplest possible answer: yes, always
        return True
    def has_module_perms(self,app_label):
        # Does the user have  permissions to view the app 'app_label'
        # simplest possible answer: yes, always
        return True    
"""

"""
    Registration  models
    
"""

# profile

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
        return self.first_name
        
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

'''
    Dashboard  models
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

# Notifications
class Notification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    details = models.CharField(max_length=40)
    amount = models.PositiveIntegerField()

# withdrawal
class Withdraw(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)    
    password = models.CharField(max_length=30, default = '')

# bitcoin balance
class BTCbalance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=11, decimal_places=11)

# daily Investments
class DailyInvestments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    amount = models.PositiveIntegerField()

# verification documents
class VerificationDocument(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=30)
    front_document = models.FileField(upload_to='doc/front_page/', blank=False, null=False)
    back_document = models.FileField(upload_to='doc/back_page/', blank=False, null=False)
    verified = models.BooleanField(default=False, blank=True)