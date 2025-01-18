from pygame import *
from random import randint

# ініціалізація Pygame
font.init()

# Фон гри та зображення
img_back = "Forest.png"  # фон гри
img_hero = "people.png"  # герой
img_enemy = "obstacle.png"  # ворог
img_bullet = "bullet.png"  # куля

# Рахунок та максимальні значення
score = 0  # збито ворогів
goal = 50  # кількість ворогів для виграшу
lost = 0  # пропущено ворогів
max_lost = 50  # програш, якщо пропустили стільки ворогів

# Текст для виграшу та програшу
win_font = font.Font(None, 60).render('YOU WIN!', True, (255, 255, 255))
lose_font = font.Font(None, 60).render('YOU LOSE!', True, (180, 0, 0))

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
        self.jump_speed = -15  # швидкість стрибка
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
            self.jump()  # Викликаємо метод для стрибка

    def jump(self):
        self.is_jumping = True
        self.velocity_y = self.jump_speed


# Клас для ворогів
class Enemy(GameSprite):
    def update(self):
        self.rect.x -= self.speed  # Рухаємо ворога з права на ліво
        global lost
        
        # Якщо ворог виходить за межі екрану з лівої сторони, повертається на праву сторону
        if self.rect.x < -80:
            self.rect.x = win_width  # Вороги знову з'являються з правого краю
            self.rect.y = randint(50, win_height - 50)  # Випадкова вертикальна позиція для ворога
            lost += 1  # Збільшуємо лічильник пропущених ворогів

# Створення вікна
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# Створення спрайтів
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), randint(50, win_height - 50), 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

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

    if not finish:
        window.blit(background, (0, 0))

        # Показуємо рахунок
        score_text = font.Font(None, 36).render(f"Пропущено: {lost}", 1, (255, 255, 255))
        window.blit(score_text, (10, 20))

        # Оновлюємо спрайти
        ship.update()
        monsters.update()

        # Малюємо спрайти
        ship.reset()
        monsters.draw(window)

        # Перевірка зіткнення між монстрами і гравцем (для програшу)
        if sprite.spritecollide(ship, monsters, False):
            finish = True
            window.blit(lose_font, (200, 200))

        # Перемога, якщо пропущено 50 перешкод
        if lost >= goal:
            finish = True
            window.blit(win_font, (200, 200))

        display.update()

    time.delay(50)