# Generated by Django 4.2.1 on 2023-06-03 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_remove_shoppingcart_recipe_recipe_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]
