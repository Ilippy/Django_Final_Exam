# Generated by Django 5.0.3 on 2024-03-29 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jornapal_app', '0002_category_image_ingredient_recipe_cooking_steps_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='jornapal_app.RecipeIngredient', to='jornapal_app.ingredient'),
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='is_optional',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=80, unique=True),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
