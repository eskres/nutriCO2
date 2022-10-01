
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    #RECIPES
    path('recipes/', views.recipes_index, name='index'),
    path('recipes/<int:recipe_id>', views.recipes_detail, name='detail'),
    path('recipes/create/', views.RecipeCreate.as_view(), name='recipes_create'),
    path('recipes/<int:pk>/update/', views.RecipeUpdate.as_view(), name='recipes_update'),
    path('recipes/<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipes_delete'),

    #INGREDIENTS
    path('ingredients/', views.ingredients_index, name='index'),
    path('ingredients/<int:ingredient_id>', views.ingredients_detail, name='detail'),
    path('ingredients/create/', views.IngredientCreate.as_view(), name='ingredients_create'),
    path('ingredients/<int:pk>/update', views.IngredientUpdate.as_view(), name='ingredients_update'),
    path('ingredients/<int:pk>/delete', views.IngredientDelete.as_view(), name='ingredients_delete'),


    #ASSOCIATE INGREDIENT WITH CAT
    path('recipes/<int:recipe_id>/assoc_ingredient/<int:ingredient_id>', views.assoc_ingredient, name="assoc_ingredient"),
    #UNASSOCIATE INGREDIENT FROM CAT
    path('recipes/<int:recipe_id>/assoc_ingredient/<int:ingredient_id>', views.unassoc_ingredient, name="unassoc_ingredient"),


    #SIGN UP
    path('accounts/signup/', views.signup, name='signup')

]