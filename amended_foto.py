from PIL import Image, ImageDraw, ImageFont
import time

class PostMaker:
    def __init__(self, name_foto):
        self.image = Image.open(name_foto)
        self.w, self.h = self.image.size
        self.image = self.image.resize((self.w // 1, self.h // 1))

    def paste(self, name_foto):  # метод для вставки картинки в картинку
        paste_image = Image.open(name_foto)
        paste_image = paste_image.resize((paste_image.size[0] // 4, paste_image.size[1] // 4))
        self.image.paste(paste_image, (2, 380))

    def upgrade(self, text):  # метод для вставки какого либо текста в картинку
        draw = ImageDraw.Draw(self.image)
        original_size = 27  # Исходный размер шрифта
        increased_size = int(original_size * 1.12)  # Увеличенный размер шрифта на 15%
        font = ImageFont.truetype(r"D:\\newpythonprojects\\pygame_example\\.Bazylevvenv\\Lora-VariableFont_wght.ttf", size=increased_size)
        draw.text((16, 650), text, font=font, fill="yellow")  # Укажите цвет текста

    def show(self):  # метод для отображения изображения
        self.image.show()

    def save(self, output_path):  # метод для сохранения изображения
        self.image.save(output_path)

# Создаем новый экземпляр класса PostMaker с новым изображением
image = PostMaker(r"D:\\newpythonprojects\\pythonProject11\\photo_2024-12-07_14-39-26.jpg")

# Добавляем новую надпись
image.upgrade(r'Нам ему один ответ: Олег, в Паритете - до 100 лет!')

# Отображаем изображение с добавленной надписью
image.show()

# Небольшая задержка перед сохранением
time.sleep(2)

# Сохраняем изображение с добавленной надписью в указанную папку
output_path = r"D:\\newpythonprojects\\pythonProject11\\output_image.jpg"
image.save(output_path)