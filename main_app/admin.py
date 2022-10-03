from django.contrib import admin
from .models import Ingredient, Recipe, User

# Register your models here.

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(User)

