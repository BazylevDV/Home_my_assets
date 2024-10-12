from PIL import Image
from PIL import ImageFont, ImageDraw



class PostMaker:
    def __init__(self,name_foto):
        self.image = Image.open(name_foto)
        self.w,self.h = self.image.size
        self.image = self.image.resize((self.w//1,self.h//1))

    def paste(self, name_foto):# метод для вставки картинки в картинку
        paste_image = Image.open(name_foto)
        paste_image = paste_image.resize((paste_image.size[0]//4, paste_image.size[1]//4))
        self.image.paste(paste_image,  (2,380))


    def upgrade(self,text):# метод для вставки какого либо текста в картинку
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype(r"D:\\newpythonprojects\\pygame_example\\.Bazylevvenv\\Lora-VariableFont_wght.ttf")
        draw.text((200,50),text,font=font)
        self.image.show()


image = PostMaker(r"C:\\Users\\admin\\Pictures\\Screenshots\\photo_2024-06-01_07-12-54.jpg")
image.paste(r"C:\\Users\\admin\\Pictures\\Screenshots\\photo_2024-10-12_10-51-57.jpg")
image.upgrade(r'С днем Юбилеем Вас Дмитрий Владимирович!')







