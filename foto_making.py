from PIL import Image, ImageDraw, ImageFont
import time
import os  # Для проверки существования папки


class PostMaker:
    def __init__(self, name_foto):
        self.image = Image.open(name_foto)
        self.w, self.h = self.image.size
        self.image = self.image.resize((self.w // 1, self.h // 1))

    def paste(self, name_foto):  # метод для вставки картинки в картинку
        paste_image = Image.open(name_foto)
        paste_image = paste_image.resize((paste_image.size[0] // 4, paste_image.size[1] // 4))
        self.image.paste(paste_image, (2, 380))

    def upgrade(self, text):  # метод для вставки текста в картинку
        draw = ImageDraw.Draw(self.image)

        # Исходный размер шрифта
        original_size = 27

        # Увеличиваем размер шрифта на 100% (в 2 раза)
        increased_size = int(original_size * 2)

        # Загружаем шрифт
        try:
            font = ImageFont.truetype(r"C:\Users\bdv\PycharmProjects\pythonProject42\Lora-Italic-VariableFont_wght.ttf",
                                      size=increased_size)
        except OSError:
            print("Ошибка: шрифт не найден. Убедитесь, что шрифт доступен.")
            exit()

        # Текущая позиция текста (y = 650)
        current_y = 650

        # Перемещаем текст на 15% ниже
        new_y = current_y + int(current_y * 0.15)

        # Автоматическое разбиение текста на строки
        lines = self.wrap_text(text, font, self.w - 32)  # Максимальная ширина строки

        # Рисуем каждую строку текста
        y = new_y
        for line in lines:
            draw.text((16, y), line, font=font, fill="yellow")  # Укажите цвет текста
            y += font.getbbox(line)[3] - font.getbbox(line)[1] + 10  # Смещение для следующей строки

    def wrap_text(self, text, font, max_width):
        """Разбивает текст на строки, чтобы он уместился в заданную ширину."""
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            # Проверяем, умещается ли текущая строка с добавленным словом
            test_line = current_line + word + " "
            if font.getlength(test_line) <= max_width:
                current_line = test_line
            else:
                # Если не умещается, добавляем текущую строку в список и начинаем новую строку
                lines.append(current_line.strip())
                current_line = word + " "

        # Добавляем последнюю строку
        if current_line:
            lines.append(current_line.strip())

        return lines

    def show(self):  # метод для отображения изображения
        self.image.show()

    def save(self, output_path):  # метод для сохранения изображения
        try:
            # Проверяем, существует ли папка для сохранения
            output_folder = os.path.dirname(output_path)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)  # Создаем папку, если она не существует
                print(f"Папка {output_folder} создана.")

            # Сохраняем изображение
            self.image.save(output_path)
            print(f"Изображение успешно сохранено в {output_path}")
        except PermissionError:
            print(f"Ошибка: нет разрешения на запись в {output_path}. Проверьте права доступа.")
        except Exception as e:
            print(f"Произошла ошибка при сохранении изображения: {e}")


# Создаем новый экземпляр класса PostMaker с новым изображением
image = PostMaker(r"C:\Users\bdv\PycharmProjects\pythonProject42\foto\photo_2024-12-19_10-31-25.jpg")

# Добавляем текст
text = "Владимир Владимирович многие лета Вам! с Днем варенья!"
image.upgrade(text)

# Отображаем изображение с добавленным текстом
image.show()

# Небольшая задержка перед сохранением
time.sleep(2)

# Сохраняем изображение с добавленным текстом на рабочий стол
output_path = r"C:\Users\bdv\Desktop\output_image.jpg"  # Укажите путь на ваш рабочий стол
image.save(output_path)