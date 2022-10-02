from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Recipe, Ingredient, User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


#RECIPES CRUD
class RecipeCreate(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['name']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RecipeUpdate(LoginRequiredMixin, UpdateView):
    model = Recipe
    fields = ['name']

class RecipeDelete(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = '/recipes/'


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def recipes_index(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/index.html', { 'recipes': recipes})

def recipes_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    # return render(request, 'recipes/detail.html', {'recipe': recipe, 'ingredients': ingredients_recipe_doesnt_have})







#INGREDIENTS CRUD

class IngredientList(LoginRequiredMixin, ListView):
    model = Ingredient

class IngredientDetail(LoginRequiredMixin, DetailView):
    model = Ingredient

class IngredientCreate(LoginRequiredMixin, CreateView):
    model = Ingredient
    fields = '__all__'

class IngredientUpdate(LoginRequiredMixin, UpdateView):
    model = Ingredient
    fields = '__all__'

class IngredientDelete(LoginRequiredMixin, DeleteView):
    model = Ingredient
    success_url = '/ingredients/'



def ingredients_index(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredients/index.html', { 'ingredients': ingredients})

def ingredients_detail(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    return render(request, 'ingredients/detail.html', { 'ingredients': ingredient})



def signup(request):
    error_message =""
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = "Invalid signup"


#ASSOCIATE AND UNASSOCIATE INGREDIENTS WITH RECIPES

def assoc_ingredient(request, recipe_id, ingredient_id):
    Recipe.objects.get(id = recipe_id).ingredients.add(ingredient_id)
    return redirect('detail', recipe_id = recipe_id)

def unassoc_ingredient(request, recipe_id, ingredient_id):
    Recipe.objects.get(id = recipe_id).ingredients.remove(ingredient_id)
    return redirect('detail', recipe_id = recipe_id)
