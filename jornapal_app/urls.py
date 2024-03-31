from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='home'),
    path('recipes/add/', views.AddRecipeView.as_view(), name='add_recipe'),
    path('recipes/', views.IngredientListView.as_view(), name='ingredients'),
    path('ingredients/add/', views.AddIngredientView.as_view(), name='add_ingredient'),
    path('ingredients/', views.IngredientListView.as_view(), name='ingredients'),
    path('categories/add/', views.AddCategoryView.as_view(), name='add_category'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
]
