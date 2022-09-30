from unicodedata import name
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# class Recipe:
#     def __init__(self, name):
#         self.name = name

# recipes = [
#     Recipe('Quiche')
# ]

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def recipes_index(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/index.html', { 'recipes': recipes})

def recipes_detail(request, recipe_id):
    #select * from main_app_cat table where ID = to specific cat
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'recipes/detail.html', {'recipe': recipe})
