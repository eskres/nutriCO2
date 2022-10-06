from datetime import date
from email.mime import image
from email.policy import default
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
# USER SPECIFIC INGREDIENTS
class CustomIngredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default="")

# INGREDIENTS PROVIDED WITH CO2E/KG DATA
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default="")
    category = models.CharField(max_length=100, default="")
    production_region = models.CharField(max_length=100, default="")
    co2e_min = models.FloatField()
    co2e_max = models.FloatField()
    co2e_med = models.FloatField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ingredients_detail', kwargs={'pk': self.id})

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to = 'main_app/static/uploads/', default="")
    upload_image_of_ingredients = models.ImageField(upload_to = 'main_app/static/uploads/', default="")
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="")
    custom_ingredients = models.ManyToManyField(CustomIngredient)
    ingredients = models.ManyToManyField(Ingredient)
    method = models.CharField(max_length=300, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    # user id? 


    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs = {'recipe_id': self.id })

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    image = models.ImageField(upload_to = 'main_app/static/uploads/', default="")