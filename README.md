![Yamdb_workflow Actions Status](https://github.com/VladislavYar/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title). Произведения делятся на категории:
«Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен (например, можно добавить категорию
«Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения
«Винни Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая
сюита Баха. Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 

Новые жанры может создавать только администратор.

Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению
рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок автоматически высчитывается средняя
оценка произведения.

## Cтек проекта
Python v3.9, Django, DRF, postgreSQL, Docker

## Шаблон наполнения env-файла(так же аналогично для Secrets Actions)
- DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
- DB_NAME=postgres # имя базы данных
- POSTGRES_USER=postgres # логин для подключения к базе данных
- POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
- DB_HOST=db # название сервиса (контейнера)
- DB_PORT=5432 # порт для подключения к БД 

## Шаблон наполнения Secrets Actions
Обратите внимание что в проекте имеется CI/CD(GitHub Actions)
- DOCKER_USERNAME=<ваш_username_dockerhub>
- DOCKER_PASSWORD=<ваш_пароль_dockerhub>
- HOST=<IP-адрес_вашего_сервера>
- USER=<имя_пользователя_для_подключения_к_серверу>
- SSH_KEY=<ssh-ключ_пользователя_для_подключения_к_серверу>
- PASSPHRASE=<фраза-пароль_для_доступа_к_ssh-ключу> # если такой имеется
- TELEGRAM_TO=<ID-аккаунта>
- TELEGRAM_TOKEN=<токен_бота>

## Как запустить проект:

В терминале, перейдите в каталог, в который будет загружаться приложение:
```
cd 
```
Клонируйте репозиторий:
```
git clone git@github.com:VladislavYar/yamdb_final.git
```
### На данном этапе создайте env-файл по шаблону из раздела выше

Перейдите в каталог конфигурации nginx и поменяйте данные поля server_name в файле default.conf на IP(домен) Вашего сервера:
```
cd yamdb_final/infra/nginx/
sudo nano default.conf
```

Далее перейдите в папку инфраструктуры:
```
cd ..
```
Запустите docker-compose командой:
```
docker-compose up -d
```
Выпоните миграции:
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```
### Заполнить базу данных начальными данными (из резервной копии) можно по инструкции раздела ниже.

Создайте суперюзера (логин\почта\пароль):
```
docker-compose exec web python manage.py createsuperuser
```
Соберите статические файлы:
```
docker-compose exec web python manage.py collectstatic --no-input 
```
Теперь проект доступен по адресу http://localhost/.

Остановить и удалить контейнеры, оставив образы:
```
docker-compose down -v
```
### Команды для заполнения базы данных
Создать дамп (резервную копию) базы данных "fixtures.json" можно следующей командой:
```
docker-compose exec web python manage.py dumpdata > fixtures.json
```
Далее команды по востановлению базы данных из резервной копии. Узнаем CONTAINER ID для контейнера:
```
docker container ls -a
```
Копируем файл "fixtures.json" с фикстурами в контейнер:
```
docker cp fixtures.json <CONTAINER ID>:/app
```
Применяем фикстуры:
```
docker-compose exec web python manage.py loaddata fixtures.json
```
Удаляем файл "fixtures.json" из контейнера:
```
docker exec -it <CONTAINER ID> bash
rm fixtures.json
exit
```

## Пользовательские роли
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django — обладет правами администратора (admin)

## Примеры работы с учетными записями через запросы к API
Подробная документация доступна по адресу `http://localhost/redoc/`

Для неавторизованных пользователей работа с API доступна в режиме чтения, что-либо изменить или создать не получится.

### Регистрация нового пользователя
Получить код подтверждения на переданный email. 

- Права доступа: Доступно без токена.
- Использовать имя 'me' в качестве username запрещено. 
- Поля email и username должны быть уникальными.
- Регистрация нового пользователя:

Method:POST `/api/v1/auth/signup/`
```
{
 "email": "string",
 "username": "string"
}
```

### Получение JWT-токена:
Method:POST `/api/v1/auth/token/`
```

{
 "username": "string",
 "confirmation_code": "string"
}
```

### Получение списка всех пользователей.
- Права доступа: Администратор

Method:GET `/api/v1/users/`

### Добавление пользователя:
- Права доступа: Администратор
- Поля email и username должны быть уникальными.

Method:POST `/api/v1/users/`
```
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```
### Получение пользователя по username:
- Права доступа: Администратор

Method:GET `/api/v1/users/{username}/`

### Изменение данных пользователя по username:
- Права доступа: Администратор

Method:PATCH `/api/v1/users/{username}/`
```
{
 "username": "string",
 "email": "user@example.com",
 "first_name": "string",
 "last_name": "string",
 "bio": "string",
 "role": "user"
}
```

### Удаление пользователя по username:
- Права доступа: Администратор

Method: DELETE `/api/v1/users/{username}/`

### Получение данных своей учетной записи:
- Права доступа: Любой авторизованный пользователь

Method:GET `/api/v1/users/me/`

### Изменение данных своей учетной записи:
- Права доступа: Любой авторизованный пользователь

Method:PATCH `/api/v1/users/me/`

## Примеры работы с моделями Categories(Категории)

### Получить список всех категорий:
- Права доступа: Любой авторизованный пользователь

Method:GET `/api/v1/categories/`

### Добавление новой категории:
- Права доступа: Администратор

Method:POST `/api/v1/categories/`

### Удаление категории:
- Права доступа: Администратор

Method:DELETE `/api/v1/categories/{slug}/`

## Примеры работы с моделями Genres(Жанры)
### Получение списка всех жанров:
- Права доступа: Любой пользователь

Method:GET `/api/v1/genres/`

### Добавление жанра:
- Права доступа: Администратор

Method:POST `/api/v1/genres/`

### Удаление жанра:
- Права доступа: Администратор

Method:DELETE `/api/v1/genres{slug}/`

## Примеры работы с моделями Titles(Произведения)

### Получение списка всех произведений:
- Права доступа: Любой пользователь

Method:GET `/api/v1/titles/`

### Добавление произведения:
- Права доступа: Администратор

Method:POST `/api/v1/titles/`

### Получение информации о произведении:
- Права доступа: Любой пользователь

Method:GET `/api/v1/titles/{titles_id}/`

### Частичное обновление информации о произведении:
- Права доступа: Администратор

Method:PATCH `/api/v1/titles/{titles_id}/`

### Удаление произведения:
- Права доступа: Администратор

Method:DELETE `/api/v1/titles/{titles_id}/`

## Примеры работы с моделями Reviews(Отзывы)

### Получения списка всех отзывов
- Права доступа: Любой пользователь

Method:GET `/api/v1/titles/{title_id}/reviews/`

### Создание нового отзыва
- Права доступа: Любой авторизованный пользователь

Method:POST `/api/v1/titles/{title_id}/reviews/`
```
{
  "text": "string",
  "score": 1
}
```

### Получение пользователя по ID
- Права доступа: Любой пользователь

Method:GET `/api/v1/titles/{title_id}/reviews/{review_id}/`
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
### Частичное обновление отзыва по ID
- Права доступа: Автор отзыва, модератор или администратор

Method:PATCH `/api/v1/titles/{title_id}/reviews/{review_id}/`
```
{
  "text": "string",
  "score": 1
}
```
### Удаление отзыва по ID
- Права доступа: Автор отзыва, модератор или администратор

Method:DELETE `/api/v1/titles/{title_id}/reviews/{review_id}/`

## Примеры работы с моделями Comments(Комментарии)

### Получения списка всех комментариев к отзыву
- Права доступа: Любой пользователь

Method:GET `/api/v1/titles/{title_id}/reviews/{review_id}/comments/`

### Добавление комментария к отзыву
- Права доступа: Любой авторизованный пользователь

Method:POST `/api/v1/titles/{title_id}/reviews/{review_id}/comments/`
```
{
  "text": "string"
}
```

### Добавление комментария к отзыву по ID
- Права доступа: Любой пользователь

Method:GET `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`

### Частичное обновление комментария к отзыву по ID
- Права доступа: Автор отзыва, модератор или администратор

Method:PATCH `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`
```
{
  "text": "string"
}
```
### Удаление комментария к отзыву по ID
- Права доступа: Автор отзыва, модератор или администратор

Method:DELETE `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`
