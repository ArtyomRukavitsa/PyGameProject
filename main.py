import os
import sys
import pygame
from random import randint, choice
from PyQt5.QtWidgets import QApplication, QInputDialog, QWidget, QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5 import uic
import time
import csv


# Константы
WIDTH = 1000
HEIGHT = 600
COUNT_OF_KILLS = 0
GRAVITY = 1
NAME = ''

# Создание групп для первого монстрика. Новые создаю в фукнции Level
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
monster_group = pygame.sprite.Group()
gameover_youwin_group = pygame.sprite.Group()
stars = pygame.sprite.Group()
screen_rect = (0, 0, WIDTH, HEIGHT)

# Список с изображенииями монстриков
PICTURES = ['monster1.png', 'monster2.png', 'monster3.png', 'monster4.png']

# Установка таймера
pygame.time.set_timer(pygame.USEREVENT, 1000)


# Функция, отвечающая за загрузку того или иного музыкального файла в mixer
def music(file):
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.mixer.music.load(file)


# Данная инициализация миксера идет для загрузки выстрела
# (иначе звук основной игры будет сбиваться)
music('data/gun_sound.wav')
gun_sound = pygame.mixer.Sound("data/gun_sound.wav")


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


# Класс, отвечающий за спрайты монстров
class Monster(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(monster_group, all_sprites)
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(x, y)
        self.mw = self.image.get_width()
        self.mh = self.image.get_height()
        self.rect = self.image.get_rect()
        # Данное условие нужно для расположения первого монстра на начальном экране
        if x != 750 and y != 0:
            self.x = randint(0, WIDTH - self.mw)
            self.y = randint(0, HEIGHT - self.mh - 150)
            self.rect = self.image.get_rect().move(self.x, self.y)
        else:
            self.rect = self.image.get_rect().move(750, 0)


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
                  "Для паузы нажимай правую стрелку",
                  'Для просмотра таблицы результатов жми Q']

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
                if event.key == pygame.K_q:
                    base = DataBase()
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
    screen.blit(text, (400, 20))


# Сколько осталось убить монстров
def leftkills(count):
    font = pygame.font.SysFont('Verdana', 20)
    if count >= 0:
        text = font.render(f"Осталось убить: {count}", 1, (100, 255, 100))
    else:
        text = font.render(f"Осталось убить: 0", 1, (100, 255, 100))
    screen.blit(text, (750, 20))


# Функция отвечает за выстрел
def blood(x, y):
    image = load_image("blood.png")
    gun_sound.play()
    pygame.mixer.music.play()
    imagew = image.get_width()
    imageh = image.get_height()
    screen.blit(image, (x - imagew / 2, y - imageh / 2))
    pygame.display.update()
    time.sleep(0.1)


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

    music('data/main_sound.mp3')
    pygame.mixer.music.play(-1)

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
                            blood(monster_list[i].x + monster_list[i].mw / 2,
                                       monster_list[i].y + monster_list[i].mh / 2)
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
                pygame.mixer.music.stop()
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


# Запись результатов в таблицу
def my_writer(reader, new_row):
    with open('data/results.csv', 'w', newline='\n', encoding='utf8') as csvfile:
        csvfile.write('')
        row = f'{reader[0][0]};{reader[0][1]}\n'
        csvfile.write(row)
        for row in reader[1:]:
            row = f'{row[0]};{str(row[1])}\n'
            csvfile.write(row)
        if new_row != ' ':
            csvfile.write(new_row)


# Считывание данных таблицы
def results(NAME, COUNT_OF_KILLS):
    flag = 'No'
    # Считывание данных
    with open('data/results.csv', encoding="utf8") as csvfile:
        reader = list(csv.reader(csvfile, delimiter=';', quotechar='"'))
    # Преобразуем кол-во монстров в тип int
    for elem in reader[1:]:
        elem[1] = int(elem[1])
    for elem in reader[1:]:
        # Если победивший есть в csv-файле, то в методе my_writer идет запись
        # количества убитых монстров в общем + за эту игру
        if elem[0] == NAME:
            flag = 'Yes'
            elem[1] += COUNT_OF_KILLS
            my_writer(reader, ' ')
            break
    # Победившего в таблице не оказалось. Записываем его имя и количество убийств в файл
    if flag == 'No':
        my_writer(reader, f'{NAME};{COUNT_OF_KILLS}\n')


