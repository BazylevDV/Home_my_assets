from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import telebot
import datetime

# Состояния для разных этапов заполнения заявки
INITIATOR_INFO, EQUIPMENT_INFO, SERVICES_INFO, COMMERCIAL_OFFER, FEEDBACK = range(5)

# Словарь для хранения номеров заявок для каждого учреждения
institution_request_count = {}

# Дата последнего обнуления счетчика
last_reset_date = datetime.datetime.now().date()


# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Привет! Я ваш бот. Чем могу помочь?\n'
        'Для начала заполнения заявки, нажмите /new_request'
    )
    return ConversationHandler.END


# Функция для начала заполнения заявки
def new_request(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Давайте начнем заполнение заявки.\n'
        'Пожалуйста, введите ФИО инициатора заявки:'
    )
    return INITIATOR_INFO


# Функция для обработки ФИО инициатора заявки
def initiator_info(update: Update, context: CallbackContext) -> int:
    context.user_data['initiator_fio'] = update.message.text
    update.message.reply_text(
        'Введите должность инициатора заявки:'
    )
    return INITIATOR_INFO


# Функция для обработки должности инициатора заявки
def initiator_position(update: Update, context: CallbackContext) -> int:
    context.user_data['initiator_position'] = update.message.text
    update.message.reply_text(
        'Введите телефон инициатора заявки:'
    )
    return INITIATOR_INFO


# Функция для обработки телефона инициатора заявки
def initiator_phone(update: Update, context: CallbackContext) -> int:
    context.user_data['initiator_phone'] = update.message.text
    update.message.reply_text(
        'Введите название учреждения:'
    )
    return INITIATOR_INFO


# Функция для обработки названия учреждения
def institution_name(update: Update, context: CallbackContext) -> int:
    context.user_data['institution_name'] = update.message.text
    update.message.reply_text(
        'Введите наименование оборудования:'
    )
    return EQUIPMENT_INFO


# Функция для обработки наименования оборудования
def equipment_name(update: Update, context: CallbackContext) -> int:
    context.user_data['equipment_name'] = update.message.text
    update.message.reply_text(
        'Выберите необходимые услуги:\n'
        '1. Диагностика\n'
        '2. Ремонт\n'
        '3. Up-grade (модернизация)'
    )
    return SERVICES_INFO


# Функция для обработки выбора услуг
def services_info(update: Update, context: CallbackContext) -> int:
    context.user_data['services'] = update.message.text
    update.message.reply_text(
        'Выберите запрос коммерческого предложения:\n'
        '1. На годовое обслуживание\n'
        '2. Закуп запасных частей\n'
        '3. Ремонт внеплановый\n'
        '4. Нового оборудования и/или медизделий для его работы'
    )
    return COMMERCIAL_OFFER


# Функция для обработки запроса коммерческого предложения
def commercial_offer(update: Update, context: CallbackContext) -> int:
    context.user_data['commercial_offer'] = update.message.text
    update.message.reply_text(
        'Спасибо за заполнение заявки!\n'
        'Ваша заявка:\n'
        f"Инициатор: {context.user_data['initiator_fio']}, {context.user_data['initiator_position']}, {context.user_data['initiator_phone']}\n"
        f"Учреждение: {context.user_data['institution_name']}\n"
        f"Оборудование: {context.user_data['equipment_name']}\n"
        f"Необходимые услуги: {context.user_data['services']}\n"
        f"Запрос коммерческого предложения: {context.user_data['commercial_offer']}"
    )

    # Запись данных в Google Таблицы
    write_to_google_sheets(context.user_data)

    # Отправка уведомления на email
    send_email_notification(context.user_data)

    # Показ салюта из конфети
    show_confetti(update, context)

    # Предложение оставить отзыв
    update.message.reply_text(
        'Пожалуйста, оставьте отзыв о работе инженеров:',
        reply_markup=ReplyKeyboardMarkup(
            [['Разочарование', 'Неудовлетворение', 'Нейтрально', 'Удовлетворение', 'Широчайшая улыбка']],
            one_time_keyboard=True)
    )
    return FEEDBACK


# Функция для обработки отзыва
def feedback(update: Update, context: CallbackContext) -> int:
    context.user_data['feedback_rating'] = update.message.text
    update.message.reply_text(
        'Пожалуйста, напишите комментарий о работе инженеров:'
    )
    return FEEDBACK


