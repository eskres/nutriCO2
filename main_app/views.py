from unicodedata import name
from django.shortcuts import render
from django.http import HttpResponse
from .models import Recipe, Ingredient, User

# Create your views here.



def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def recipes_index(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/index.html', { 'recipes': recipes})

def recipes_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'recipes/detail.html', {'recipe': recipe})

def ingredients_index(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredients/index.html', { 'ingredients': ingredients})

def ingredients_detail(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    return render(request, 'ingredients/detail.html', { 'ingredients': ingredient})
