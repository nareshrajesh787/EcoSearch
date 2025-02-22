from django.db import models

# Create your models here.
class addressModel(models.Model):
  address = models.CharField(max_length=100)