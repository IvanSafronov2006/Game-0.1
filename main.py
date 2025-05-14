import time
import threading
import math
import random
import pygame
import ctypes
import os
from exception import Exception
import sqlite3
from qt import *
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidget, QTableWidgetItem
from fields import *
from player import *
from constants import *
from objects_function import *

def day_night():
    global day
    while True:
        time.sleep(10)
        day = not(day)
        print('change')

def start_play(screen, hero):
    global field
    time_to_normal_route = FPS//2
    running = True
    while running:
        clock = pygame.time.Clock()
        clock.tick(FPS) #FPS
        redraw_game_window(screen, hero)
        # Анимация NPC
        for i in field.npc:
            i.next_frame()
        # Блок движения
        keys = pygame.key.get_pressed()
        for i in pygame.event.get():
            if (i.type == pygame.KEYDOWN and i.key == pygame.K_e):
                if field.interaction:
                    object_function(field.interaction, field.interaction_object)
            if (i.type == pygame.KEYDOWN and i.key == pygame.K_q):
                if field.speak:
                    nps_speak(field.speak)
        for i in [[1, 0, 0, 0, "left", (-1, 0)], [0, 1, 0, 0, "right", (1, 0)],
                  [0, 0, 1, 0, "up", (0, -1)], [0, 0, 0, 1, "down", (0, 1)],
                  [1, 0, 1, 0, "left_up", (-0.7, -0.7)], [1, 0, 0, 1, "left_down", (-0.7, 0.7)],
                  [0, 1, 1, 0, "right_up", (0.7, -0.7)], [0, 1, 0, 1, "right_down", (0.7, 0.7)],
                  [0, 0, 0, 0, "normal", (0, 0)]]:
            if [keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s]] == i[:4]:
                if i[4] != 'normal':
                    time_to_normal_route = FPS//2
                else:
                    time_to_normal_route -= 1
                if i[4] == 'normal':
                    if time_to_normal_route <= 0:
                        hero.set_route(i[4])
                else:
                    hero.set_route(i[4])
                if i[4] != 'normal':
                    field = hero.move(int(hero.size_h // 16) * hero.speed * i[5][0],
                            int(hero.size_h // 16) * hero.speed * i[5][1], field)
                break


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('1')
                running = False
                pygame.quit()

def redraw_game_window(screen, hero):
    global field, day
    #Заливка экрана
    if day:
        screen.fill((60, 90, 60))
    else:
        screen.fill((20, 40, 20))
    # Отрисовка предметов
    draw_e = False
    for object in field.objects:
        if (object._type in INTERACTION_OBJECT) and (object.can_interaction(hero.space_x, hero.space_y, field)):
            draw_e = True
        address = object.address()
        sprite = pygame.image.load(address)
        screen.blit(sprite, (object.coord_x+field.get_center()[0], object.coord_y+field.get_center()[1]))
    # Отрисовка npc
    draw_q = False
    for npc in field.npc:
        if npc.can_speak(hero.space_x, hero.space_y, field) != 0:
            draw_q = True
        for object in ['head', 'body', 'legs', 'belt', 'helmet', 'cloak']:
            address = str("images/hero/" + object + "/" + npc.ammunition[object][0] + '/normal/' +
                           "_".join([npc.ammunition[object][1],
                                     str(min(int(npc.now_position[1]), COUNT_FRAMES[npc.now_position[0]][object])).zfill(3)]) + ".png")
            sprite = pygame.image.load(Exception().load_image(address))
            sprite = pygame.transform.scale(sprite, (int(npc.size_h), int(npc.size_w)))
            sprite = pygame.transform.flip(sprite, False, False)
            screen.blit(sprite, (npc.space_x+field.get_center()[0], npc.space_y+field.get_center()[1]))
    # Отрисовка персонажа
    #pygame.draw.rect(screen, 'red', pygame.Rect(int(hero.screen_x), int(hero.screen_y),32, 48))
    for object in ['head', 'body', 'legs', 'belt', 'helmet', 'cloak']:
        rotate = False
        if 'right' in hero.now_position[0]:
            hero.now_position[0] = hero.now_position[0].replace('right', 'left')
            rotate = True
        address = str("images/hero/" + object + "/" + hero.ammunition[object][0] +
                      '/normal/test_'+object+'_001.png')
        #address = str("images/hero/" + object + "/" + hero.ammunition[object][0] +
        #              '/' + hero.now_position[0] + '/' +
        #              "_".join([hero.ammunition[object][1],
        #                        str(min(int(hero.now_position[1]), COUNT_FRAMES[hero.now_position[0]][object])).zfill(3)]) + ".png")
        if rotate:
            hero.now_position[0] = hero.now_position[0].replace('left', 'right')
        sprite = pygame.image.load(Exception().load_image(address))
        sprite = pygame.transform.scale(sprite, (int(hero.size_h), int(hero.size_w)))
        sprite = pygame.transform.flip(sprite, rotate, False)
        screen.blit(sprite, (hero.screen_x, hero.screen_y))
    if draw_e:
        sprite = pygame.image.load("images/click_e.png")
        screen.blit(sprite, (int(hero.screen_x+9), int(hero.screen_y-16)))
    if draw_q:
        sprite = pygame.image.load("images/click_q.png")
        screen.blit(sprite, (int(hero.screen_x+20), int(hero.screen_y-10)))

    pygame.display.update()

# Создание персонажа

# Создание поля
basa_d = sqlite3.connect('basa.db')
basa_cursor = basa_d.cursor()
secondary_thread = threading.Thread(target=day_night)
secondary_thread.start()
if __name__ == '__main__':
    day = True
    field = Field(basa_cursor)
    id_player = 1
    hero = Player(id_player, basa_cursor)
    pygame.init() #инициализация pygame
    # Оконный режим
    screen = pygame.display.set_mode((WIDHT, HEIGHT))
    # Полноэкранный режим
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Подгрузка иконки и названия
    pygame.display.set_caption("РПГ")
    icon = pygame.image.load("images/pictures/icon.png")
    pygame.display.set_icon(icon)

    screen.fill((30, 60, 30))
    ''''# Создание окон
    app = QApplication(sys.argv)
    login_window = Login_window(basa_d)
    login_window.setObjectName("Вход")
    login_window.setStyleSheet("#Вход{border-image:url(photo.png)}")
    # Окно регистрации
    registration_window = Registration_window(basa_d)
    registration_window.setObjectName("Регистрация")
    registration_window.setStyleSheet("#Регистрация{border-image:url(photo.png)}")
    login_window.show()'''
    # Начало игры
    start_play(screen, hero)
    basa_d = sqlite3.connect('basa.db')
    basa_cursor = basa_d.cursor()

    print(login_window)
    basa_d.commit()
    basa_d.close()
    basa_cursor.close()
