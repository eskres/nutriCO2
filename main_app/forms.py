from dataclasses import field, fields
from email.policy import default
from pyexpat import model
from turtle import forward
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from dal import autocomplete
from.models import IngredientQuantity
from .choices import INGREDIENT_CHOICES

class ImageTextForm(forms.Form):
    image = forms.ImageField(required=False)
    text = forms.CharField(label='Text Response', max_length=1000, required=False, widget=forms.Textarea)

class RecipeCustomIngredients(forms.ModelForm):
    quantity = forms.IntegerField(required=False)
    class Meta:
        model = IngredientQuantity
        fields = ('custom_ingredient',)
        widgets = {
            'custom_ingredient': autocomplete.ModelSelect2(url='custom_ingredient_autocomplete')
        }


class RecipeIngredients(forms.Form):
    ingredient = forms.CharField(max_length=100, required=False)
    custom_ingredient = forms.CharField(max_length=100, required=False)

# # USER SPECIFIC INGREDIENTS
# class CustomIngredient(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.CharField(max_length=100, default="")

# # INGREDIENTS PROVIDED WITH CO2E/KG DATA
# class Ingredient(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.CharField(max_length=100, default="")
#     category = models.CharField(max_length=100, default="")
#     production_region = models.CharField(max_length=100, default="")
#     co2e_min = models.FloatField()
#     co2e_max = models.FloatField()
#     co2e_med = models.FloatField()

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse('ingredients_detail', kwargs={'pk': self.id})

# class Recipe(models.Model):
#     name = models.CharField(max_length=100)
#     image = models.ImageField(upload_to = 'main_app/static/uploads/', default="")
#     upload_image_of_ingredients = models.ImageField(upload_to = 'main_app/static/uploads/', default="")
#     description = models.CharField(max_length=100)
#     category = models.CharField(max_length=100, default="")
#     custom_ingredients = models.ManyToManyField(CustomIngredient, through='IngredientQuantity')
#     ingredients = models.ManyToManyField(Ingredient, through='IngredientQuantity')
#     method = models.CharField(max_length=300, default="")
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     public = models.BooleanField(default=False)
#     # user id? 

#     def get_absolute_url(self):
#         return reverse('recipe_detail', kwargs = {'recipe_id': self.id })

#     def __str__(self):
#         return self.name

# class IngredientQuantity(models.Model):
#     custom_ingredient = models.ForeignKey(CustomIngredient, on_delete=models.CASCADE)
#     ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=False)

#     def __str__(self):
#         return "{}_{}".format(self.sandwich.__str__(), self.sauce.__str__())

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
class RecipeIngredients(forms.ModelForm):
    quantity = forms.IntegerField(required=False)
    class Meta:
        model = IngredientQuantity
        fields = ('ingredient',)
        widgets = {
            'ingredient': autocomplete.ModelSelect2(url='ingredient_autocomplete')
        }
