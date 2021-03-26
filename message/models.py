from django.db import models
from django.db import models
from django.conf import settings
from django.template.defaultfilters import truncatechars


class InboxMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='receiver')
    new_msg_active = models.BooleanField(default=True)
    delete_status = models.BooleanField(default=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    @property
    def sliced_message(self):
        return truncatechars(self.message, 40)




class NewMessage(models.Model):
    MSG_STATUS = (
        ('Send', 'Send'),
        ('Draft', 'Draft'),
    )
    msg = models.ForeignKey(InboxMessage, on_delete=models.SET_NULL, null=True, blank=True, related_name='reply')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='new_msg_receiver')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='new_msg_sender')
    msg_status = models.CharField(max_length=6, choices=MSG_STATUS, default='Send')
    new_msg_active = models.BooleanField(default=True)
    delete_status = models.BooleanField(default=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)

    @property
    def sliced_message(self):
        return truncatechars(self.message, 40)




