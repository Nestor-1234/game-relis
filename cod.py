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

# Рахунок та максимальні значення
score = 0  # збито ворогів
goal = 15  # кількість ворогів для виграшу (змінено на 15)
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
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.is_jumping = False  # чи в процесі стрибка
        self.jump_speed = -10  # зменшено швидкість стрибка (від -15 до -10)
        self.gravity = 0.5  # сила тяжіння
        self.velocity_y = 0  # вертикальна швидкість

    def update(self):
        keys = key.get_pressed()

        # Стрибок
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
            if self.rect.y >= win_height - 100:  # повертається на землю
                self.rect.y = win_height - 100
                self.is_jumping = False
                self.velocity_y = 0

        # Якщо натиснута клавіша для стрибка (пробіл)
        if keys[K_SPACE] and not self.is_jumping:
            self.jump()  # Викликаємо стрибок

        # Рух вліво
        if keys[K_a]:
            self.rect.x -= self.speed  # Рухаємо гравця вліво

        # Рух вправо
        if keys[K_d]:
            self.rect.x += self.speed  # Рухаємо гравця вправо

    def jump(self):
        self.is_jumping = True
        self.velocity_y = self.jump_speed


# Клас для ворогів
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        # Можемо додати різну швидкість для ворогів
        self.speed = randint(5, 15)  # випадкова швидкість ворога між 5 і 15

    def update(self):
        self.rect.x -= self.speed  # Рухаємо ворога з права на ліво
        global lost
        
        # Якщо ворог виходить за межі екрану з лівої сторони, повертається на праву сторону
        if self.rect.x < -80:
            # Встановлюємо нову координату Y для ворога в правому нижньому куті
            self.rect.x = win_width - 80  # Вороги знову з'являються з правого краю
            self.rect.y = win_height - 50  # Випадкова координата Y для ворога в нижньому куті
            lost += 1  # Збільшуємо лічильник пропущених ворогів

# Функція для скидання гри
def restart_game():
    global score, lost, finish, monsters, ship
    score = 0
    lost = 0
    finish = False
    monsters = sprite.Group()
    ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
    monster1 = Enemy(img_enemy, win_width - 80, win_height - 50, 80, 50, 5)
    monsters.add(monster1)

# Створення вікна
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# Створення спрайтів
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()

# Збільшуємо швидкість ворогів
enemy_speed = 5  # Збільшена швидкість для ворогів

# Створення 1 ворога в правому нижньому куті
monster1 = Enemy(img_enemy, win_width - 80, win_height - 50, 80, 50, enemy_speed)
monsters.add(monster1)

bullets = sprite.Group()

# Завантаження музики та запуск
mixer.music.load("musik1.mp3")  # Завантажуємо музику
mixer.music.set_volume(0.1)  # Встановлюємо гучність (від 0.0 до 1.0)
mixer.music.play(-1, 0.0)  # Відтворюємо музику в циклі (-1 означає безкінечний цикл)

# Змінна для перевірки, чи закінчена гра
finish = False
run = True  # прапорець скидається кнопкою закриття вікна

# Основний цикл гри
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            # При натисканні пробілу викликаємо стрибок
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

        # Оновлюємо спрайти
        ship.update()
        monsters.update()

        # Якщо перший ворог досягає половини екрану, створюємо другого ворога
        if monster1.rect.x <= win_width // 2 and len(monsters) == 1:
            monster2 = Enemy(img_enemy, win_width - 80, win_height - 50, 80, 50, enemy_speed)
            monsters.add(monster2)

        # Малюємо спрайти
        ship.reset()
        monsters.draw(window)

        # Перевірка зіткнення між монстрами і гравцем (для програшу)
        if sprite.spritecollide(ship, monsters, False):
            finish = True
            window.blit(lose_font, (200, 200))

        # Перемога, якщо пропущено 15 перешкод
        if lost >= goal:
            finish = True
            window.blit(win_font, (200, 200))

        # Вивести текст "R - почати заново", якщо гра завершена
        if finish:
            window.blit(restart_font, (250, 300))

        display.update()

    # Перевірка на кінець музики і повторне відтворення, якщо вона закінчилася
    if not mixer.music.get_busy():  # Якщо музика не грає
        mixer.music.play(-1, 0.0)  # Перезапускаємо її в циклі

    time.delay(50)