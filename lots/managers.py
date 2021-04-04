# Model Managers
from django.db import models
import re

class UserManager(models.Manager):
    def registrationValidator(self, postData):
        errors = {}
        EMAIL_REGREX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['name']) < 2:
            errors['name'] = "First Name should be at least 2 characters!"
        if len(postData['alias']) < 2:
            errors['alias'] = "Alias should be at least 2 characters!"
        if not EMAIL_REGREX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['email'] = "Invalid email - user already exists!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        if postData['password'] != postData['passwordConfirm']:
            errors['passwordConfirm'] = "Password does not match!"
        return errors
        
    def loginValidator(self, postData):
        errors = {}
        EMAIL_REGREX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGREX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(User.objects.filter(email=postData['email'])) < 1:
            errors['email'] = "Invalid email address - user does not exist. Please register!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        return errors