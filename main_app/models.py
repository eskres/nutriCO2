from django.db import models

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=300)
    image = models.ImageField(upload_to = 'main_app/static/uploads/', default="")

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    




