import logging
import asyncio
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')
import django

django.setup()
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TOKEN, TELEGRAM_CHAT_ID
from orders.models import Flower, Report, OrderHistory
from asgiref.sync import sync_to_async
from aiogram.enums import ParseMode
from django.utils import timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Получаем цветок по ID
@sync_to_async
def get_flower_by_id(id):
    return Flower.objects.get(id=id)

# Получаем последний заказ пользователя из истории
@sync_to_async
def get_last_order(user):
    return OrderHistory.objects.filter(order__user=user).order_by('-completed_at').first()

# Отправка заказа в Telegram
async def send_order_to_telegram(order_data):
    text = f"Получен новый заказ!\n\n" \
           f"🌸 Букет: {order_data['flower_image']}\n" \
           f"💰 Стоимость: {order_data['cost']} ₽\n" \
           f"📅 Дата доставки: {order_data['delivery_date']}\n" \
           f"🕑 Время доставки: {order_data['delivery_time']}\n" \
           f"📍 Адрес доставки: {order_data['delivery_address']}\n" \
           f"💬 Комментарий: {order_data.get('comment', 'Без комментариев')}"

    # Формируем полный URL для изображения
    flower_image_url = settings.SITE_URL + order_data["flower_image"].lstrip('/media')

    try:
        # Отправка изображения в Telegram
        await bot.send_photo(TELEGRAM_CHAT_ID, flower_image_url, caption=text, parse_mode=ParseMode.MARKDOWN)
        logger.info("Order data sent successfully to Telegram.")
    except Exception as e:
        logger.error(f"Failed to send order to Telegram: {e}")

# Команда /start и /help
@dp.message(Command('start'))
@dp.message(Command('help'))
async def send_welcome(message: types.Message):
    logger.info(f"User {message.from_user.id} sent the /start command")
    await message.reply("Здравствуйте! Я ваш помощник для получения заказов!")

# Команда /order для оформления заказа
@dp.message(Command('order'))
async def order(message: types.Message):
    try:
        flower_id = int(message.text.split()[1])  # Получаем ID букета из команды
        flower = await get_flower_by_id(flower_id)  # Получаем цветок по ID

        # Создаем данные о заказе
        order_data = {
            "flower_image": flower.image.url,
            "cost": flower.price,
            "delivery_date": "2024-12-25",  # Пример даты доставки
            "delivery_time": "14:00",  # Пример времени доставки
            "delivery_address": "Москва, ул. Примерная, 10",  # Пример адреса
            "comment": "Поздравляю с праздником!"  # Пример комментария
        }

        # Отправляем заказ пользователю в Telegram
        await bot.send_photo(message.chat.id, order_data["flower_image"], caption=f"Ваш заказ: {flower.name}.\nСтоимость: {flower.price} руб", parse_mode=ParseMode.MARKDOWN)

        # Отправляем заказ в Telegram-канал магазина
        await send_order_to_telegram(order_data)

    except IndexError:
        await message.reply("Пожалуйста, укажите ID букета, например: /order 3")
    except ValueError:
        await message.reply("ID букета должно быть числом.")
    except Flower.DoesNotExist:
        await message.reply("Букет с таким ID не найден.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await message.reply("Произошла ошибка, пожалуйста, попробуйте позже.")

# Команда /repeat_order для повторного оформления заказа
@dp.message(Command('repeat_order'))
async def repeat_order(message: types.Message):
    try:
        # Получаем последний заказ пользователя
        last_order = await get_last_order(message.from_user)

        if last_order:
            # Формируем заказ на основе данных последнего
            order_data = {
                "flower_image": last_order.flower.image.url,
                "cost": last_order.flower.price,
                "delivery_date": last_order.delivery_date,
                "delivery_time": last_order.delivery_time,
                "delivery_address": last_order.delivery_address,
                "comment": last_order.comment or "Без комментариев"
            }

            # Отправляем информацию о повторном заказе
            await bot.send_photo(message.chat.id, order_data["flower_image"],
                                 caption=f"Повторный заказ: {last_order.flower.name}\nСтоимость: {order_data['cost']} руб",
                                 parse_mode=ParseMode.MARKDOWN)

            # Отправляем заказ в Telegram-канал магазина
            await send_order_to_telegram(order_data)

        else:
            await message.reply("Вы еще не делали заказ.")
    except Exception as e:
        logger.error(f"Error while repeating order: {e}")
        await message.reply("Произошла ошибка, попробуйте позже.")

# Команда /report для получения отчета о заказах
@dp.message(Command('report'))
async def send_report(message: types.Message):
    try:
        # Получаем отчет за текущий день
        report = await sync_to_async(Report.objects.filter(date=timezone.now().date()).first)()
        if report:
            text = f"Отчет за {report.date}:\n"
            text += f"Общее количество заказов: {report.total_orders}\n"
            text += f"Общий объем продаж: {report.total_sales} руб\n"
            text += f"Общий доход: {report.total_revenue} руб\n"
            text += f"Общие расходы: {report.total_expenses} руб\n"
            text += f"Прибыль: {report.profit} руб\n"
        else:
            text = "Отчетов за сегодня нет."

        await message.reply(text)

    except Exception as e:
        logger.error(f"Error generating report: {e}")
        await message.reply("Произошла ошибка при получении отчета.")

# Функция для запуска бота
def start_bot():
    """Запуск Telegram бота"""
    asyncio.run(dp.start_polling(bot))  # Используем asyncio.run для запуска polling

# Основная функция для запуска всех процессов
def main():
    """Основная функция для запуска всех процессов"""
    print("Запуск проекта...")
    start_bot()

if __name__ == '__main__':
    main()
