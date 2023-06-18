![example workflow](https://github.com/Olga-koml/foodgram_project_react/actions/workflows/foodgram_workflow.yml/badge.svg)

### Пароли для ревью:
```
# Пользователь с правами администратора
username = admin
password = 123456#F
email = ol@mail.ru

# Пользователь без прав администратора
username = vova
password = 987654#F
email = vv@mail.ru

```

# Проект FOODGRAM

[Ссылка на redoc проекта](http://158.160.40.3/redoc/ "http://158.160.40.3/redoc/").

```http://okk.hopto.org/redoc/```

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

## Как запустить проект на сервере:


* Клонировать репозиторий

```
https://github.com/Olga-koml/foodgram-project-react
```

* На сервере установить docker и docker compose.
```
sudo apt install docker.io
```

* Создайте на сервере дирректорию ```foodgram_project```:
```
mkdir foodgram_project
```

* Добавить в Secrets на Github следующие данные:

```
SECRET_KEY_APP='123'#указать secret key
DB_ENGINE=django.db.backends.postgresql # указать, что проект работает с postgresql
POSTGRES_DB=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД
DB_HOST=db # название сервиса БД (контейнера) 
DB_PORT=5432 # порт для подключения к БД
DOCKER_PASSWORD= # Пароль от аккаунта на DockerHub
DOCKER_USERNAME= # Username в аккаунте на DockerHub
HOST= # IP удалённого сервера
USER= # Логин на удалённом сервере
SSH_KEY= # приватный SSH ключ компьютера, с которого будет происходить подключение к удалённому серверу
PASSPHRASE= #Если для ssh используется фраза-пароль
TELEGRAM_TO= #ID пользователя в Telegram
TELEGRAM_TOKEN= #ID бота в Telegram
```

* Затем локально запустить процес workflow и сделате команды для активации workflow на push проекта:

```
git add .
git commit -m ''
git push
```
* После создастся 2 образа на докерхабе и скопируются на сервер файлы nginx.cong и docker-compose yml. в дирректорию ```foodgram_project```



* На сервере выполните миграции в контейнере ```backend```: 

```
sudo docker compose exec backend python manage.py makemigrations

sudo docker compose exec backend python manage.py migrate
```

* Загрузите статику:
```
sudo docker compose exec backend python manage.py collectstatic --no-input
```

* Создайте суперпользователя:
```
sudo docker compose exec backend python manage.py createsuperuser
```

* Выполнить загрузку данных ингредиентов в базу данных:

```
sudo docker compose exec backend python manage.py load_csv
```
или 

```
docker compose exec backend python manage.py loaddata ingredients.json 
```



#### Проект доступен



## Документация для FOODGRAM доступна по адресу:

```http://localhost/api/docs/redoc.html```
[Ссылка на redoc проекта](http://158.160.40.3/redoc/ "http://158.160.40.3/redoc/")

## Сайт FOODGRAM доступен по адресу:


[http://localhost/](http://158.160.40.3/redoc/ "http://158.160.40.3/redoc/")

## Автор:

[Комлева Ольга](https://github.com/Olga-koml)
