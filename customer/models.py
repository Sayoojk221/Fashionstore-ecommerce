from django.db import models
from adminpanel.models import *

class register(models.Model):
    email = models.CharField(max_length=200,default='')
    phoneno = models.CharField(max_length=20,default='')
    password = models.CharField(max_length=200,default='')

class CustomersUniqueId(models.Model):
    encryptedid = models.CharField(max_length=200,default='')

class CartList(models.Model):
    productid = models.ForeignKey(ProductSize,on_delete=models.CASCADE)
    encryptedid = models.CharField(max_length=200,default='')

