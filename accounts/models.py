from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
import hashlib

# Create your models here.
class CustomUserManager(BaseUserManager):
    def Create_user(self, email, name, phone_no = None, password = None):
        if not email:
            raise ValueError('User must have an email')
        if not phone_no:
            raise ValueError('User must have a phone number')

        email = email.lower()
        name = name.title()

        user = self.model(
            email = self.normalize_email(email),
            name = name,
            phone_no = phone_no
        )
        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_superuser(self, email, name, phone_no = None, password = None):
        user = self.Create_user(
            email = email,
            name = name,
            phone_no = phone_no,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using = self._db)

        return user


class CustomUser(AbstractBaseUser):
    user_type_data = (
        ('1', 'Super admin'),
        ('2', 'Admin'),
        ('3', 'Employee'),
    )
    user_type = models.CharField(max_length=10, choices=user_type_data, default='3')
    email = models.EmailField(max_length=255, unique = True, verbose_name = 'Email')
    name = models.CharField(max_length = 255, verbose_name = 'Full Name')
    phone_no = models.CharField(max_length = 20, unique = True, verbose_name = 'Phone Number')
    date = models.DateField(auto_now_add = True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('name','phone_no')

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email
    
    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return self.is_admin

    class Meta:
        verbose_name_plural = 'Users'

class EmailConfirmed(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    activation_key = models.CharField(max_length = 500)
    email_confirmed = models.BooleanField(default=False)
    email_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = 'User Email-Confirmed'

@receiver(post_save, sender=CustomUser)
def create_user_email_confirmation(sender, instance, created, **kwargs):
    if created:
        dt = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        email_confirmed_instance = EmailConfirmed(user = instance)
        user_encoded = f'{instance.email}-{dt}'.encode()
        activation_key = hashlib.sha224(user_encoded).hexdigest()
        email_confirmed_instance.activation_key = activation_key
        email_confirmed_instance.save()

