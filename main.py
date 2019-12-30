import os
import sys
import pygame
from random import randint, random


FPS = 50
WIDTH = 1000
HEIGHT = 600

pygame.init()
pygame.key.set_repeat(200, 70)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
monster_group = pygame.sprite.Group()


file = 'data/start.mp3'
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.mixer.init()
pygame.mixer.music.load(file)


class Monster(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(monster_group, all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(x, y)
        self.mw = self.image.get_width()
        self.mh = self.image.get_height()
        self.x = randint(0, WIDTH - self.mw)
        self.y = randint(0, HEIGHT - self.mh)
        if self.x != 750 and self.y != 0:
            self.rect = self.image.get_rect().move(x, y)
        else:
            self.rect = self.image.get_rect().move(750, 0)

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


def terminate():
    pygame.quit()
    sys.exit()


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
    monster = Monster(load_image('monster1.png', -1), 750, 0)
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

    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # monster_group.remove(monster)
                    return  # начинаем игру
        monster_group.draw(screen)
        pygame.display.flip()
        clock.tick()


start_screen()
