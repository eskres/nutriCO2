from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import IngredientQuantity, Recipe, CustomIngredient, Ingredient, User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from .forms import ImageTextForm, RecipeIngredients, RecipeCustomIngredients
import os
import requests
from django.utils.encoding import smart_bytes
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django import forms  
from .forms import NewUserForm
from dal import autocomplete
from django.core import serializers


# Create your views here.

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
        
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/")

	messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    email = forms.EmailField(max_length=200, help_text='Required')  
    template_name = "registration/signup.html" 

    class Meta:  
        model = User  
        fields = ('username', 'email', 'password1', 'password2') 

class SignupView(UserCreationForm):  
    email = forms.EmailField(max_length=200, help_text='Required')  
    
    class Meta:  
        model = User  
        fields = ('username', 'email', 'password1', 'password2')  

class PasswordChange(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/password_change.html"

class PasswordReset(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/password_reset.html"

#RECIPES CRUD
class RecipeCreate(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['name', 'image', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RecipeUpdate(LoginRequiredMixin, UpdateView):
    model = Recipe
    fields = ['name', 'image', 'description', 'category', 'method', 'public']

class RecipeDelete(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = '/recipes/'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# ---------------------------------------------------------------- #
#ADD RECIPE USER MESSAGES

@login_required
def addRecipe(request):
    if request.method == "POST":
        form = RecipeCreate(request.POST)

    form = RecipeCreate()
    context = {'form': form}
    return render(request, 'recipes/index.html', context)

def recipes_index(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/index.html', { 'recipes': recipes})
# ---------------------------------------------------------------- #

#RECIPE DETAIL
@login_required
def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    ingqty = IngredientQuantity.objects.filter(recipe_id = recipe_id)
    form1 = RecipeIngredients(request.POST)
    form2 = RecipeCustomIngredients(request.POST)
    return render(request, 'recipes/detail.html', { 'recipe': recipe, 'form1': form1, 'form2': form2, 'ingqty': ingqty})

# ---------------------------------------------------------------- #

#ASSOCIATE AND UNASSOCIATE INGREDIENTS WITH RECIPES

def assoc_ingredient(request, recipe_id):
    Recipe.objects.get(id = recipe_id).ingredients.add(request.POST['ingredient'])
    row = IngredientQuantity.objects.get(recipe_id = recipe_id, ingredient_id = request.POST['ingredient'])
    row.quantity = request.POST['quantity']
    row.save()
    return redirect('recipe_detail', recipe_id = recipe_id)

def unassoc_ingredient(request, recipe_id):
    Recipe.objects.get(id = recipe_id).ingredients.remove(request.POST['ingredient'])
    return redirect('recipe_detail', recipe_id = recipe_id)
# ---------------------------------------------------------------- #

#ASSOCIATE AND UNASSOCIATE CUSTOM_INGREDIENTS WITH RECIPES

def assoc_custom_ingredient(request, recipe_id):
    Recipe.objects.get(id = recipe_id).custom_ingredients.add(request.POST['custom_ingredient'])
    row = IngredientQuantity.objects.get(recipe_id = recipe_id, custom_ingredient_id = request.POST['custom_ingredient'])
    row.quantity = request.POST['quantity']
    row.save()
    return redirect('recipe_detail', recipe_id = recipe_id)

def unassoc_custom_ingredient(request, recipe_id):
    Recipe.objects.get(id = recipe_id).custom_ingredients.remove(request.POST['custom_ingredient'])
    return redirect('recipe_detail', recipe_id = recipe_id)
# ---------------------------------------------------------------- #

#Calculate Carbon emmissions
def carbon_calculation(request, recipe_id):
    qty = IngredientQuantity.objects.filter(recipe_id = recipe_id)
    count = 0
    for q in qty:
        if q.quantity is not None and q.ingredient is not None:
            co2 = Ingredient.objects.get(id = q.ingredient.id).co2e_med
            count += (co2 * q.quantity)
            print(count)
        elif q.quantity is not None and q.custom_ingredient is not None:
            co2 = CustomIngredient.objects.get(id = q.custom_ingredient.id).co2e
            count += (co2 * q.quantity)
            print(count)
    recipe = Recipe.objects.get(id = recipe_id)
    recipe.carbon_calculation = count
    recipe.save()
    return redirect('recipe_detail', recipe_id = recipe_id)
# ---------------------------------------------------------------- #
# POST METHOD FROM IMAGE
def update_method(request, recipe_id):
    recipe = Recipe.objects.get(id = recipe_id)
    recipe.method = request.POST['text']
    recipe.save()
    return redirect('recipe_detail', recipe_id = recipe_id)

# ---------------------------------------------------------------- #

# NEW NEW NEW
@login_required
def recipe_delete(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    messages.success(request, 'Recipe deleted.')
    return render(request, 'recipes/index.html', { 'success': 'Recipe deleted'})


class CustomIngredientCreate(LoginRequiredMixin, CreateView):
    model = CustomIngredient
    fields = ['name', 'description', 'co2e']
    template_name='custom_ingredients/form.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CustomIngredientUpdate(LoginRequiredMixin, UpdateView):
    model = CustomIngredient
    fields = ['name', 'description', 'co2e']
    template_name='custom_ingredients/form.html'

class CustomIngredientDelete(LoginRequiredMixin, DeleteView):
    model = CustomIngredient
    template_name='custom_ingredients/confirm_delete.html'
    success_url = '/custom_ingredients/'

# CUSTOM INGREDIENTS VIEWS
def custom_ingredients_index(request):
    custom_ingredients = CustomIngredient.objects.all()
    return render(request, 'custom_ingredients/index.html', { 'custom_ingredients': custom_ingredients})

def custom_ingredient_detail(request, custom_ingredient_id):
    custom_ingredient = CustomIngredient.objects.get(id=custom_ingredient_id)
    return render(request, 'custom_ingredients/detail.html', { 'custom_ingredient': custom_ingredient})

# ! OLD SIGN UP METHOD
#SIGN UP USER MESSAGES
# def signup(request):
#     error_message =""
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)

#         if form.is_valid():
#             user = form.save()
#             login(request,user)
#             messages.success(request, 'Your registration was successful')
#             return redirect('/')
    
#         else:
#             messages.error(request, 'Your registration was unsuccessful; please try again')
#             return redirect('/')  

#     form = UserCreationForm()
#     context = {'form': form, 'error_message': error_message}
#     return render(request, 'registration/signup.html', context)

#LOGOUT USER MESSAGES
@login_required
def logout(request):
    if request.method == "POST":
        logout.is_valid()
        messages.success(request, 'You have been logged out succesfully')
        return render (request, 'home.html', {'successs': 'You have been logged out succesfully'})

#LOGIN USER MESSAGES (this one works)
def log_in(request):
    if request.method == "POST":

        if log_in.is_valid():
            messages.success(request, 'You have been logged in')
            return render(request,'home,html', {'success': 'You have been logged in'})

            # next field; create in html 

        else: 
            messages.error(request, 'We have been unable to log you in; please try again')
            return render(request, 'registration/login.html', { 'error': 'We have been unable to log you in; please try again'})


# @login_required
# def password_change(request):
#     user = request.user
#     if request.method == 'POST':
#         form = SetPasswordForm(user, request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Your password has been changed")
#             return redirect('login')
#         else:
#             for error in list(form.errors.values()):
#                 messages.error(request, error)

#     form = SetPasswordForm(user)
#     return render(request, 'password_reset_confirm.html', {'form': form})


#NAV BAR
def nav_view(request):
    return render(request, "nav.html")


#USER CRUD
class UserDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name='user/detail.html'
    
class UserCreate(LoginRequiredMixin, CreateView):
    model = User
    fields = '__all__'

class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name='user/update.html'
    fields = '__all__'

class UserDelete(LoginRequiredMixin, DeleteView):
    model = User
    template_name='user/user_confirm_delete.html'
    success_url = '/'

#USER DETAILS

# @login_required
# def user_detail(request, user_id):
#     user = User.objects.get(id=user_id)
#     return render(request, 'user/detail.html', { 'user': user})

# @login_required
# def user_profile(request, user_id):
#     user = User.objects.get(id=user_id)
#     return render(request, 'user/profile.html', { 'user': user})

#IMAGE TO TEXT API (100% Einar's work))
def method_image_to_text(request, recipe_id):
    recipe = Recipe.objects.get(id = recipe_id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ImageTextForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print('valid')

            request.encoding = 'utf-8'
            imageFile = request.FILES["image"]
            receipt_image = imageFile.read()
            
            url = "https://api.apilayer.com/image_to_text/upload"

            payload = smart_bytes(receipt_image, encoding="utf-8", strings_only=False, errors="strict")
            headers= {
            # "apikey": os.getenv('APIKEY')
            "apikey": 'j5bBeYtVScafh6Q3BmKwgobGfvawvsBZ'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            status_code = response.status_code
            result = response.text
            print(result)

            # # # # MANIPULATE RESPONSE HERE
            # # # # DO CODE!!!!
            resultJSON = json.dumps(result)
            # print(resultJSON)
            return render(request, 'main_app/image_to_text.html', {'form': form, 'result': result, 'recipe': recipe})
            # return redirect('/')
        else:
            print('not valid')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ImageTextForm()
    return render(request, 'main_app/image_to_text.html', {'form': form, 'recipe': recipe})


def calculate_nutrition(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ImageTextForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print('valid')

            url = "https://api.spoonacular.com/recipes/analyze"

            # Prepare payload here as JSON object
            recipe = ""

            headers= {
            "apikey": os.getenv('SPOONACULAR')
            }

            response = requests.request("POST", url, headers=headers, params=recipe)

            print(response)

            # # # # MANIPULATE RESPONSE HERE
            # return redirect('/')
        else:
            print('not valid')
    # if a GET (or any other method) we'll create a blank form
    else:
        return redirect('recipes/create/')

# ! OLD SIGN UP METHOD
#SIGN UP USER MESSAGES
# def signup(request):
#     error_message =""
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)

#         if form.is_valid():
#             user = form.save()
#             login(request,user)
#             messages.success(request, 'Your registration was successful')
#             return redirect('/')
#         else:
#             messages.error(request, 'Your registration was unsuccessful; please try again')
#             return redirect('/')  

#     form = UserCreationForm()
#     context = {'form': form, 'error_message': error_message}
#     return render(request, 'registration/signup.html', context)

class IngredientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Ingredient.objects.none()

        qs = Ingredient.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
            print(qs)
        return qs
    def get_result_value(self, result):
            print(result)
            return result.pk   

class CustomIngredientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return CustomIngredient.objects.none()

        qs = CustomIngredient.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

#GET RECIPE AS JSON
#--------------------------------------------------------------------------------#
def get_recipe(request, recipe_id):
    # recipe = serializers.serialize("json", Recipe.objects.filter(id = recipe_id))
    # qty = IngredientQuantity.objects.filter(recipe_id=recipe_id).values()
    #THIS ONE qty = IngredientQuantity.objects.filter(recipe_id = recipe_id).values('ingredient')
    # print('!!',qty)
    # print('!',recipe)

    return redirect('recipe_detail', recipe_id = recipe_id)