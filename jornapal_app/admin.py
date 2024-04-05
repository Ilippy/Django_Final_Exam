from django.contrib import admin
from django.utils.html import format_html

from .models import Recipe, Ingredient, RecipeIngredient, Category, Image


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['id', 'title', 'cooking_time', 'author']
    list_editable = ['cooking_time', 'author']
    list_filter = ['cooking_time', 'author']
    search_fields = ['title']
    filter_horizontal = ['categories']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['id', 'name']
    list_editable = ['name']


admin.site.register(Category)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_tag', ]
    fields = ['image_tag']
    readonly_fields = ['image_tag']
