from django.forms import modelformset_factory, inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView
from .models import Ingredient, Recipe, Image, Category, RecipeIngredient
from .forms import IngredientForm, RecipeForm, RecipeIngredientForm, CategoryForm, IngredientFormSet
from django.contrib.auth.mixins import LoginRequiredMixin


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
            Image(url=image_data, recipe=self.object).save()

        # Handling ingredients and categories
        for key, value in self.request.POST.items():
            # print(key, value)
            match key.split('-'):
                case ['ingredient', index, 'ingredient']:
                    amount = self.request.POST.get(f'ingredient-{index}-amount')
                    if value and amount:
                        ingredient, _ = Ingredient.objects.get_or_create(name=value.strip().lower())
                        form.instance.ingredients.add(ingredient, through_defaults={'amount': amount})
                case ['category', _, 'name']:
                    if value:
                        category, _ = Category.objects.get_or_create(name=value.strip().lower())
                        form.instance.categories.add(category)

        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'jornapal_app/update_recipe.html'

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredient_formset'] = IngredientFormSet(instance=self.object, prefix='ingredient')
        # print(context)
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()

        # ingredient_formset = self.get_context_data()['ingredient_formset']
        # ingredient_formset = IngredientFormSet(data=self.request.POST, files=self.request.FILES, instance=self.object)
        # for obj in ingredient_formset:
        #     print(obj)
        #
        # print(ingredient_formset.cleaned_data)
        #
        # Handling ingredients
        # TODO: Разобраться как сделать сохранение ингредиентов через formset
        # if form.is_valid() and not ingredient_formset.errors:  # ingredient_formset.is_valid() возвращает False
        #     self.object.save()
        #     ingredient_formset.save()  # Save the formset
        # else:
        #     print(ingredient_formset.errors, ingredient_formset.non_form_errors)

        # Handling images
        images = self.request.FILES.getlist('photo')
        for image_data in images:
            Image(url=image_data, recipe=self.object).save()

        # Handling ingredients and  categories
        existing_ingredients = set(self.object.ingredients.values_list('id', flat=True))
        categories = set()
        ingredients = set()
        for key, value in self.request.POST.items():
            match key.split('-'):
                case ['ingredient', index, 'ingredient']:
                    ingredient_name = value.strip().lower()
                    recipe_ingredient_id = self.request.POST.get(f'ingredient-{index}-id')
                    amount = self.request.POST.get(f'ingredient-{index}-amount')
                    if ingredient_name and amount:
                        if recipe_ingredient_id:
                            # recipe_ingredients.add(recipe_ingredient_id)
                            recipe_ingredient = self.object.recipe_ingredients.get(id=recipe_ingredient_id)
                            if recipe_ingredient:
                                ingredients.add(recipe_ingredient.ingredient.id)
                                if recipe_ingredient.ingredient.name == ingredient_name:
                                    if recipe_ingredient.amount != amount:
                                        recipe_ingredient.amount = amount
                                        recipe_ingredient.save()
                                else:
                                    recipe_ingredient.delete()
                                    ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
                                    self.object.ingredients.add(ingredient, through_defaults={'amount': amount})
                        else:
                            ingredient, _ = Ingredient.objects.get_or_create(name=value.strip().lower())
                            self.object.ingredients.add(ingredient, through_defaults={'amount': amount})

                case ['category', _, 'name']:
                    category_name = value.strip().lower()
                    if category_name:
                        categories.add(category_name)

        ingredients_to_remove = existing_ingredients - ingredients
        self.object.ingredients.filter(id__in=ingredients_to_remove).delete()

        existing_categories = set(self.object.categories.values_list('name', flat=True))
        categories_to_remove = existing_categories - categories
        self.object.categories.filter(name__in=categories_to_remove).delete()

        categories_to_add = categories - existing_categories
        for category_name in categories_to_add:
            category, _ = Category.objects.get_or_create(name=category_name)
            self.object.categories.add(category)

        return super().form_valid(form)

    def post(self, request, pk):
        # удаление картинок
        if 'delete_image' in request.POST:
            image_id = request.POST.get('delete_image')
            image = Image.objects.filter(pk=image_id).first()
            if image:
                image.delete()
        return redirect('recipe_update', pk)

    # def form_invalid(self, form):
    #     response = super().form_invalid(form)
    #     print(response)
    #     return JsonResponse(form.errors, status=400)


class RecipeListView(ListView):
    template_name = 'jornapal_app/home.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.select_related('author').filter(is_deleted=False).order_by('?')[:5]
        # return Recipe.objects.select_related('author').filter(is_deleted=False)


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
        elif 'update' in request.POST:
            return redirect('recipe_update', pk=self.get_object().id)
        return render(request, self.template_name)


# Отобразить рецепты пользователя
class MyRecipeListView(LoginRequiredMixin, ListView):
    template_name = 'jornapal_app/home.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.select_related('author').filter(is_deleted=False, author=self.request.user)


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
