from django.contrib import admin
from .models import Recipe, Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'cooking_time', 'author']
    list_editable = ['cooking_time', 'author']
    list_filter = ['cooking_time', 'author']
    search_fields = ['title']


admin.site.register(Ingredient)
