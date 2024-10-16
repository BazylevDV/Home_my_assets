import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram import Router, F
from aiogram.filters import Command
from PyPDF2 import PdfReader
from docx import Document

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
API_TOKEN = "7648682046:AAGja31Hvk6Y_VV9HHTeiQ6R2hfeZVHz-vQ"  # Вставьте ваш токен бота здесь

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

router = Router()

# Пример чтения PDF файла
def read_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        logging.error(f"Ошибка при чтении PDF: {e}")
        return "Не удалось прочитать PDF файл."

# Пример чтения Word файла
def read_docx(file_path):
    try:
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text.strip()
    except Exception as e:
        logging.error(f"Ошибка при чтении Word: {e}")
        return "Не удалось прочитать Word файл."

# Обработчик команды /start
@router.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для продажи по выгодным для Вас ценам мед.оборудования и мед.изделий, чем могу помочь?")

# Обработчик команды /readpdf
@router.message(Command('readpdf'))
async def read_pdf_file(message: types.Message):
    pdf_file_path = 'example.pdf'  # Вставьте путь к вашему PDF файлу здесь
    pdf_text = read_pdf(pdf_file_path)
    await message.reply(pdf_text or "PDF файл пуст.")

# Обработчик команды /readdocx
@router.message(Command('readdocx'))
async def read_docx_file(message: types.Message):
    docx_file_path = 'example.docx'  # Вставьте путь к вашему Word файлу здесь
    docx_text = read_docx(docx_file_path)
    await message.reply(docx_text or "Word файл пуст.")

# Обработчик команды /contact
@router.message(Command('contact'))
async def send_contact_info(message: types.Message):
    contact_email = 'your_email@example.com'  # Вставьте ваш адрес электронной почты здесь
    contact_phone = '+7-351-274-40-17'  # Вставьте ваш городской номер телефона здесь
    await message.reply(f"Для связи с нами, напишите на почту: {contact_email} или позвоните по телефону: {contact_phone}")

dp.include_router(router)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())