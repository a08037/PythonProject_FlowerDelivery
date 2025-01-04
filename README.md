# FlowerDelivery

**FlowerDelivery** — это веб-приложение для заказа цветов с интеграцией Telegram-бота. Пользователи могут просматривать каталог цветов, оформлять заказы, а также получать обновления о статусе своих заказов через Telegram-бота.

## Описание проекта

FlowerDelivery предоставляет удобный интерфейс для выбора и покупки цветов, а также функциональность для управления заказами. В проект включена интеграция с Telegram-ботом, который уведомляет клиентов о статусах их заказов и позволяет отслеживать обновления.

## Стек технологий

- **Backend**: Django
- **Telegram Bot**: Python (aiogram)
- **Frontend**: HTML, CSS, Bootstrap
- **База данных**: SQLite (по умолчанию, можно настроить для использования других СУБД)
- **Авторизация и регистрация**: Django Allauth
- **Аналитика и отчеты**: Yandex DataLens (для анализа заказов и статистики)

## Установка

Для того чтобы запустить проект локально, выполните следующие шаги:

### 1. Клонировать репозиторий:

```bash
git clone https://github.com/your-username/FlowerDelivery.git
cd FlowerDelivery


### 2. Создать и активировать виртуальное окружение:
bash
Копировать код
python -m venv venv
source venv/bin/activate  # Для Linux/MacOS
venv\Scripts\activate     # Для Windows

### 3. Установить зависимости:
bash
Копировать код
pip install -r requirements.txt

### 4. Настроить файл конфигурации для Telegram-бота:
Создайте файл config.py в корне проекта и добавьте свои API ключи:
python
Копировать код
TOKEN = 'your-telegram-bot-token'
WEATHER_API_KEY = 'your-weather-api-key'
THE_CAT_API_KEY = 'your-cat-api-key'

### 5. Миграции базы данных:
bash
Копировать код
python manage.py migrate

### 6. Запуск сервера:
bash
Копировать код
python manage.py runserver
Теперь вы можете зайти на http://127.0.0.1:8000 и начать пользоваться приложением.

Как использовать Telegram-бота
Найдите бота в Telegram по имени, которое вы указали при регистрации бота в BotFather.
Начните общение с ботом, используя команду /start или /help.
Бот уведомит вас о статусе заказа и предложит дополнительные функции, такие как получение прогноза погоды или картинок с кошками.
Функциональные возможности
Просмотр каталога цветов: клиенты могут выбрать цветы и добавить их в корзину.
Оформление заказов: пользователи могут оформить заказ, указав контактные данные.
История заказов: пользователи могут просматривать историю своих заказов через веб-интерфейс.
Уведомления через Telegram-бота: бот будет информировать пользователей о статусах их заказов.
Аналитика: интеграция с Yandex DataLens позволяет анализировать заказы, популярные товары и другие бизнес-показатели.
Вклад в проект
Если вы хотите внести изменения или улучшения в проект, пожалуйста, создайте pull request. Перед этим убедитесь, что ваш код прошел тесты и соответствует стандартам проекта.

Лицензия
Этот проект распространяется под лицензией MIT. Подробности можно найти в файле LICENSE.

Контакты
Если у вас возникли вопросы, свяжитесь с нами по электронной почте: a08037@gmail.com

