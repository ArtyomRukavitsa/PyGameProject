import os
import sys
import pygame
from random import randint
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QWidget, QApplication
import time

# Константы
FPS = 50 # нужна ли? подумать!
WIDTH = 1000
HEIGHT = 600
COUNT_OF_KILLS = 0

# Создание групп для первого монстрика. Новые создаю в фукнции Level
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
monster_group = pygame.sprite.Group()
gameover_youwin_group = pygame.sprite.Group()

# Список с изображенииями монстриков
PICTURES = ['monster1.png', 'monster2.png', 'monster3.png', 'monster4.png']

# Установка таймера
pygame.time.set_timer(pygame.USEREVENT, 1000)


# Функция, отвечающая за загрузку того или иного музыкального файла в mixer
def music(file):
    pygame.mixer.pre_init(44100, -16, 2, 2048)
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


# Текст "уровень пройден"
def nextlevel():
    font = pygame.font.SysFont('Verdana', 60)
    text = font.render("УРОВЕНЬ ПРОЙДЕН", 1, (100, 255, 100))
    screen.blit(text, (200, 300))
    pygame.display.update()


class Gameover(pygame.sprite.Sprite):
    image = load_image("gameover.png")

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite
        super().__init__(group)
        self.image = Gameover.image
        self.rect = self.image.get_rect()
        self.rect.left = -2000
        self.rect.top = 0

    def update(self):
        v = 200
        #if self.rect.left < 0:
        self.rect.left += v * clock.tick() / 1000 # v * t в секундах


def set_gameover_background():
    Gameover(gameover_youwin_group)
    print(gameover_youwin_group)
    pygame.display.update()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
        screen.fill(pygame.Color("black"))
        gameover_youwin_group.update()
        gameover_youwin_group.draw(screen)
        pygame.display.flip()


class Win(pygame.sprite.Sprite):
    image = load_image("youwin.png")

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite
        super().__init__(group)
        self.image = Win.image
        self.rect = self.image.get_rect()
        self.rect.left = -2000
        self.rect.top = 0

    def update(self):
        v = 200
        if self.rect.left < 0:
            self.rect.left += v * clock.tick() / 1000 # v * t в секундах


def set_youwin_background():
    Win(gameover_youwin_group)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(pygame.Color("white"))
        gameover_youwin_group.update()
        gameover_youwin_group.draw(screen)
        pygame.display.flip()

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
                  "Нажимай на пробел, время не ждет!",
                  "Для паузы нажимай правую стрелку"]

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


# Текст паузы
def pausetext():
    font = pygame.font.SysFont('Verdana', 60)
    text = font.render("ПАУЗА", 1, (100, 255, 100))
    screen.blit(text, (400, 30))


# Универсальная функция для уровней игры
def Level(background, n, seconds, countOfMonsters):
    # background - изображение файла (*.png)
    # n - количество монстров, возможных на экране
    # seconds - количество секунд на уровень
    # conunOfMonsters - сколько монстров нужно убить
    monster_list = []
    monster_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    for i in range(n):
        monster = Monster(PICTURES[randint(0, 3)], 100, 100)
        monster_list.append(monster)
    fon = pygame.transform.scale(load_image(background), (WIDTH, HEIGHT))
    gun = load_image('gun3.png')
    arrow = load_image("arrow_small.png")
    count = 0
    #arrow = Arrow(all_sprites)
    pause, running = False, True
    state = running

    # pygame.mixer.music.play(-1)

    while True:
        if state == running:
            # флаг нужен для того, чтобы пресекать возможность убийства сразу двух или даже трех монстров
            flag = 0
            x, y = pygame.mouse.get_pos()
            screen.blit(fon, (0, 0))
            for i in range(n):
                screen.blit(monster_list[i].image,
                            (monster_list[i].x, monster_list[i].y))

            screen.blit(gun, (x, 450))  # или х оставить неизменным?
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
                        if arrow_r.colliderect(monster_list[i]) and flag == 0:
                            all_sprites.remove(monster_list[i])
                            monster_group.remove(monster_list[i])
                            del monster_list[i]
                            monster = Monster(PICTURES[randint(0, 3)], 100, 100)
                            monster_list.append(monster)
                            count += 1
                            flag = 1
                if event.type == pygame.USEREVENT:
                    seconds -= 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    state = pause
                    #music('data/lost.mp3')
            mytime(seconds)
            killscount(count)
            leftkills(countOfMonsters - count)
            if seconds == 0:
                pygame.display.update()
                if count >= countOfMonsters:
                    return 0, count
                else:
                    return 1, count
            all_sprites.draw(screen)
            all_sprites.update()
        elif state == pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    state = running
            pausetext()
            #music('data/lost.mp3')
            #pygame.mixer.music.play(-1)
        pygame.display.flip()
        #clock.tick(30)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        NAME = ''
        while NAME == '':
            NAME, okBtnPressed = QInputDialog.getText(self,
                                                      "Введите имя", "Как тебя зовут?")
            if okBtnPressed:
                return


if __name__ == '__main__':
    # Диалоговое окно с вводом имени
    app = QApplication(sys.argv)
    ex = Example()
    # Создание экрана
    pygame.init()
    # pygame.key.set_repeat(200, 70)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.mouse.set_visible(False)
    # Запуск заставки, далее первого уровня
    start_screen()
    result1 = Level('background1.png', 2, 20, 20)
    # Уровень возвращает два параметра: 0 - победа, 1 - поражение и
    # количество убитых монстров на уровне
    COUNT_OF_KILLS += result1[1]

    if result1[0] == 0:
        nextlevel()
        set_youwin_background()
        time.sleep(5) # почему отсчет идет сразу, получается (15 - 5) = 10 секунд
        result2 = Level('background2.png', 3, 15, 10) # 3 15 10
        COUNT_OF_KILLS += result2[1]
        if result2[0] == 0:
            nextlevel()
            time.sleep(5)  # почему отсчет идет сразу, получаетсч 15-5 секунд
            result3 = Level('background3.png', 3, 15, 10) # 3 15 40
            COUNT_OF_KILLS += result3[1]
            if result3[0] == 0:
                set_youwin_background()
            else:
                set_gameover_background()
        else:
            set_gameover_background()
    else:
        #terminate()
        #pygame.init()
        # pygame.key.set_repeat(200, 70)
        #screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.update()
        set_gameover_background()


