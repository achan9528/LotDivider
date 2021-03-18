from django.db import models
from .models import *
import uuid

# Create your models here.
# class UserManager(models.Manager):
#     def registrationValidator(self, postData):
#         errors = {}
#         EMAIL_REGREX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#         if len(postData['name']) < 2:
#             errors['name'] = "First Name should be at least 2 characters!"
#         if len(postData['alias']) < 2:
#             errors['alias'] = "Alias should be at least 2 characters!"
#         if not EMAIL_REGREX.match(postData['email']):
#             errors['email'] = "Invalid email address!"
#         if len(User.objects.filter(email=postData['email'])) > 0:
#             errors['email'] = "Invalid email - user already exists!"
#         if len(postData['password']) < 8:
#             errors['password'] = "Password must be at least 8 characters!"
#         if postData['password'] != postData['passwordConfirm']:
#             errors['passwordConfirm'] = "Password does not match!"
#         return errors
        
#     def loginValidator(self, postData):
#         errors = {}
#         EMAIL_REGREX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#         if not EMAIL_REGREX.match(postData['email']):
#             errors['email'] = "Invalid email address!"
#         if len(User.objects.filter(email=postData['email'])) < 1:
#             errors['email'] = "Invalid email address - user does not exist. Please register!"
#         if len(postData['password']) < 8:
#             errors['password'] = "Password must be at least 8 characters!"
#         return errors

# class User(models.Model):
#     name = models.CharField(max_length=255)
#     alias = models.CharField(max_length=255)
#     email = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)
#     createdAt = models.DateTimeField(auto_now_add=True)
#     updatedAt = models.DateTimeField(auto_now=True)
#     objects = UserManager()

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    fractionalLotsAllowed = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    #lotsAssociated = lots associated with this product type

    def __str__(self):
        return (f"Product Type Name: {self.name}, Fractional Lots Allowed: {self.fractionalLotsAllowed}")

class Security(models.Model):
    ticker = models.CharField(max_length=50)
    cusip = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    productType = models.ForeignKey(ProductType, related_name="relatedSecurities", on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"Security Ticker {self.ticker}, Security Name: {self.name}, Security Product Type: {self.productType.name}")

class Portfolio(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50, default=uuid.uuid4)
    # owner = models.ForeignKey(User, related_name="relatedPortfolios", on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"Portfolio Name: {self.name}, Portfolio Number: {self.number}")

class Account(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50, default=uuid.uuid4)
    portfolio = models.ForeignKey(Portfolio, related_name="accounts", on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    # holdings = holdings
    
    def __str__(self):
        return (f"Account Name {self.name}, Account Number: {self.number}")

class Holding(models.Model):
    security = models.ForeignKey(Security, related_name="relatedHoldings", on_delete=models.CASCADE)
    account = models.ForeignKey(Account, related_name="holdings", on_delete=models.CASCADE)
    
    #taxLots = tax lots associated with the holding

    def __str__(self):
        return (f"Holding: {self.security.name}, Account Name: {self.account.name}")

class TaxLot(models.Model):
    number = models.CharField(max_length=50, default=uuid.uuid4)
    holding = models.ForeignKey(Holding, related_name="taxLots", on_delete=models.CASCADE)
    units = models.DecimalField(max_digits=20, decimal_places=4)
    totalFederalCost = models.DecimalField(max_digits=20, decimal_places=2)
    totalStateCost = models.DecimalField(max_digits=20, decimal_places=2)
    acquisitionDate = models.DateTimeField(auto_now_add=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # portfolio = models.ForeignKey(Portfolio, related_name="lots", on_delete=models.CASCADE)
    # productType = models.ForeignKey(ProductType, related_name="lotsAssociated", on_delete=models.CASCADE)

    def __str__(self):
        return (f"Lot Number: {self.number}, Ticker: {self.holding.security.ticker}, Units: {self.units}, Cost: {self.totalFederalCost}")

