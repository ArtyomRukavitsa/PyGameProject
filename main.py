import os
import sys
import pygame
from random import randint, random
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
import time

# Константы
FPS = 50
WIDTH = 1000
HEIGHT = 600
COUNT_OF_KILLS = 0

all_sprites = pygame.sprite.Group()
monster_group = pygame.sprite.Group()
PICTURES = ['monster1.png', 'monster2.png', 'monster3.png', 'monster4.png']

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
    #image = image.convert_alpha()

    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


# Фукнция, отвечающая за выход из программы
def terminate():
    pygame.quit()
    sys.exit()


# Сколько убито монстров
def nextlevel():
    font = pygame.font.SysFont('Verdana', 100)
    text = font.render("УРОВЕНЬ ПРОЙДЕН", 1, (100, 255, 100))
    screen.blit(text, (500, 300))
    time.sleep(5)


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
            #while not pygame.sprite.spritecollide(self, monster_group, False) != 1:
            self.x = randint(0, WIDTH - self.mw)
            self.y = randint(0, HEIGHT - self.mh - 150)
            self.rect = self.image.get_rect().move(self.x, self.y)
        else:
            self.rect = self.image.get_rect().move(750, 0)


# Класс, отвечающий за курсор (прицел)
class Arrow(pygame.sprite.Sprite):
    image = load_image("прицел2.jpg")

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
                    #Arrow(all_sprites)
                    return
        monster_group.draw(screen)
        pygame.display.flip()
        clock.tick()


# Сколько секунд осталось
def mytime(seconds):
    font = pygame.font.SysFont('Verdana', 20)
    text = font.render(f"Осталось секунд: {seconds}", 1, (100, 255, 100))
    screen.blit(text, (20, 20))


# Сколько убито монстров
def killscount(count):
    font = pygame.font.SysFont('Verdana', 20)
    text = font.render(f"Убийств: {count}", 1, (100, 255, 100))
    screen.blit(text, (350, 20))


# Сколько осталось убить монстров
def leftkills(count):
    font = pygame.font.SysFont('Verdana', 20)
    text = font.render(f"Осталось убить: {count}", 1, (100, 255, 100))
    screen.blit(text, (800, 20))


# Первый уровень игры
def Level(background, n, seconds, countOfMonsters):
    monster_list = []
    for el in monster_group:
        monster_group.remove(el)
    for i in range(n):
        monster = Monster(PICTURES[randint(0, 3)], 100, 100)
        monster_list.append(monster)
    fon = pygame.transform.scale(load_image(background), (WIDTH, HEIGHT))
    gun = load_image('gun3.png')
    arrow = load_image("arrow.png")
    count = 0
    #seconds = 10
    #arrow = Arrow(all_sprites)
    while True:
        x, y = pygame.mouse.get_pos()
        screen.blit(fon, (0, 0))
        for i in range(n):
            screen.blit(monster_list[i].image,
                        (monster_list[i].x, monster_list[i].y))

        screen.blit(gun, (x, 450)) # или х оставить неизменным?
        # что делать с стрелкой?
        screen.blit(arrow, (x - arrow.get_width() / 2, y - arrow.get_height() / 2))
        arrow_r = pygame.Rect(x - arrow.get_width() / 2, y - arrow.get_height() / 2, arrow.get_width(),
                                      arrow.get_height())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                all_sprites.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # продумать столкновения (+ добавить их в функцию?)
                for i in range(n):
                    if arrow_r.colliderect(monster_list[i]):
                        all_sprites.remove(monster_list[i])
                        monster_group.remove(monster_list[i])
                        del monster_list[i]
                        monster = Monster(PICTURES[randint(0, 1)], 100, 100)
                        monster_list.append(monster)
                        count += 1
            if event.type == pygame.USEREVENT:
                seconds -= 1
        mytime(seconds)
        killscount(count)
        leftkills(countOfMonsters - count)
        if seconds == 0:
            if count >= countOfMonsters:
                return 0, count
            else:
                return 1, count
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.update()
        clock.tick(30)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        i, okBtnPressed = QInputDialog.getText(self, "Введите имя",
                                               "Как тебя зовут?")
        if okBtnPressed:
            NAME = i
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    # Создание экрана, групп, параметров
    pygame.init()
    # pygame.key.set_repeat(200, 70)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    # Запуск заставки, далее первого уровня
    start_screen()
    result = Level('background1.png', 2, 20, 20) # начинаем игру
    COUNT_OF_KILLS += result[1]
    if result[0] == 0:
        nextlevel()
        Level('background2.png', 3, 10, 30)
    else:
        print('lost')

