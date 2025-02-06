from pygame import *
from random import randint

# ініціалізація Pygame
font.init()
mixer.init()  # Ініціалізація міксера для роботи з музикою

# Фон гри та зображення
img_back = "Forest.png"  # фон гри
img_hero = "people.png"  # герой
img_enemy = "obstacle.png"  # ворог
img_bullet = "bullet.png"  # куля
img_log = "log.png"  # зображення колоди (замініть на ваше зображення)
heart_img = "heart.png"  # Зображення серця

# Рахунок та максимальні значення
score = 0  # збито ворогів
goal = 51  # кількість ворогів для виграшу (змінено на 15)
lost = 0  # пропущено ворогів
max_lost = 50  # програш, якщо пропустили стільки ворогів

# Текст для виграшу та програшу
win_font = font.Font(None, 60).render('YOU WIN!', True, (255, 255, 255))
lose_font = font.Font(None, 60).render('YOU LOSE!', True, (180, 0, 0))
restart_font = font.Font(None, 36).render('R - почати заново', True, (0, 0, 0))  # Чорний текст для перезапуску

# Клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Клас для головного гравця
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, lives):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.lives = lives  # додаємо кількість життів
        self.start_x = player_x  # Початкове значення X
        self.start_y = player_y  # Початкове значення Y

    def update(self):
        keys = key.get_pressed()

        # Рух вліво
        if keys[K_a]:
            self.rect.x -= self.speed  # Рухаємо гравця вліво

        # Рух вправо
        if keys[K_d]:
            self.rect.x += self.speed  # Рухаємо гравця вправо

        # Перевірка на вихід за межі екрану
        if self.rect.x < 0:  # Лівий край
            self.rect.x = 0
        if self.rect.x > win_width - self.rect.width:  # Правий край
            self.rect.x = win_width - self.rect.width
        if self.rect.y < 0:  # Верхній край
            self.rect.y = 0
        if self.rect.y > win_height - self.rect.height:  # Нижній край
            self.rect.y = win_height - self.rect.height

    def take_damage(self):
        self.lives -= 1  # Зменшуємо кількість життів
        if self.lives <= 0:
            return True  # Якщо життя закінчились, повертаємо True
        return False  # Якщо життя залишились, повертаємо False

    def reset_position(self):
        # Повертаємо гравця на початкові координати
        self.rect.x = win_width // 2 - self.rect.width // 2  # Центруємо по осі X
        self.rect.y = self.start_y  # Встановлюємо Y на початкову позицію

# Клас для ворогів
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.speed = randint(5, 15)  # випадкова швидкість ворога між 5 і 15

    def update(self):
        self.rect.y += self.speed  # Вороги рухаються вниз

        # Якщо ворог виходить за межі екрану, він знову з'являється зверху
        if self.rect.y > win_height:
            self.rect.y = 0  # Встановлюємо Y на найвищу точку екрану
            self.rect.x = randint(0, win_width - self.rect.width)  # Випадкова X координата
            global lost
            lost += 1  # Збільшуємо лічильник пропущених ворогів

# Клас для серця
class Heart(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)

# Ініціалізуємо серце
heart = None  # Спочатку немає серця

# Таймер для появи серця
heart_timer = 0

# Кількість початкових ворогів
initial_enemy_count = 5  # 5 колод на початку гри

# Створюємо ворогів на старті
def create_initial_enemies():
    global monsters
    monsters.empty()  # Очищаємо поточних ворогів, якщо є
    for _ in range(initial_enemy_count):  # Створюємо п'ять ворогів
        new_enemy = Enemy(img_enemy, randint(0, win_width - 80), 0, 80, 50, randint(5, 15))
        monsters.add(new_enemy)

# Перезапуск гри (додавання ворогів)
def restart_game():
    global score, lost, finish, monsters, ship
    score = 0
    lost = 0
    finish = False
    # Переміщаємо персонажа в центр екрану по осі X
    ship = Player(img_hero, win_width // 2 - 80 // 2, win_height - 100, 80, 100, 10, 3)  # 80 - ширина персонажа
    create_initial_enemies()  # Створюємо п'ять ворогів

# Створення вікна
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# Створення групи ворогів
monsters = sprite.Group()

# Створення спрайтів
ship = Player(img_hero, win_width // 2 - 80 // 2, win_height - 100, 80, 100, 10, 3)  # додаємо 3 життя

# Створюємо ворогів на початку
create_initial_enemies()

# Завантаження музики та запуск
mixer.music.load("musik1.mp3")  # Завантажуємо музику
mixer.music.set_volume(0.1)  # Встановлюємо гучність (від 0.0 до 1.0)
mixer.music.play(-1, 0.0)  # Відтворюємо музику в циклі (-1 означає безкінечний цикл)

# Змінна для перевірки, чи закінчена гра
finish = False
run = True  # прапорець скидається кнопкою закриття вікна

# Таймер для додавання нових ворогів
spawn_timer = 0  # Початковий час для додавання нових ворогів

# Основний цикл гри
while run:
    heart_timer += 1  # Кожен кадр збільшуємо таймер
    
    # Поява серця раз на 100 кадрів
    if heart_timer >= 100:
        heart_timer = 0  # Скидаємо таймер
        # Створюємо нове серце з випадковою позицією
        heart = Heart(heart_img, randint(0, win_width - 40), 0, 40, 40, randint(2, 5))

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.jump()  # Викликаємо стрибок
            # Перезапуск гри при натисканні клавіші "R"
            if e.key == K_r and finish:
                restart_game()  # Перезапускаємо гру

    if not finish:
        window.blit(background, (0, 0))

        # Показуємо рахунок
        score_text = font.Font(None, 36).render(f"Пропущено: {lost}", 1, (255, 255, 255))
        window.blit(score_text, (10, 20))

        # Показуємо кількість життів
        lives_text = font.Font(None, 36).render(f"Життя: {ship.lives}", 1, (255, 255, 255))
        window.blit(lives_text, (win_width - 150, 20))

        # Оновлюємо спрайти
        ship.update()
        monsters.update()

        # Додаємо нових ворогів
        if spawn_timer > 500:
            spawn_timer = 0
            new_enemy = Enemy(img_enemy, randint(0, win_width - 80), 0, 80, 50, randint(5, 15))
            monsters.add(new_enemy)

        # Малюємо спрайти
        ship.reset()
        monsters.draw(window)

        # Якщо є серце, оновлюємо та малюємо його
        if heart:
            heart.update()  # Оновлюємо його рух
            heart.reset()  # Малюємо його на екрані

            # Перевірка на зіткнення з серцем
            if sprite.collide_rect(ship, heart):
                heart = None  # Якщо зіткнулися з серцем, видаляємо його

        # Перевірка зіткнення з ворогами
        if sprite.spritecollide(ship, monsters, False):
            if ship.take_damage():
                finish = True
                monsters.empty()
                window.blit(lose_font, (200, 200))
            else:
                ship.reset_position()
                create_initial_enemies()

        # Перемога
        if lost >= goal:
            finish = True
            window.blit(win_font, (200, 200))

        if finish:
            window.blit(restart_font, (250, 300))

        display.update()

    # Перевірка на кінець музики
    if not mixer.music.get_busy():
        mixer.music.play(-1, 0.0)

    time.delay(50)
