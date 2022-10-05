
from django.urls import path
from . import views
from .views import nav_view, image_to_text

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    #RECIPES
    path('recipes/', views.recipes_index, name='recipes_index'),
    path('recipes/<int:recipe_id>', views.recipe_detail, name='recipe_detail'),
    path('recipes/create/', views.RecipeCreate.as_view(), name='recipes_create'),
    path('recipes/<int:pk>/update/', views.RecipeUpdate.as_view(), name='recipe_update'),
    path('recipes/<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipe_delete'),

    #INGREDIENTS
    path('ingredients/', views.ingredients_index, name='ingredients_index'),
    path('ingredients/<int:ingredient_id>', views.ingredients_detail, name='ingredient_detail'),
    path('ingredients/create/', views.IngredientCreate.as_view(), name='ingredients_create'),
    path('ingredients/<int:pk>/update', views.IngredientUpdate.as_view(), name='ingredients_update'),
    path('ingredients/<int:pk>/delete', views.IngredientDelete.as_view(), name='ingredients_delete'),


    #ASSOCIATE INGREDIENT
    path('recipes/<int:recipe_id>/assoc_ingredient/<int:ingredient_id>', views.assoc_ingredient, name="assoc_ingredient"),
    #UNASSOCIATE INGREDIENT
    path('recipes/<int:recipe_id>/assoc_ingredient/<int:ingredient_id>', views.unassoc_ingredient, name="unassoc_ingredient"),


    #USER
    path('accounts/signup/', views.signup, name='signup'),
    # path('user/<int:user_id>', views.user_detail, name='user_detail'),
    path('user/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
    path('user/<int:pk>/update', views.UserUpdate.as_view(), name='user_update'),
    path('user/<int:pk>/delete', views.UserDelete.as_view(), name='user_delete'),
    
    #LOGIN
    path('accounts/login', views.login, name='login'),

    # NAV
    path('', nav_view),

    # IMAGE FORM
    path('form/', views.image_to_text, name='form'),
]