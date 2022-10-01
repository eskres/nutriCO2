
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('recipes/', views.recipes_index, name='index'),
    path('recipes/<int:recipe_id>', views.recipes_detail, name='detail'),
    path('ingredients/', views.ingredients_index, name='index'),
    path('ingredients/<int:ingredient_id>', views.ingredients_detail, name='detail')

]