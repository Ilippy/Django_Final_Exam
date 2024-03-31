from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('categories')


class Ingredient(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ingredients')


class Recipe(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    # лучше это поле вынести в отдельную таблицу, но тогда нужно использовать JS для добавления шагов
    cooking_steps = models.TextField(blank=True, null=False)
    cooking_time = models.TimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    categories = models.ManyToManyField(Category, related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name='recipes')

    def __str__(self):
        return f"{self.title} | {self.author}"


class Image(models.Model):
    url = models.ImageField(upload_to='recipe_images')
    recipe = models.ForeignKey(Recipe, related_name='images', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.url


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    # возможно надо было это сделать числом и вынести тип числа в отдельное поле
    amount = models.CharField(max_length=20, blank=True)
    is_optional = models.BooleanField(default=False)
