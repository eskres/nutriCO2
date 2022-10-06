
from django.urls import path
from . import views
from .views import nav_view, image_to_text
from .views import SignUpView


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),


    #RECIPES
    path('recipes/', views.recipes_index, name='recipes_index'),
    path('recipes/<int:recipe_id>', views.recipe_detail, name='recipe_detail'),
    path('recipes/create/', views.RecipeCreate.as_view(), name='recipes_create'),
    path('recipes/<int:pk>/update/', views.RecipeUpdate.as_view(), name='recipe_update'),
    path('recipes/<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipe_delete'),

    #CUSTOM INGREDIENTS
    path('custom_ingredients/', views.CustomIngredientList.as_view(), name='custom_ingredients_index'),
    path('custom_ingredients/<int:ingredient_id>', views.custom_ingredients_detail, name='ingredient_detail'),
    path('custom_ingredients/create/', views.CustomIngredientCreate.as_view(), name='custom_ingredients_create'),
    path('custom_ingredients/<int:pk>/update', views.CustomIngredientUpdate.as_view(), name='custom_ingredients_update'),
    path('custom_ingredients/<int:pk>/delete', views.CustomIngredientDelete.as_view(), name='custom_ingredients_delete'),


    #ASSOCIATE INGREDIENT
    path('recipes/<int:recipe_id>/assoc_ingredient/<int:ingredient_id>', views.assoc_ingredient, name="assoc_ingredient"),
    #UNASSOCIATE INGREDIENT
    path('recipes/<int:recipe_id>/assoc_ingredient/<int:ingredient_id>', views.unassoc_ingredient, name="unassoc_ingredient"),


    #USER
    path('signup/', SignUpView.as_view(), name='signup'),
    path('user/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
    path('user/<int:pk>/update', views.UserUpdate.as_view(), name='user_update'),
    path('user/<int:pk>/delete', views.UserDelete.as_view(), name='user_delete'),
    # path("password_reset/", views.PasswordReset.as_view(), name="password_reset"),

    # path('recipes/<int:pk>/update/', views.RecipeUpdate.as_view(), name='recipe_update'),
    # path('recipes/<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipe_delete'),
    
    #LOGIN
    path('accounts/login', views.log_in, name='log_in'),
    path('accounts/logout', views.logout,name='logout'),


    # NAV
    path('', nav_view),

    # IMAGE FORM
    path('form/', views.image_to_text, name='form'),

    # RECIPE FORM STEP 1
    path('recipes/step1', views.recipe_ingredients, name='step1'),
]