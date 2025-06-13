from django.db import models

# Create your models here.
class Education(models.Model0):
    title = models.CharField(max_legnht=50)
    description = models.TextField()