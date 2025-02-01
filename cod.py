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
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, lives):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.lives = lives  # додаємо кількість життів
        self.is_jumping = False  # чи в процесі стрибка
        self.jump_speed = -10  # зменшено швидкість стрибка (від -15 до -10)
        self.gravity = 0.5  # сила тяжіння
        self.velocity_y = 0  # вертикальна швидкість
        self.jump_count = 0  # Лічильник стрибків
        self.start_y = player_y  # Початкова координата Y
        self.start_x = player_x  # Початкова координата X

    def update(self):
        keys = key.get_pressed()

        # Стрибок
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

            # Обмежуємо максимальну висоту стрибка 275
            if self.rect.y <= 275:
                self.rect.y = 275  # Не дозволяємо гравцю піднятися вище 275
                self.velocity_y = 0

            # Якщо персонаж досягає низу (землі), зупиняється
            if self.rect.y >= win_height - 100:
                self.rect.y = win_height - 100
                self.is_jumping = False
                self.velocity_y = 0
                # Після другого стрибка повертаємо персонажа в початкову координату Y
                if self.jump_count >= 2:
                    self.rect.y = self.start_y
                    self.jump_count = 0  # скидаємо лічильник стрибків

        # Якщо натиснута клавіша для стрибка (пробіл)
        if keys[K_SPACE] and not self.is_jumping and self.jump_count < 2:
            self.jump()  # Викликаємо стрибок

        # Рух вліво
        if keys[K_a]:
            if self.rect.x > 0:  # Якщо гравець не виходить за ліву межу
                self.rect.x -= self.speed  # Рухаємо гравця вліво

        # Рух вправо
        if keys[K_d]:
            if self.rect.x < win_width // 2 - self.rect.width:  # Обмеження на рух вправо
                self.rect.x += self.speed  # Рухаємо гравця вправо

    def jump(self):
        self.is_jumping = True
        self.velocity_y = self.jump_speed
        self.jump_count += 1  # Збільшуємо лічильник стрибків

    def take_damage(self):
        self.lives -= 1  # Зменшуємо кількість життів
        if self.lives <= 0:
            return True  # Якщо життя закінчились, повертаємо True
        return False  # Якщо життя залишились, повертаємо False

    def reset_position(self):
        # Повертаємо гравця на початкові координати
        self.rect.x = self.start_x
        self.rect.y = self.start_y

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

# Функція для скидання гри
def restart_game():
    global score, lost, finish, monsters, ship
    score = 0
    lost = 0
    finish = False
    monsters = sprite.Group()
    ship = Player(img_hero, 5, win_height - 100, 80, 100, 10, 3)  # додаємо 3 життя
    # Створюємо ворогів з найвищою координатою Y (0) та випадковою X
    monster1 = Enemy(img_enemy, randint(0, win_width - 80), 0, 80, 50, 5)  # Вороги на випадковій X
    monster2 = Enemy(img_enemy, randint(0, win_width - 80), 0, 80, 50, 5)  # Вороги на випадковій X
    monsters.add(monster1, monster2)

# Створення вікна
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# Створення спрайтів
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10, 3)  # додаємо 3 життя

monsters = sprite.Group()

# Створюємо ворогів з випадковими координатами X і найвищою координатою Y (0)
monster1 = Enemy(img_enemy, randint(0, win_width - 80), 0, 80, 50, 5)  # Вороги на випадковій X
monster2 = Enemy(img_enemy, randint(0, win_width - 80), 0, 80, 50, 5)  # Вороги на випадковій X
monsters.add(monster1, monster2)

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
    spawn_timer += 1  # Кожен кадр збільшуємо таймер

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

        # Додаємо нових ворогів, коли пройшов певний час
        if spawn_timer > 500:  # Наприклад, через кожні 500 кадрів
            spawn_timer = 0  # Скидаємо таймер
            # Додаємо нового ворога, який з'являється зверху
            new_enemy = Enemy(img_enemy, randint(0, win_width - 80), 0, 80, 50, 5)  # Випадкова X
            monsters.add(new_enemy)

        # Малюємо спрайти
        ship.reset()
        monsters.draw(window)

        # Перевірка зіткнення між монстрами і гравцем (для програшу)
        if sprite.spritecollide(ship, monsters, False):
            if ship.take_damage():  # якщо життя закінчились
                finish = True
                # Очищуємо всі вороги
                monsters.empty()  
                window.blit(lose_font, (200, 200))
            else:
                # Повертаємо гравця на початкові координати
                ship.reset_position()

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
