from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255, default=uuid.uuid4)
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

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    fractionalLotsAllowed = models.BooleanField(default=False)
    number = models.CharField(max_length=50, default=uuid.uuid4)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # lotsAssociated = lots associated with this type of produc type

    def __str__(self):
        return (f"Product Type Name: {self.name}, Fractional Lots Allowed: {self.fractionalLotsAllowed}")