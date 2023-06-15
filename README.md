![example workflow](https://github.com/Olga-koml/foodgram_project_react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Проект FOODGRAM

[Ссылка на redoc проекта на сервере будет позже](http://158.160.40.3/redoc/ "http://158.160.40.3/redoc/").


Приложение FOODGRAM -  сайт с рецептами. 


## Описание проекта:

Сайт Foodgram, «Продуктовый помощник».  На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд. 


## Стек технологий:

* [Python 3.7+](https://www.python.org/downloads/)
* [Django 4.2.1](https://www.djangoproject.com/download/)
* [Django Rest Framework 3.14.0](https://pypi.org/project/djangorestframework/#files)
* [djoser 2.2.0](https://pypi.org/project/djoser/)
* [Pillow 9.5.0](https://pypi.org/project/Pillow/)
* [PyJWT 2.7.0](https://pypi.org/project/PyJWT/)
* [requests 2.31.0](https://pypi.org/project/requests/)
* [prettytable 3.8.0](https://pypi.org/project/prettytable/)

## Как запустить проект локально:


* Клонировать репозиторий и перейти в него в командной строке

```
https://github.com/Olga-koml/foodgram-project-react
```
* В директории ```infra``` выполните команду для запуска фронтенда через контейнер докера

```
docker-compose up -d
```

* В директории ```backend``` cоздайте и активируйте виртуальное окружение:
```
cd backend
```
```
python -m venv env
```
```
source venv/scripts/activate
```

* Установить зависимости из файла ```requirements.txt```:

```
pip install -r requirements.txt
```

* Перейдите в директорию ```foodgram``` и выполните миграции:

```
cd foodgram
```
```
python manage.py migrate
```

* Выполнить загрузку ингредиентов в базу данных:

```
python manage.py load_csv
```

* Запустить проект:

```
python manage.py runserver
```

## Документация для FOODGRAM доступна по адресу:

```http://localhost/api/docs/redoc.html```

## Сайт FOODGRAM доступен по адресу:

```http://localhost/```

## Автор:

[Комлева Ольга](https://github.com/Olga-koml)
