from django.db import models

# Create your models here.
class Champion(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    descript = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, default='')
    version = models.CharField(max_length=500, default='')

class Mastery(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    # descript = models.CharField(max_length=500, default='')
    tree = models.CharField(max_length=500, default='')
    ranks = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, default='')
    version = models.CharField(max_length=500, default='')

class Rune(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    descript = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, default='')
    version = models.CharField(max_length=500, default='')

class Spell(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    descript = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, default='')
    version = models.CharField(max_length=500, default='')