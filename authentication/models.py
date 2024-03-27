import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
# class CustomUser(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     username = models.CharField(max_length=100,blank=False, default='')
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)
#     confirm_password = models.CharField(max_length=100)
#     mobile_phone = models.CharField(max_length=11)
#     profile_picture = models.ImageField(upload_to='authentication/images/', null=True, blank=True)
#     activation_key = models.UUIDField(default=uuid.uuid4, editable=False)
#     is_active = models.BooleanField(default=False)

class CustomUser(AbstractUser):
  #custom fields 
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  mobile_phone = models.CharField(max_length=11)
  profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
  confirm_password = models.CharField(max_length=100)
  activation_key = models.UUIDField(default=uuid.uuid4, editable=False)
  
  def activate(self):
    self.is_active = True
    self.save()
      
  def __str__(self):
    return f"{self.email}"

  @classmethod
  def get_all_users(cls):
    return cls.objects.all()

