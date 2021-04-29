from django.db import models
import uuid

class User(models.Model):
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