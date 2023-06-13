# Generated by Django 4.2.1 on 2023-05-31 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.RecipesIngredient', to='recipes.ingredient', verbose_name='Ингридиент'),
        ),
        migrations.AlterField(
            model_name='recipesingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes_ingredients', to='recipes.ingredient', verbose_name='Ингредиент'),
        ),
    ]
