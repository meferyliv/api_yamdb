# Проект API_YamDB.

## Описание

Данный проект реализует REST API для сервиса YaMDb — базы отзывов о фильмах, книгах и музыке. Через этот интерфейс
смогут работать мобильное приложение или чат-бот. В данном проекте посредством API реализованы следующие возможности:

**Для неавторизованных пользователей**
- Самостоятельная регистрация нового пользователя с кодом подтверждения на e-mail.
- Получение списка всех категроий произведений.
- Получение списка всех жанров произведений.
- Получение списка всех произведений.
- Получение информации о конкретном произведении.
- Получение списка всех отзывов на произведения.
- Получение информации о конкретном отзыве на произведение.
- Получение списка всех комментариев на отзыв по произведению.
- Получение информации о конкретном комментарии к отзыву.

**Для авторизованных пользователей**
- Все возможности неавторизованных пользователей.
- Авторизация пользователя по JWT-токену.
- Получение данных о своей учетной записи.
- Изменение данных своей учетной записи.
- Возможность добавления отзыва с оценкой для произведений.
- Возможности редактирования и удаления своих отзывов с оценкой произведения.
- Возможность добавления комментария для отзывов с оценкой произведений.
- Возможности редактирования и удаления своих комментариев для отзывов с оценкой произведений.

**Для модераторов проекта**
- Все возможности неавторизованных и авторизованных пользователей.
- Возможность редактирования и удаляения отзывов всех пользователей.
- Возможность редактирования и удаляения комментариев всех пользователей.

**Для администраторов**
- Все возможности неавторизованных, авторизованных пользователей и модераторов.
- Добавление и удаление категорий произведений.
- Добавление и удаление жанров произведений.
- Добавление, изменение и удаление информации о произведении.
- Получение списка всех пользователей
- Добавление пользователей
- Просмотр информации о конкретном пользователе.
- Изменение данных пользователя.
- Удаление пользователя.


## Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/meferyliv/api_yamdb
```
```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```
```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
