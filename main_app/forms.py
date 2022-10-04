from dataclasses import field
from django import forms

class ImageTextForm(forms.Form):
    image = forms.ImageField()