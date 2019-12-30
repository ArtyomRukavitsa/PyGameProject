import os
import sys
import pygame
from random import randint, random

# Константы
FPS = 50
WIDTH = 1000
HEIGHT = 600

# Создание экрана, групп, параметров
pygame.init()
pygame.key.set_repeat(200, 70)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
monster_group = pygame.sprite.Group()
PICTURES = ['monster.png', 'monster1.png']

pygame.time.set_timer(pygame.USEREVENT, 1000)


# Функция, отвечающая за загрузку того или иного файла в mixer
def music(file):
    pygame.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer to avoid sound lag
    pygame.mixer.init()
    pygame.mixer.music.load(file)


# Функция, отвечающая за загрузку изображения
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


# Фукнция, отвечающая за выход из программы
def terminate():
    pygame.quit()
    sys.exit()


# Класс, отвечающий за спрайты монстров
class Monster(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(monster_group, all_sprites)
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(x, y)
        self.mw = self.image.get_width()
        self.mh = self.image.get_height()
        # Данное условие нужно для расположения первого монстра на начальном экране
        if x != 750 and y != 0:
            self.x = randint(0, WIDTH - self.mw)
            self.y = randint(0, HEIGHT - self.mh)
            self.rect = self.image.get_rect().move(self.x, self.y)
        else:
            self.rect = self.image.get_rect().move(750, 0)


# Класс, отвечающий за курсор (прицел)
class Arrow(pygame.sprite.Sprite):
    image = load_image("прицел2.jpg", -1)

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно !!!
        super().__init__(group)
        self.image = Arrow.image
        self.rect = self.image.get_rect()

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION:
            self.rect.x, self.rect.y = args[0].pos


# Начальный экран
def start_screen():
    intro_text = ["ОХОТА НА МОНСТРОВ!", "",
                  "Правила игры",
                  "Сегодня чудесный день для охоты на монстров, ",
                  "не так ли?",
                  "Убивай монстров на каждом уровне, но внимание!",
                  "с каждым уровнем все меньше времени и больше убийств",
                  "Ты со мной?",
                  "Нажимай Enter, время не ждет!"]

    fon = pygame.transform.scale(load_image('fon1.jpg'), (WIDTH, HEIGHT))
    monster = Monster('monster1.png', 750, 0)
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('Verdana', 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, (139, 0, 139))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    # Загрузка музыки и ее цикличное проигрывание
    music('data/start.mp3')
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # удаляю монстрика из всех групп, чтобы не появлялся потом
                    monster_group.remove(monster)
                    all_sprites.remove(monster)
                    # Остановка стартовой музыки
                    pygame.mixer.music.stop()
                    Arrow(all_sprites)
                    FirstLevel() # начинаем игру
        monster_group.draw(screen)
        pygame.display.flip()
        clock.tick()


# Первый уровень игры
def FirstLevel():
    monster_list = []
    for i in range(2):
        monster = Monster(PICTURES[randint(0, 1)], 100, 100)
        monster_list.append(monster)

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    gun = load_image('gun3.png')
    while True:
        screen.blit(fon, (0, 0))
        for i in range(2):
            screen.blit(monster_list[1].image,
                        (monster_list[1].x, monster_list[1].y))

        screen.blit(gun, (400, 450))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                all_sprites.update(event)

        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.update()


pygame.mouse.set_visible(False)
start_screen()
