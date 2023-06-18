import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Класс для базы данных ингредиентов."""
    help = 'Load ingedients_data from csv files'

    def handle(self, *args, **options):
        path = os.path.split(os.path.split(settings.BASE_DIR)[0])
        with open(f'{path[0]}/data/ingredients.csv',
                  'r', encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            objs = []
            for row in reader:
                name, unit = row
                objs.append(Ingredient(name=name, measurement_unit=unit))
            Ingredient.objects.bulk_create(objs)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully load data  {Ingredient.objects.count()} elements')
        )
