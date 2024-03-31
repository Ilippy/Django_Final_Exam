from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import Ingredient, Recipe, Image, Category
from .forms import IngredientForm, RecipeForm, ImageForm, RecipeIngredientForm, CategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin


# РЕЦЕПТЫ
class AddRecipeView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'jornapal_app/add_recipe.html'
    success_url = reverse_lazy('recipe_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = ImageForm()
        context['ingredient_form'] = RecipeIngredientForm()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()

        # Handling images
        images_data = self.request.POST.getlist('images')
        for img_data in images_data:
            image = Image.objects.create(url=img_data)
            self.object.images.add(image)

        # Handling ingredients
        ingredient_form = RecipeIngredientForm(self.request.POST)
        if ingredient_form.is_valid():
            ingredient_form.instance.recipe = self.object
            ingredient_form.save()

        return super().form_valid(form)


class RecipeListView(ListView):
    model = Recipe
    template_name = 'jornapal_app/home.html'
    context_object_name = 'recipes'


class MyRecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'jornapal_app/home.html'
    context_object_name = 'recipes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = context['recipes'].filter(author=self.request.user)
        return context


# Ингредиенты
class AddIngredientView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'jornapal_app/add_ingredient.html'


class IngredientListView(ListView):
    model = Ingredient
    form_class = IngredientForm
    context_object_name = 'ingredients'
    template_name = 'jornapal_app/ingedients_list.html'


# Категории
class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'jornapal_app/add_category.html'


class CategoryListView(ListView):
    model = Category
    form_class = CategoryForm
    context_object_name = 'categories'
    template_name = 'jornapal_app/categories_list.html'
