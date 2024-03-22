from django.db import models

# Create your models here.

class CustomUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    mobile_phone = models.CharField(max_length=11)
    profile_picture = models.ImageField(upload_to='authentication/images/', null=True, blank=True)
    
    def __str__(self):
      return f"{self.email}"

    @classmethod
    def get_all_users(cls):
        return cls.objects.all()
