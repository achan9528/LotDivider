from django.db import models
from .models import *

# Create your models here.
class Portfolio(model.Model):
    number = models.CharField(max_length=50)
    accountNumber = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    # holdings = holdings
    # lots = tax lots in the portfolio.
    # we don't necessarily need a holdings model because we can just sort and group the tax lots

class Holding(model.Model):
    ticker = models.CharField(max_length=50)
    cusip = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2)
    units = models.DecimalField(decimal_places=8)
    totalCost = models.DecimalField(decimal_places=2)
    
    productType = models.ForeignKey(ProductType, related_name="holdingsAssociated", on_delete=models.CASCADE)

class TaxLot(model.Model):
    number = models.CharField(max_length=50)
    ticker = models.CharField(max_length=50)
    cusip = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    units = models.DecimalField(decimal_places=8)
    totalFederalCost = models.DecimalField(decimal_places=2)
    totalStateCost = models.DecimalField(decimal_places=2)
    acquisitionDate = models.DateTimeField(auto_now=False, auto_now_add=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    portfolio = models.models.ForeignKey(Portfolio, related_name="lots", on_delete=models.CASCADE)
    productType = models.ForeignKey(ProductType, related_name="lotsAssociated", on_delete=models.CASCADE)

    def __str__(self):
        print f"Lot Number: {self.number}, Ticker: {self.ticker}, Units: {self.units}"

class ProductType(model.Model):
    name = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    #lotsAssociated = lots associated with this product type

    def __str__(self):
        print f"Product Type Name: {self.name}"