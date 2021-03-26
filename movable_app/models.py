from django.db import models
from accounts.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Ornaments(models.Model):
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


class Stocks(models.Model):
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


class Share(models.Model):
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


class Insurance(models.Model):
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


class Cash_or_bankvalue(models.Model):
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

class Vehicles(models.Model):
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

class Electronics(models.Model):
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

class Other_m(models.Model):
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

class NoteField(models.Model):
    ornament = models.ForeignKey(Ornaments, on_delete = models.CASCADE, related_name='ornaments', null= True, blank = True)
    stock = models.ForeignKey(Stocks, on_delete = models.CASCADE, related_name='stocks', null= True, blank = True)
    share = models.ForeignKey(Share, on_delete = models.CASCADE, related_name='shares', null= True, blank = True)
    insurance = models.ForeignKey(Insurance, on_delete = models.CASCADE, related_name='insurances', null= True, blank = True)
    cash_or_bankvalue = models.ForeignKey(Cash_or_bankvalue, on_delete = models.CASCADE, related_name='Cash_or_bankvalues', null= True, blank = True)
    vehicles = models.ForeignKey(Vehicles, on_delete = models.CASCADE, related_name='vehicles', null= True, blank = True)
    electronic = models.ForeignKey(Electronics, on_delete = models.CASCADE, related_name='electronics', null= True, blank = True)
    other_m = models.ForeignKey(Other_m, on_delete = models.CASCADE, related_name='others_m', null= True, blank = True)
    notefield  = models.FileField(upload_to = 'immovable-files/', blank = True, null = True)
    
    def __str__(self):
        return str(self.pk)