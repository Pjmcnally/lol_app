from django.db import models

# Create your models here.
class ChampStatic(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    descript = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, default='')
    version = models.CharField(max_length=500, default='')

class MastStatic(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    # descript = models.CharField(max_length=500, default='')
    tree = models.CharField(max_length=500, default='')
    ranks = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, default='')
    version = models.CharField(max_length=500, default='')

class RuneStatic(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    descript = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, default='')
    version = models.CharField(max_length=500, default='')

class SpellStatic(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    descript = models.CharField(max_length=500, default='')
    image = models.CharField(max_length=500, default='')
    version = models.CharField(max_length=500, default='')
