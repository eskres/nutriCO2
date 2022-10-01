from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to = 'main_app/static/uploads/', default="")
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="")
    ingredients = models.CharField(max_length=300, default="")
    # method coule be potential image upload?
    method = models.CharField(max_length=300, default="")
    # need to find default value for portions
    # portions = models.SmallIntegerField(default="4")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # option to make public or keep private?

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default="")
    allergy = models.CharField(max_length=100, default="")

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    image = models.ImageField(upload_to = 'main_app/static/uploads/', default="")

# USER SPECIFIC
class CustomIngredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default="")
    allergy = models.CharField(max_length=100)

    




