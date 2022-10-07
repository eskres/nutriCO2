from datetime import date
from email.mime import image
from email.policy import default
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django import forms  

# Create your models here.
# USER SPECIFIC INGREDIENTS
class CustomIngredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    co2e = models.FloatField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('custom_ingredient_detail', kwargs={'custom_ingredient_id': self.id})

# INGREDIENTS PROVIDED WITH CO2E/KG DATA
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    # description = models.CharField(max_length=100, default="")
    category = models.CharField(max_length=100, default="")
    # production_region = models.CharField(max_length=100, default="")
    co2e_min = models.FloatField()
    co2e_max = models.FloatField()
    co2e_med = models.FloatField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ingredient_detail', kwargs={'ingredient_id': self.id})

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to = 'main_app/static/uploads/', default="")
    # upload_image_of_ingredients = models.ImageField(upload_to = 'main_app/static/uploads/', default="")
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="")
    custom_ingredients = models.ManyToManyField(CustomIngredient, blank=True, through='IngredientQuantity')
    ingredients = models.ManyToManyField(Ingredient, blank=True, through='IngredientQuantity')
    method = models.CharField(max_length=1000, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    carbon_calculation = models.FloatField(default=False, null=True)
    # user id? 

    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs = {'recipe_id': self.id })

    def __str__(self):
        return self.name

class IngredientQuantity(models.Model):
    custom_ingredient = models.ForeignKey(CustomIngredient, null=True, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, null=True, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=False)


class User(models.Model):
    name = models.CharField(max_length=100)
    email = forms.EmailField(max_length=200, help_text='Required')  
    image = models.ImageField(upload_to = 'main_app/static/uploads/', default="")