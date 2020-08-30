from django.db import models

class register(models.Model):
    email = models.CharField(max_length=200,default='')
    phoneno = models.CharField(max_length=20,default='')
    password = models.CharField(max_length=200,default='')
