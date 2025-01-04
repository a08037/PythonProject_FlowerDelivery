import logging
import asyncio
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')
import django

django.setup()
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from config import TOKEN, TELEGRAM_CHAT_ID
from orders.models import Flower
from asgiref.sync import sync_to_async

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()


@sync_to_async
def get_flower_by_id(id):
    return Flower.objects.get(id=id)


@dp.message(Command('start'))
@dp.message(Command('help'))
async def send_welcome(message: types.Message):
    logger.info(f"User {message.from_user.id} sent the /start command")
    await message.reply("Здравствуйте! Я ваш помощник для получения заказов!")


async def send_order_to_telegram(order_data):
    text = f"Получен новый заказ!\n\n" \
           f"🌸 Букет: {order_data['flower_image']}\n" \
           f"💰 Стоимость: {order_data['cost']} ₽\n" \
           f"📅 Дата доставки: {order_data['delivery_date']}\n" \
           f"🕑 Время доставки: {order_data['delivery_time']}\n" \
           f"📍 Адрес доставки: {order_data['delivery_address']}\n" \
           f"💬 Комментарий: {order_data.get('comment', 'Без комментариев')}"

    try:
        await bot.send_photo(TELEGRAM_CHAT_ID, order_data["flower_image"], caption=text, parse_mode=ParseMode.MARKDOWN)
        logger.info("Order data sent successfully to Telegram.")
    except Exception as e:
        logger.error(f"Failed to send order to Telegram: {e}")


@dp.message(Command('order'))
async def order(message: types.Message):
    try:
        flower_id = int(message.text.split()[1])
        flower = await get_flower_by_id(flower_id)

        order_data = {
            "flower_image": flower.image.url,
            "cost": flower.price,
            "delivery_date": "2024-12-25",
            "delivery_time": "14:00",
            "delivery_address": "Москва, ул. Примерная, 10",
            "comment": "Поздравляю с праздником!"
        }

        photo = order_data["flower_image"]
        cost = order_data["cost"]
        delivery_date = order_data["delivery_date"]
        delivery_time = order_data["delivery_time"]
        delivery_address = order_data["delivery_address"]
        comment = order_data.get("comment", "Без комментариев")

        text = f"Получен новый заказ!\n\n" \
               f"🌸 Букет: {photo}\n" \
               f"💰 Стоимость: {cost} ₽\n" \
               f"📅 Дата доставки: {delivery_date}\n" \
               f"🕑 Время доставки: {delivery_time}\n" \
               f"📍 Адрес доставки: {delivery_address}\n" \
               f"💬 Комментарий: {comment}"

        await bot.send_photo(message.chat.id, photo, caption=text, parse_mode=ParseMode.MARKDOWN)
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


if __name__ == '__main__':
    logger.info("Бот запущен")
    asyncio.run(dp.start_polling(bot))

@dp.message_handler(commands=['report'])
async def send_report(message: types.Message):
    report = Report.objects.first()  # Получаем последний отчет
    if report:
        text = f"Отчет за {report.date}:\n"
        text += f"Общее количество заказов: {report.total_orders}\n"
        text += f"Общий объем продаж: {report.total_sales} руб\n"
        text += f"Общий доход: {report.total_revenue} руб\n"
        text += f"Общие расходы: {report.total_expenses} руб\n"
        text += f"Прибыль: {report.profit} руб\n"
    else:
        text = "Отчетов нет."

    await message.reply(text)
