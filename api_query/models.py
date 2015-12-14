from django.db import models

# Create your models here.
class Champion(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=30, default='')
    key = models.CharField(max_length=30, default='')

    
