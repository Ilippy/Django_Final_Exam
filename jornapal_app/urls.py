from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='home'),
    path('recipes/add/', views.AddRecipeView.as_view(), name='add_recipe'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/<int:pk>/update/', views.RecipeUpdateView.as_view(), name='recipe_update'),
    path('ingredients/add/', views.AddIngredientView.as_view(), name='add_ingredient'),
    path('ingredients/', views.IngredientListView.as_view(), name='ingredients'),
    path('ingredients/<int:pk>/', views.IngredientDetailView.as_view(), name='ingredient_detail'),
    path('categories/add/', views.AddCategoryView.as_view(), name='add_category'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
]
