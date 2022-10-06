from dataclasses import field
from django import forms

class ImageTextForm(forms.Form):
    image = forms.ImageField(required=False)
    text = forms.CharField(label='Text Response', max_length=1000, required=False)


class RecipeIngredients(forms.Form):
    ingredient = forms.CharField(max_length=100, required=False)
    custom_ingredient = forms.CharField(max_length=100, required=False)