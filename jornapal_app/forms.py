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
            'name': 'Категория'
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


# test image
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={"class": "form-control"}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class RecipeForm(forms.ModelForm):
    photo = MultipleFileField(label='Выбрать файлы', required=False)

    class Meta:
        model = Recipe
        fields = ['photo', 'title', 'description', 'cooking_steps', 'cooking_time']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'cooking_time': forms.TimeInput(format='%H:%M',
                                            attrs={'class': 'form-control', 'type': 'time', 'value': '00:00'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cooking_steps': forms.Textarea(attrs={'class': 'form-control'}),
        }

        labels = {
            'title': 'Название рецепта',
            'cooking_time': 'Время приготовление',
            'description': 'Описание рецепта',
            'cooking_steps': 'Инструкция приготовления ',
        }


class RecipeIngredientForm(forms.ModelForm):
    ingredient = forms.CharField(max_length=80)
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'amount', ]
        widgets = {
            'amount': forms.TextInput(attrs={'placeholder': 'Введите количество'})
        }
