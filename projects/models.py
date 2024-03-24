from django.db import models
from django.urls import reverse
from authentication.models import CustomUser
from django.db.models import Avg, Count
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    startDate = models.DateField() 
    endDate = models.DateField()
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    @property
    def show_url(self):
        url = reverse('view_projects')
        return url
    
    def averageReview(self):
        reviews = Rating.objects.filter(project=self.id).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = Rating.objects.filter(project=self.id).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
    def totalDonate(self):
        return sum(donation.amount for donation in self.donation_set.all())

        
class Image(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return str(self.image)
    

class Rating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, null=True)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    
class Donation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} donated ${self.amount} to {self.project.title}"
