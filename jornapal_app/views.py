from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from .models import Ingredient, Recipe, Image, Category, RecipeIngredient
from .forms import IngredientForm, RecipeForm, RecipeIngredientForm, CategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from uuid import uuid4


# РЕЦЕПТЫ
class AddRecipeView(LoginRequiredMixin, CreateView):
    form_class = RecipeForm
    template_name = 'jornapal_app/add_recipe.html'
    success_url = reverse_lazy('home')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['ingredient_form'] = RecipeIngredientForm()
    #     return context

    # def form_invalid(self, form):
    #     print(form)
    #     return super().form_invalid(form)

    def form_valid(self, form):
        print('aaaaaa')
        form.instance.author = self.request.user
        self.object = form.save()

        # Handling images
        images = self.request.FILES.getlist('photo')
        for image_data in images:
            extension = image_data.name.split('.')[-1]
            filename = f'{uuid4()}.{extension}'
            # image_data = Image.objects.create(url=image_data)
            fs = FileSystemStorage()
            fs.save(filename, image_data)
            image = Image.objects.create(url=filename)
            self.object.images.add(image)

        # Handling ingredients
        ingredients_data = self.request.POST.getlist('ingredient_name')
        amounts_data = self.request.POST.getlist('amount')
        print(ingredients_data)
        print(amounts_data)

        for i in range(len(ingredients_data)):
            ingredient_name = ingredients_data[i].strip().lower()
            amount = amounts_data[i]
            ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)

            # Создание RecipeIngredient
            RecipeIngredient.objects.create(
                recipe=self.object,
                ingredient=ingredient,
                amount=amount,
            )

        # Категории
        categories = self.request.POST.getlist('category_name')
        for category_data in categories:
            category, _ = Category.objects.get_or_create(name=category_data.strip().lower())
            form.instance.categories.add(category)

        return super().form_valid(form)


class RecipeListView(ListView):
    template_name = 'jornapal_app/home.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.order_by('?')[:5]


class RecipeDetailView(DetailView):
    template_name = ''
    model = Recipe
    context_object_name = 'recipe'


# Отобразить рецепты пользователя
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
    form_class = IngredientForm
    template_name = 'jornapal_app/add_ingredient.html'


class IngredientListView(ListView):
    model = Ingredient
    context_object_name = 'ingredients'
    template_name = 'jornapal_app/ingredients_list.html'


class IngredientDetailView(DetailView):
    template_name = 'jornapal_app/ingredient_detail.html'
    model = Ingredient
    context_object_name = 'ingredient'


# Категории
class AddCategoryView(LoginRequiredMixin, CreateView):
    form_class = CategoryForm
    template_name = 'jornapal_app/add_category.html'


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'jornapal_app/categories_list.html'


class CategoryDetailView(DetailView):
    template_name = 'jornapal_app/category_detail.html'
    model = Category
    context_object_name = 'category'
