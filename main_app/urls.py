
from django.urls import path, re_path
from . import views
from .views import nav_view, method_image_to_text, IngredientAutocomplete, CustomIngredientAutocomplete
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
    path('recipes/<int:recipe_id>/carbon', views.carbon_calculation, name='carbon_calculation'),
    path('recipes/<int:recipe_id>/method/image_to_text/', views.method_image_to_text, name='method_image_to_text'),
    path('recipes/<int:recipe_id>/method/update/', views.update_method, name='update_method'),


    #CUSTOM INGREDIENTS
    path('custom_ingredients/', views.custom_ingredients_index, name='custom_ingredients_index'),
    path('custom_ingredients/<int:custom_ingredient_id>', views.custom_ingredient_detail, name='custom_ingredient_detail'),
    path('custom_ingredients/create/', views.CustomIngredientCreate.as_view(), name='custom_ingredients_create'),
    path('custom_ingredients/<int:pk>/update', views.CustomIngredientUpdate.as_view(), name='custom_ingredient_update'),
    path('custom_ingredients/<int:pk>/delete', views.CustomIngredientDelete.as_view(), name='custom_ingredient_delete'),
    #ASSOCIATE CUSTOM_INGREDIENT
    path('recipes/<int:recipe_id>/assoc_custom_ingredient/', views.assoc_custom_ingredient, name="assoc_custom_ingredient"),
    #UNASSOCIATE CUSTOM_INGREDIENT
    path('recipes/<int:recipe_id>/unassoc_custom_ingredient/', views.unassoc_custom_ingredient, name="unassoc_custom_ingredient"),


    #ASSOCIATE INGREDIENT
    path('recipes/<int:recipe_id>/assoc_ingredient/', views.assoc_ingredient, name="assoc_ingredient"),
    #UNASSOCIATE INGREDIENT
    path('recipes/<int:recipe_id>unassoc_ingredient/', views.unassoc_ingredient, name="unassoc_ingredient"),


    #USER
    path('register/', views.register_request, name='register'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('user/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
    path('user/<int:pk>/update', views.UserUpdate.as_view(), name='user_update'),
    path('user/<int:pk>/delete', views.UserDelete.as_view(), name='user_delete'),
    # path("password_change/", views.Password_Change.as_view(), name='password_change'),
    # path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),


    # path('recipes/<int:pk>/update/', views.RecipeUpdate.as_view(), name='recipe_update'),
    # path('recipes/<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipe_delete'),
    
    #LOGIN
    # path('accounts/login', views.log_in, name='log_in'),
    # path('accounts/logout', views.logout,name='logout'),


    # NAV
    path('', nav_view),

    # IMAGE FORM
    
    # JSON RECIPE
    path('json/<int:recipe_id>', views.get_recipe, name='json'),


    

    re_path(r'^ingredient-autocomplete/$', IngredientAutocomplete.as_view(), name='ingredient_autocomplete'),
    re_path(r'^custom_ingredient-autocomplete/$', CustomIngredientAutocomplete.as_view(), name='custom_ingredient_autocomplete'),
]