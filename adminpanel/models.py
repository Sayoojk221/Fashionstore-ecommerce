from django.db import models
from django.utils import timezone

class Register(models.Model):
    email = models.CharField(max_length=50,default='')
    password = models.CharField(max_length=200,default='')

class ProductCommon(models.Model):
    productid = models.CharField(max_length=200,default='')
    title = models.CharField(max_length=200,default='')
    gender = models.CharField(max_length=200,default='')
    description = models.CharField(max_length=1000,default='')
    additionaldescription = models.CharField(max_length=2000,default='')
    shippingandreturns = models.CharField(max_length=500,default='')
    createddate = models.DateTimeField(default=timezone.now)

class ProductColor(models.Model):
    productcommon = models.ForeignKey(ProductCommon,on_delete=models.CASCADE)
    colorid = models.CharField(max_length=200,default='')
    picture = models.ImageField(upload_to='product',default='')
    picture2 = models.ImageField(upload_to='product',default='')
    picture3 = models.ImageField(upload_to='product',default='')
    color = models.CharField(max_length=200,default='')

class ProductSize(models.Model):
    productcolor = models.ForeignKey(ProductColor,on_delete=models.CASCADE)
    sizeid = models.CharField(max_length=200,default='')
    size = models.CharField(max_length=200,default='')
    quantity = models.CharField(max_length=200,default='')
    price = models.CharField(max_length=200,default='')
