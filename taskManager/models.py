from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Users(AbstractUser):

    def __str__(self):
        return self.username

class Task(models.Model):
    subject = models.TextField()
    answer = models.TextField(null=True)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)