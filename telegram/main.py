import logging
import os
import requests
from cryptography.fernet import Fernet
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv

# Инициализация логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO  # Set to DEBUG for more detailed logging
)

load_dotenv()

# Получение ключа шифрования из переменных окружения
key = os.getenv('FERNET_KEY')
if not key:
    raise ValueError("No Fernet key found in environment variables. Please set FERNET_KEY in your .env file.")
cipher_suite = Fernet(key)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Просмотр неподтвержденных записей")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите действие:", reply_markup=reply_markup)

# Обработчик нажатия кнопки
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    if user_message == "Просмотр неподтвержденных записей":
        # Отправка запроса на Django view
        response = requests.get('http://127.0.0.1:8000/sendAllNotConfirmedOrdersToTelegram/')
        if response.status_code != 200:
            await update.message.reply_text("Не удалось вывести записи")

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == 'confirm':
        # Проверяем, что query.message существует
        if query.message:
            message_text = query.message.text
            order_id = None
            for line in message_text.split('\n'):
                if "Идентификатор записи:" in line:
                    order_id = int(line.split(': ')[1])
                    break

            if order_id is not None:
                # Отправляем запрос на подтверждение записи с order_id
                response = requests.get(f'http://127.0.0.1:8000/confirmOrder/{order_id}')
                if response.status_code == 200:
                    await query.answer("Запись подтверждена")
                else:
                    await query.answer("Не удалось подтвердить запись")
            else:
                await query.answer("Не удалось определить идентификатор записи")
        else:
            await query.answer("Сообщение не найдено")
    elif query.data == 'cancel':
        # Аналогично получаем order_id и отправляем запрос на отмену записи
        if query.message:
            message_text = query.message.text
            order_id = None
            for line in message_text.split('\n'):
                if "Идентификатор записи:" in line:
                    order_id = int(line.split(': ')[1])
                    break

            if order_id is not None:
                response = requests.get(f'http://127.0.0.1:8000/cancelOrder/{order_id}')
                if response.status_code == 200:
                    await query.answer("Запись отменена")
                else:
                    await query.answer("Не удалось отменить запись")
            else:
                await query.answer("Не удалось определить идентификатор записи")
        else:
            await query.answer("Сообщение не найдено")

if __name__ == '__main__':
    application = ApplicationBuilder().token('7431207165:AAGEnZqak6p6J09Fx5nzOwcO29TaBlyuvak').build()

    # Регистрация обработчиков
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)

    application.add_handler(start_handler)
    application.add_handler(message_handler)
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)