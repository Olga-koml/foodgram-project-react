import csv

from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Класс для загрузки базы данных ингредиентов на сервере."""
    help = 'Load ingedients_data from csv files'

    def handle(self, *args, **options):
        with open('/app/data/ingredients.csv',
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
