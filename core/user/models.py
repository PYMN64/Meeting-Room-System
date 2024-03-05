from django.db import models
from django.contrib.auth.models import AbstractUser 
from phonenumber_field.modelfields import PhoneNumberField 

# Create your models here. 

class CustomUser(AbstractUser): 
    first_name = None 
    last_name = None 
    phone_number = PhoneNumberField(unique=True, blank=True, null=True) 
    is_admin = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

