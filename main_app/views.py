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
from django.template import loader
from .forms import ImageTextForm
import os
import requests
from django.utils.encoding import smart_bytes
import json
from django.contrib import messages

# Create your views here.


#RECIPES CRUD
class RecipeCreate(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RecipeUpdate(LoginRequiredMixin, UpdateView):
    model = Recipe
    fields = '__all__'

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

@login_required
def recipes_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'recipes/detail.html'),


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
            return redirect('/')
        else:
            error_message = "Invalid signup"

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

#ASSOCIATE AND UNASSOCIATE INGREDIENTS WITH RECIPES

def assoc_ingredient(request, recipe_id, ingredient_id):
    Recipe.objects.get(id = recipe_id).ingredients.add(ingredient_id)
    return redirect('detail', recipe_id = recipe_id)

def unassoc_ingredient(request, recipe_id, ingredient_id):
    Recipe.objects.get(id = recipe_id).ingredients.remove(ingredient_id)
    return redirect('detail', recipe_id = recipe_id)

#NAV BAR
def nav_view(request):
    return render(request, "nav.html")

#USER DETAILS
def user_detail(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'user/detail.html', { 'user': user})

#USER CRUD
class UserDetail(LoginRequiredMixin, DetailView):
    model = User
    fields = '__all__'

class UserCreate(LoginRequiredMixin, CreateView):
    model = User
    fields = '__all__'

class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = '__all__'

class UserDelete(LoginRequiredMixin, DeleteView):
    model = User
    success_url = '/'


def image_to_text(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ImageTextForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print('valid')
            
            result = {"lang": "en", "all_text": "2 tbsp extra-virgin olive oil,\nplus extra for drizzling\n300g sweet potato\n(unpeeled), cut into\n1cm cubes\n50g spring onions, trimmed\nand finely chopped\n4 eggs\n1 tsp dried thyme\n1 tsp dried oregano\n1 tsp sweet paprika\n\u00bd tsp cayenne pepper,\nplus extra to serve\n\u00bd tsp ground black pepper\n100g curly kale, stems\nremoved and leaves\nroughly chopped\n100g sweetcorn kernels\n(fresh, frozen or tinned)\n25g sunflower seeds, toasted\nand lightly crushed\nsea salt and freshly\nground black pepper\n\u314f\na\nM\nt\nF", "annotations": ["2", "tbsp", "extra", "-", "virgin", "olive", "oil", ",", "plus", "extra", "for", "drizzling", "300g", "sweet", "potato", "(", "unpeeled", ")", ",", "cut", "into", "1cm", "cubes", "50g", "spring", "onions", ",", "trimmed", "and", "finely", "chopped", "4", "eggs", "1", "tsp", "dried", "thyme", "1", "tsp", "dried", "oregano", "1", "tsp", "sweet", "paprika", "\u00bd", "tsp", "cayenne", "pepper", ",", "plus", "extra", "to", "serve", "\u00bd", "tsp", "ground", "black", "pepper", "100g", "curly", "kale", ",", "stems", "removed", "and", "leaves", "roughly", "chopped", "100g", "sweetcorn", "kernels", "(", "fresh", ",", "frozen", "or", "tinned", ")", "25g", "sunflower", "seeds", ",", "toasted", "and", "lightly", "crushed", "sea", "salt", "and", "freshly", "ground", "black", "pepper", "\u314f", "a", "M", "t", "F"]}

            # request.encoding = 'utf-8'
            # imageFile = request.FILES["image"]
            # receipt_image = imageFile.read()
            
            # url = "https://api.apilayer.com/image_to_text/upload"

            # payload = smart_bytes(receipt_image, encoding="utf-8", strings_only=False, errors="strict")
            # headers= {
            # "apikey": "OEgEEQl78jXRGAnGHnEugqPQWgMRU9C9"
            # }

            # response = requests.request("POST", url, headers=headers, data=payload)

            # status_code = response.status_code
            # result = response.text
            # print(status_code)

            # # # # MANIPULATE RESPONSE HERE
            # # # # DO CODE!!!!
            resultJSON = json.dumps(result)
            # print(resultJSON)
            return render(request, 'main_app/image_to_text.html', {'form': form, 'result': resultJSON})
            # return redirect('/')
    # if a GET (or any other method) we'll create a blank form
    else:
        print('not valid')
        form = ImageTextForm()
    return render(request, 'main_app/image_to_text.html', {'form': form})

    # os.getenv('APIKEY')
# FLASH MESSAGE FOR LOGOUT
# @require_http_methods(["GET", "POST"])
@login_required(login_url='/login', redirect_field_name='')
def do_logout(request):
    assert isinstance(request, HttpRequest)

    messages.add_message(request, messages.INFO, '{0} logged out.'.format(request.user))
    logout(request)
    return redirect('home')
