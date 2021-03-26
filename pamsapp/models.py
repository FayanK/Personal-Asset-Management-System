from django.db import models
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.template.defaultfilters import truncatechars

User = get_user_model()

# Create your models here.
class Designation(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    gender_type = (
        ('1', 'Male'),
        ('2', 'Female'),
        ('3', 'Others'),
    )
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE , related_name = 'profile')
    image = models.ImageField(upload_to = 'images/', blank=True, null=True)
    designation = models.ForeignKey(Designation, on_delete = models.CASCADE, blank = True, null = True)
    gender = models.CharField(max_length=10, choices=gender_type, blank = True, null = True)
    
    def __str__(self):
        return self.user.name

@receiver(post_save, sender= CustomUser)  
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

@receiver(post_save, sender= CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Messsage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete= models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    seen = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date_created",)

    @property
    def sliced_message(self):
        return truncatechars(self.message, 20)



