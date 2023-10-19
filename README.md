# Сonverter into mp3

![FastAPI](https://img.shields.io/badge/FastAPI-ff033e?style=for-the-badge&logo=fastapi&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-000000?style=for-the-badge&logo=python&logoColor=white) ![Pydantic](https://img.shields.io/badge/Pydantic-000000?style=for-the-badge&logo=python&logoColor=white) ![Alembic](https://img.shields.io/badge/Alembic-000000?style=for-the-badge&logo=python&logoColor=white) ![Postgres](https://img.shields.io/badge/postgresql-ff033e?style=for-the-badge&logo=postgresql&logoColor=white)

## Задание 1
Необходимо реализовать API сервис который будет принимать пост запрос в виде:
```
{"questions_num": integer}
```
И отправлять запрос на
```
https://jservice.io/api/random?count=1
```
Вытаскивая из ответа `count` - количество вопросов и информацию о них, сохранять их в базу
и в качестве ответа выдавать последний сохраненный вопрос. (все вопросы в базе уникальные)

### Пример запроса и ответа
- *POST* запрос на endpoint `/quiz` сохранит в базе 2 вопроса предоставленные API - `jservice.io/api`
```
{"questions_num": 2}
```
- и в качестве ответа выдаст последний вопрос:
```
{
  "id": 106305,
  "question": "To metabolize calcium & have strong bones, iguanas need this type of radiation, provided by a special light",
  "answer": "ultraviolet",
  "created_at": "2022-12-30T19:35:09.980000+00:00"
}
```

## Задание 2
Необходимо реализовать веб-сервис, выполняющий следующие функции:
- Создание пользователя;
- Для каждого пользователя - преобразование аудиозаписи из формата `wav` в `mp3`, сохранение ее в базу данных и предоставление ссылки для скачивания аудиозаписи.

Доступны следующие эндпоинты:
```
- auth/jwt/login (POST)
- auth/jwt/logout (POST)
- auth/jwt/register (POST)
- /add-audio (POST)
- /download (GET)
```
### Алгоритм регистрации:
- клиент отправляет `POST` запрос на endpoint `auth/jwt/register` в виде:
```
{
  "email": "maks@example.com",
  "password": "maks1234",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```
- поля `is_active`, `is_superuser`, `is_verified` - меняются на дефолтные в процессе обработки данных
- Далее клиент вводит данные для авторизации *email* и *password* по endpoint-у `auth/jwt/login` и получает JWT - токен, который хранится в `cookie`

### Алгоритм сохранения аудиозаписи
- Для сохранения аудиозаписи в бд клиент отправляет `POST` запрос на endpoint `/add-audio` с аудиофайлом в формате `wav`
```
http://127.0.0.1:8000/add-audio?user_id=7dab660d-57b8-44c5-b82a-5ceb3d5c5f32
```
В ответе получает:
```
{
  "detail": "Аудиозапись успешно добавлена",
  "file_id": "72acf242-aed5-44e6-a2bc-f0a338c9f2d8"
}
```
- Для загрузки аудиофайла клиент отправляет `GET` запрос на endpoint `/download`:
```
http://127.0.0.1:8000/download?file_id=72acf242-aed5-44e6-a2bc-f0a338c9f2d8
```
- И получает возможность скачать аудиофайл в формате `mp3`

## Установка проекта через `docker`
1. клонируйте репозиторий:
```
git clone git@github.com:xodiumx/test_for_bewise.git
```
2. Перейдите в директорию `infra`
```
cd infra
```
3. В этой директории создайте файл `.env` пример:
```
SECRET_KEY=KDOuifes@@ruy432iiupupifesUIPDASBDKGA3dko5OwCXyli1Il8M
USER_SECRET_KEY=KDOuifehtryuoigreuo@4327TG!!*&g8cbSAidsamopi~!^

DB_HOST=db
DB_PORT=5432
DB_NAME=tasks
DB_USER=postgres
DB_PASS=postgres

DB_NAME=tasks
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
4. Выполните команду:
```
docker-compose up -d
```
5. В контейнере `db` выполните команды:
```
psql -U postgres
CREATE DATABASE tasks;
```
6. В контейнере `back` выполните команду:
```
alembic upgrade head
```
### Подробная информация по endpoint-у `/docs`
