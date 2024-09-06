from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext


# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я ваш бот. Чем могу помочь?')


# Функция для обработки текстовых сообщений
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Вы сказали: {update.message.text}')


def main() -> None:
    # Вставляем ваш токен
    application = Application.builder().token("7510171738:AAGNPgXDresmzf3a6ZOzgPVyv7yTmjNi5Ao").build()

    # Добавляем обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускаем бота
    application.run_polling()


if __name__ == '__main__':
    main()
