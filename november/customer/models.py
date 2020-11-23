from django.db import models

# Create your models here.

class menu(models.Model):
    typename = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    price = models.IntegerField()