# Функция для обработки комментария
def feedback_comment(update: Update, context: CallbackContext) -> int:
    context.user_data['feedback_comment'] = update.message.text
    update.message.reply_text(
        'Спасибо за ваш отзыв!\n'
        f"Оценка: {context.user_data['feedback_rating']}\n"
        f"Комментарий: {context.user_data['feedback_comment']}"
    )

    # Отправка отзыва на email
    send_feedback_notification(context.user_data)

    return ConversationHandler.END


# Функция для отмены заявки
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Заявка отменена.',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


# Функция для записи данных в Google Таблицы
def write_to_google_sheets(data):
    global last_reset_date
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('your_credentials_file.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("Your Google Sheet Name").sheet1

    # Проверка на изменение года и обнуление счетчика
    current_date = datetime.datetime.now().date()
    if current_date.year != last_reset_date.year:
        institution_request_count.clear()
        last_reset_date = current_date

    # Присваивание номера заявки для каждого учреждения
    institution_name = data['institution_name']
    if institution_name not in institution_request_count:
        institution_request_count[institution_name] = 0
    institution_request_count[institution_name] += 1
    request_number = institution_request_count[institution_name]

    row = [
        request_number,
        data['initiator_fio'],
        data['initiator_position'],
        data['initiator_phone'],
        data['institution_name'],
        data['equipment_name'],
        data['services'],
        data['commercial_offer']
    ]

    sheet.append_row(row)


# Функция для отправки email-уведомления
def send_email_notification(data):
    sender_email = "your_email@gmail.com"
    sender_password = "your_email_password"
    receiver_emails = ["sereginsn@mail.ru", "S9120832249@yandex.ru"]

    message = MIMEMultipart()
    message["From"] = sender_email
    message["Subject"] = "Новая заявка"

    body = f"""
    Новая заявка:
    Инициатор: {data['initiator_fio']}, {data['initiator_position']}, {data['initiator_phone']}
    Учреждение: {data['institution_name']}
    Оборудование: {data['equipment_name']}
    Необходимые услуги: {data['services']}
    Запрос коммерческого предложения: {data['commercial_offer']}
    """

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        for receiver_email in receiver_emails:
            message["To"] = receiver_email
            server.sendmail(sender_email, receiver_email, message.as_string())


# Функция для отправки отзыва на email
def send_feedback_notification(data):
    sender_email = "your_email@gmail.com"
    sender_password = "your_email_password"
    receiver_emails = ["sereginsn@mail.ru", "S9120832249@yandex.ru"]

    message = MIMEMultipart()
    message["From"] = sender_email
    message["Subject"] = "Отзыв о работе инженеров"

    body = f"""
    Отзыв о работе инженеров:
    Учреждение: {data['institution_name']}
    Оценка: {data['feedback_rating']}
    Комментарий: {data['feedback_comment']}
    """

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        for receiver_email in receiver_emails:
            message["To"] = receiver_email
            server.sendmail(sender_email, receiver_email, message.as_string())


# Функция для показа салюта из конфети
def show_confetti(update: Update, context: CallbackContext):
    bot = telebot.TeleBot("7510171738:AAGNPgXDresmzf3a6ZOzgPVyv7yTmjNi5Ao")
    bot.send_animation(update.effective_chat.id, "https://media.giphy.com/media/3o7TKUM3IgJBX2as9O/giphy.gif")


def main() -> None:
    # Вставляем ваш токен
    application = Application.builder().token("7510171738:AAGNPgXDresmzf3a6ZOzgPVyv7yTmjNi5Ao").build()

    # Определяем обработчик для заявки
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('new_request', new_request)],
        states={
            INITIATOR_INFO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, initiator_info),
                MessageHandler(filters.TEXT & ~filters.COMMAND, initiator_position),
                MessageHandler(filters.TEXT & ~filters.COMMAND, initiator_phone),
                MessageHandler(filters.TEXT & ~filters.COMMAND, institution_name)
            ],
            EQUIPMENT_INFO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, equipment_name)
            ],
            SERVICES_INFO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, services_info)
            ],
            COMMERCIAL_OFFER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, commercial_offer)
            ],
            FEEDBACK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, feedback),
                MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_comment)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Добавляем обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)

    # Запускаем бота
    application.run_polling()