# Диалоговое окно
class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global NAME
        while NAME == '':
            NAME, okBtnPressed = QInputDialog.getText(self,
                                                      "Введите имя", "Как тебя зовут?")
        if okBtnPressed:
            return


# Класс, отвечающий за открытие таблицы результатов
class DataBase(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/table.ui', self)
        self.loadTable('data/results.csv')
        self.show()

    # Красим имена и результат топ-3 игроков
    def colorRow(self, row, color):
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.item(row, i).setBackground(color)

    # Вывод игроков
    def loadTable(self, name):
        with open(name, encoding="utf8") as csvfile:
            reader = list(csv.reader(csvfile, delimiter=';', quotechar='"'))
            title = reader[0]
            # Сортировка по результату
            reader = sorted(reader[1:], key=lambda x: -int(x[1]))

            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(reader):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(elem))
                if i < 3:
                    self.colorRow(i, QColor(randint(0, 255), randint(0, 255), randint(0, 255)))

        self.tableWidget.resizeColumnsToContents()


# Класс для отображения частиц
class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера

    def __init__(self, name, pos, dx, dy):
        super().__init__(stars)
        fire = [load_image(name)]
        for scale in (5, 10, 20):
            fire.append(pygame.transform.scale(fire[0], (scale, scale)))
        self.image = choice(fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


# Создание частиц
def create_particles(position, win):
    # количество создаваемых частиц
    particle_count = 120
    # возможные скорости
    numbers = range(-15, 16)
    if win:
        name = 'star.png'
    else:
        name = 'sad.png'
    for _ in range(particle_count):
        Particle(name, position, choice(numbers), choice(numbers))


# Фукнция, отвечающая за проигрышное окончание игры: запись результатов,
# отображение фоновой картинки и частицы - грустные смайлики
def new_gameover():
    time.sleep(1)
    results(NAME, COUNT_OF_KILLS)
    gameover = load_image('gameover.png')
    pygame.display.update()

    # Загрузка музыки и ее цикличный проигрыш
    music('data/lost.mp3')
    pygame.mixer.music.play(-1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                # создаём частицы по щелчку мыши
                create_particles([randint(0, WIDTH), randint(0, HEIGHT)], False)
        screen.fill(pygame.Color("white"))
        screen.blit(gameover, (0, 0))
        stars.draw(screen)
        stars.update()
        pygame.display.flip()
        clock.tick(20)


# Фукнция, отвечающая за проигрышное окончание игры: запись результатов,
# отображение фоновой картинки и частицы - звездочки
def new_you_win():
    time.sleep(1)
    results(NAME, COUNT_OF_KILLS)
    win = load_image('youwin.png')
    pygame.display.update()

    #  Загрузка музыки и ее цикличный проигрыш
    music('data/win.mp3')
    pygame.mixer.music.play(-1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                create_particles([randint(0, WIDTH), randint(0, HEIGHT)], True)

        screen.fill(pygame.Color("white"))
        screen.blit(win, (0, 0))
        stars.draw(screen)
        stars.update()
        pygame.display.flip()
        clock.tick(20)


if __name__ == '__main__':
    # Диалоговое окно с вводом имени
    app = QApplication(sys.argv)
    ex = Example()
    # Создание экрана
    pygame.init()
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
        time.sleep(5) # почему отсчет идет сразу, получается (15 - 5) = 10 секунд
        result2 = Level('background2.png', 1, 25, 20) # 3 15 10
        COUNT_OF_KILLS += result2[1]
        if result2[0] == 0:
            nextlevel()
            time.sleep(5)  # почему отсчет идет сразу, получаетсч 15-5 секунд
            result3 = Level('background3.png', 1, 15, 20) # 3 15 40
            COUNT_OF_KILLS += result3[1]
            if result3[0] == 0:
                new_you_win()
            else:
                new_gameover()
        else:
            new_gameover()
    else:
        new_gameover()
