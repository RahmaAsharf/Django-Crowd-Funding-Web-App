from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from django.db import models
from projects.models import Project

User = get_user_model()

class FeaturedProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'project')