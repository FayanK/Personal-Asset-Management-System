from django.db import models
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from PIL import Image
from django.conf import settings
import os


User = get_user_model()

# Create your models here.
class Land(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, )
    date_of_acquisition = models.DateField()
    owner = models.CharField(max_length = 200)
    class_and_location = models.CharField(max_length = 200)
    details = models.CharField(max_length = 1000)
    how_acquired_and_value = models.CharField(max_length = 1000 )   
    source_of_money = models.CharField(max_length = 1000 )   
    opinon = models.CharField(max_length = 1000)
    signature = models.ImageField()
    is_confirm = models.BooleanField(default=False)  


    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        size = 300, 300

        if self.signature:
            pic = Image.open(self.signature.path)
            pic.thumbnail(size, Image.LANCZOS)
            pic.save(self.signature.path)


class Building(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    date_of_acquisition = models.DateField()
    owner = models.CharField(max_length = 200)
    class_and_location = models.CharField(max_length = 200)
    details = models.CharField(max_length = 1000)
    how_acquired_and_value = models.CharField(max_length = 1000)   
    source_of_money = models.CharField(max_length = 1000)   
    opinon = models.CharField(max_length = 1000) 
    signature = models.ImageField()
    is_confirm = models.BooleanField(default=False)    

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        size = 300, 300

        if self.signature:
            pic = Image.open(self.signature.path)
            pic.thumbnail(size, Image.LANCZOS)
            pic.save(self.signature.path)

class Homestead(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    date_of_acquisition = models.DateField()
    owner = models.CharField(max_length = 200)
    class_and_location = models.CharField(max_length = 200)
    details = models.CharField(max_length = 1000)
    how_acquired_and_value = models.CharField(max_length = 1000)   
    source_of_money = models.CharField(max_length = 1000)   
    opinon = models.CharField(max_length = 1000) 
    signature = models.ImageField()
    is_confirm = models.BooleanField(default=False)        

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        size = 300, 300

        if self.signature:
            pic = Image.open(self.signature.path)
            pic.thumbnail(size, Image.LANCZOS)
            pic.save(self.signature.path)

class BusinessFirm(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    date_of_acquisition = models.DateField()
    owner = models.CharField(max_length = 200)
    class_and_location = models.CharField(max_length = 200)
    details = models.CharField(max_length = 1000)
    how_acquired_and_value = models.CharField(max_length = 1000)   
    source_of_money = models.CharField(max_length = 1000)   
    opinon = models.CharField(max_length = 1000)  
    signature = models.ImageField()
    is_confirm = models.BooleanField(default=False)  

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        size = 300, 300

        if self.signature:
            pic = Image.open(self.signature.path)
            pic.thumbnail(size, Image.LANCZOS)
            pic.save(self.signature.path)

class Other(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name='+')
    date_of_acquisition = models.DateField()
    owner = models.CharField(max_length = 200)
    class_and_location = models.CharField(max_length = 200)
    details = models.CharField(max_length = 1000)
    how_acquired_and_value = models.CharField(max_length = 1000)   
    source_of_money = models.CharField(max_length = 1000)   
    opinon = models.CharField(max_length = 1000)   
    signature = models.ImageField()
    is_confirm = models.BooleanField(default=False)  

    def __str__(self):
        return str(self.user)  

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        size = 300, 300

        if self.signature:
            pic = Image.open(self.signature.path)
            pic.thumbnail(size, Image.LANCZOS)
            pic.save(self.signature.path)
    
class NoteField_im(models.Model):
    land = models.ForeignKey(Land, on_delete = models.CASCADE, related_name='lands', null= True, blank = True)
    building = models.ForeignKey(Building, on_delete = models.CASCADE, related_name='buildings', null= True, blank = True)
    homestead = models.ForeignKey(Homestead, on_delete = models.CASCADE, related_name='homestead', null= True, blank = True)
    businessFirm = models.ForeignKey(BusinessFirm, on_delete = models.CASCADE, related_name='business_Firms', null= True, blank = True)
    other = models.ForeignKey(Other, on_delete = models.CASCADE, related_name='others', null= True, blank = True)
    notefield  = models.FileField(upload_to = 'immovable-files/', blank = True, null = True)
    
    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        size = 300, 300

        if self.signature:
            pic = Image.open(self.signature.path)
            pic.thumbnail(size, Image.LANCZOS)
            pic.save(self.signature.path)