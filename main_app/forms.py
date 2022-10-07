from dataclasses import field, fields
from email.policy import default
from pyexpat import model
from turtle import forward
from django import forms
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


class RecipeIngredients(forms.ModelForm):
    quantity = forms.IntegerField(required=False)
    class Meta:
        model = IngredientQuantity
        fields = ('ingredient',)
        widgets = {
            'ingredient': autocomplete.ModelSelect2(url='ingredient_autocomplete')
        }