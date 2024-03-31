from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='home'),
    path('ingredients/add', views.AddIngredientView.as_view(), name='add_ingredient'),
    path('recipes/add', views.AddRecipeView.as_view(), name='add_recipe'),
]
