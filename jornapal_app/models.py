import os
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe


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
    cooking_steps = models.TextField(blank=True, null=False)
    cooking_time = models.TimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    categories = models.ManyToManyField(Category, related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name='recipes')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} | {self.author}"


def rename_image_filename(instance, filename):
    """Изменение имени файла"""
    upload_to = 'recipe_images'
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.recipe.id, uuid4(), ext)
    return os.path.join(upload_to, filename)


class Image(models.Model):
    url = models.ImageField(upload_to=rename_image_filename)
    recipe = models.ForeignKey(Recipe, related_name='images', on_delete=models.CASCADE, null=True)

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % self.url)

    image_tag.short_description = 'Image'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    # возможно надо было это сделать числом и вынести тип измерения в отдельное поле
    amount = models.CharField(max_length=20, blank=True)
