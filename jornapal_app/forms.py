from .models import Recipe, Ingredient, Category, Image, RecipeIngredient
from django import forms


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

        labels = {
            'name': 'Ингридиент'
        }

        error_messages = {
            'name': {
                # 'max_length': "Слишком много символов",
                'unique': "Такой ингредиент уже существует",
                'required': 'Укажите хотя бы один символ',
            }
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            return name.lower()
        return name


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

        labels = {
            'name': 'Ингридиент'
        }

        error_messages = {
            'name': {
                # 'max_length': "Слишком много символов",
                'unique': "Такая категория уже существует",
                'required': 'Укажите хотя бы один символ',
            }
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            return name.lower()
        return name

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_steps', 'cooking_time', 'categories', 'ingredients']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['url']


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'amount', 'is_optional']
