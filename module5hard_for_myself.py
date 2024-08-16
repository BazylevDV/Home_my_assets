import time

class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = self.hash_password(password)
        self.age = age

    def hash_password(self, password):
        return hash(password)

class Video:
    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration
        self.adult_mode = adult_mode

class UrTube:
    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None
        self.user_logged_in = False
        self.user_age = 0

    def __log_in__(self, nickname, password):
        hashed_password = hash(password)
        for user in self.users:
            if user.nickname == nickname and user.password == hashed_password:
                self.current_user = user
                self.user_logged_in = True
                self.user_age = user.age
                print(f'Вы вошли как {user.nickname}')
                return
        print(f'Пользователь {nickname} не найден')

    def __register__(self, nickname, password, age):
        for user in self.users:
            if user.nickname == nickname:
                print(f'Пользователь {nickname} уже существует')
                return
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user
        self.user_logged_in = True
        self.user_age = age
        print(f'Пользователь {nickname} успешно зарегистрирован')

    def add(self, *videos):
        for video in videos:
            if not any(v.title == video.title for v in self.videos):
                self.videos.append(video)
                print(f'Видео {video.title} успешно добавлено')
            else:
                print(f'Видео {video.title} уже существует')

    def get_videos(self, search_word):
        search_word_lower = search_word.lower()
        filtered_videos = [video.title for video in self.videos if search_word_lower in video.title.lower()]
        return filtered_videos

    def watch_video(self, video_title):
        if not self.user_logged_in:
            print('Зайдите в систему, чтобы смотреть видео')
            return
        video = next((v for v in self.videos if v.title == video_title), None)
        if not video:
            print('Видео не найдено')
            return
        if video.adult_mode and self.user_age < 18:
            print('Вам нет 18 лет, пожалуйста покиньте страницу')
            return
        print(f'Воспроизведение видео {video_title}')
        for second in range(1, video.duration + 1):
            print(f'Просмотр на {second} секунде')
            time.sleep(1)
        print('Конец видео')

# Пример использования
ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.__register__('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.__register__('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.__register__('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user.nickname)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')
