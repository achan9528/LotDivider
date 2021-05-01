from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    number = models.CharField(max_length=50, default=uuid.uuid4)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    # objects = UserManager()

    # projects 

    def __str__(self):
        return f"Name: {self.name}"

class Project(models.Model):
    owners = models.ManyToManyField(User, related_name="projects")
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50, default=uuid.uuid4)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # draftPortfolios

    def __str__(self):
        return (f"Project Name: {self.name}, Project Number: {self.number}")