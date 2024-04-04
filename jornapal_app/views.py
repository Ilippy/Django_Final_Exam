from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView
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

    def form_valid(self, form):
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
        for key, value in self.request.POST.items():
            print(key, value)
            if key.startswith('ingredient-'):
                index = key.split('-')[1]  # Get the index from the key
                ingredient_name = self.request.POST.get(f'ingredient-{index}-ingredient')
                amount = self.request.POST.get(f'ingredient-{index}-amount')

                if ingredient_name and amount:
                    ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name.strip().lower())
                    form.instance.ingredients.add(ingredient, through_defaults={'amount': amount})
                    # RecipeIngredient.objects.create(
                    #     recipe=self.object,
                    #     ingredient=ingredient,
                    #     amount=amount
                    # )
            if key.startswith('category-'):
                index = key.split('-')[1]
                category_name = self.request.POST.get(f'category-{index}-name')

                if category_name:
                    category, _ = Category.objects.get_or_create(name=category_name.strip().lower())
                    form.instance.categories.add(category)

        # Категории
        # categories = self.request.POST.getlist('category_name')
        # for category_data in categories:
        #     category, _ = Category.objects.get_or_create(name=category_data.strip().lower())
        #     form.instance.categories.add(category)

        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'jornapal_app/update_recipe.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        IngredientFormSet = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=0)
        context['ingredient_formset'] = IngredientFormSet(queryset=self.object.recipe_ingredients.all(),
                                                          prefix='ingredient')
        print(context)
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()

        # Handling images
        images = self.request.FILES.getlist('photo')
        for image_data in images:
            extension = image_data.name.split('.')[-1]
            filename = f'{uuid4()}.{extension}'
            fs = FileSystemStorage()
            fs.save(filename, image_data)
            image = Image.objects.create(url=filename)
            self.object.images.add(image)

        # Handling ingredients
        # ingredient_formset = self.get_context_data()['ingredient_formset']

        for key, value in self.request.POST.items():
            print(key, value)
            if key.startswith('ingredient-'):
                index = key.split('-')[1]  # Get the index from the key
                ingredient_name = self.request.POST.get(f'ingredient-{index}-ingredient')
                amount = self.request.POST.get(f'ingredient-{index}-amount')

                if ingredient_name and amount:
                    ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name.strip().lower())
                    recipe_ingredient, _ = RecipeIngredient.objects.get_or_create(
                        recipe=self.object,
                        ingredient=ingredient
                    )
                    recipe_ingredient.amount = amount
                    recipe_ingredient.save()

        # Handling categories
        categories = self.request.POST.getlist('category_name')
        form.instance.categories.clear()  # Clear existing categories
        for category_data in categories:
            category, _ = Category.objects.get_or_create(name=category_data.strip().lower())
            form.instance.categories.add(category)

        return super().form_valid(form)


class RecipeListView(ListView):
    template_name = 'jornapal_app/home.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        # return Recipe.objects.select_related('author').filter(is_deleted=False).order_by('?')[:5]
        return Recipe.objects.select_related('author').filter(is_deleted=False)


class RecipeDetailView(DetailView):
    template_name = 'jornapal_app/recipe_detail.html'
    model = Recipe
    context_object_name = 'recipe'

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            recipe = self.get_object()
            recipe.is_deleted = True
            recipe.save()
            return redirect('home')
        return render(request, self.template_name)


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
