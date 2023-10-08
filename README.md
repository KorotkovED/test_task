# TEST_TASK

# Описание сервиса
Сервис предназначен для отслеживания ссылок, на которые переходил сотрудник

# Эндпоинты
Полную документацию можно посмотреть по пути
```
http://127.0.0.1:8000/redoc/
```
или
```
http://127.0.0.1:8000/swagger/
```

Для полного доступа к функционалу сервиса, получите jwt-токен
```
/auth/users/ - регистрация нового пользователя;
(Обязательные поля для регистрации: username, password)

/auth/users/me/ - получить/обновить зарегистрированного пользователя;
/auth/jwt/create/ - создание jwt-токена;
(Токен вернётся в поле access, а данные из поля refresh пригодятся для обновления токена. Для использования токена нужно перед самим токеном ставить ключевое слово Bearer и пробел.)

/auth/jwt/refresh/ - получение нового jwt токена по истечении времени жизни ранее зарегестрированного;
Срок жизни токена - 10 дней
```
Для регистрации сотрудников используйте эндпоинт 
```
/api_v1/user/
```
Регистрация по обязательным полям:
```
first_name - имя
second_name - фамилия
patronymic - отчество
age - возраст
departament - отдел компании
post - должность
email - адрес электронной почты
```
Чтобы добавить новые посещенные ссылки сотрудника, перейдите на эндпоинт 
```
/api_v1/user/{pk}/visited_links/
```
где pk - id сотрудника. Эндпоинт принимает только POST запросы

Чтобы получить уникальные домены, посещенные сотрудником, перейдите на эндпоинт 
```
/api_v1/user/{pk}/visited_domains/
```
где pk - id сотрудника. Эндпоинт принимает только GET запросы

Если хотите уточнить промежуток времени посещенных доментов, то это можно сделать по эндпоинту 
```
/api_v1/user/{pk}}/visited_domains?from={время}&to={время}
```
где время указывается в секундах с начала эпохи.

## Создание виртуального окружения

```
python -m venv venv
```

Сразу же запустите его командой:

Если ОС Windows:

```
source venv/Scripts/activate
```

Если ОС Linux:

```
. venv/bin/activate
```

## Установка модулей
Перейдите в /test_task и установите модули:
```
python -r requirements.txt
```

## Создание файла .env
В этой же директории созадйте файл .env командой:
``` 
touch .env
```

Его содержание:
```
Django_KEY='django-insecure-=w3=m6%2jn-_+uj+$qb80jr6^&1-fhw(x8!v=jxtgxozay(1$u'
DB_ENGINE='django.db.backends.postgresql'
DB_NAME='postgres'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'
DB_HOST='127.0.0.1'
DB_PORT='5432'
```

## Запуск docker-container
Выйдите из /test_task и перейдите в /infra

```
docker-compose up -d --build
```


Для остановки контейнера выполните
```
docker-compose down -v 
```
