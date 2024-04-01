import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  mobile_phone = models.CharField(max_length=11)
  profile_picture = models.ImageField(upload_to='auth', null=True) # (REQUIRED)
  confirm_password = models.CharField(max_length=100)
  activation_key = models.UUIDField(default=uuid.uuid4, editable=False)
  birthdate = models.DateField(null=True, blank=True)
  facebook_profile = models.URLField(max_length=200, null=True, blank=True)
  country = models.CharField(max_length=100, null=True, blank=True)

  def activate(self):
    self.is_active = True
    self.save()
      
  def __str__(self):
    return f"{self.email}"

  @classmethod
  def get_all_users(cls):
    return cls.objects.all()
  
  @property
  def image_url(self):
    return f'/media/{self.profile_picture}'

