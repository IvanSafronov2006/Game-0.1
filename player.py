import time
import math
import random
import pygame
from fields import *
import json
from main import *
from constants import *
from damage import *

class Persons():
    def __init__(self, my_id, basa_cursor):
        self.my_id = my_id
        self.basa_cursor = basa_cursor
        me = self.basa_cursor.execute('''SELECT * FROM Person WHERE id=(?)''', (self.my_id,)).fetchall()[0]
        self.ammunition = {}
        for i in enumerate(me[6:12]):
            sp = ['head', 'helmet', 'body', 'cloak', 'belt', 'legs']
            my_ammunition = self.basa_cursor.execute('''SELECT * FROM Ammunitions WHERE id=(?)''', (i[1],)).fetchall()[   0]
            self.ammunition[sp[i[0]]] = my_ammunition[1:]
        self.space_x = me[4]
        self.space_y = me[5]
        self.size_h = SIZE_PERSON[0]
        self.size_w = SIZE_PERSON[1]
        self.now_position = ["normal", 15]
        self.teammates = []
        self.move_history = []
        self.hp = 100

    def save(self):
        self.basa_cursor.execute('''UPDATE people SET hp = (?) WHERE id = (?)''', (self.hp, self.my_id))

    def can_speak(self, x, y, field):
        if ((x - 10 <= self.space_x + SIZE_PERSON[0]//2 <= x + SIZE_PERSON[0] + 10) and
                (y - 10 <= self.space_y + SIZE_PERSON[1]//2 <= y + SIZE_PERSON[1] + 10)):
            check = self.my_id
            field.set_speak(check)
            return check
        else:
            field.set_speak(0)
            return 0

    def decorate(self):
        return self.move_history

    def __add__(self, second):
        self.teammates.append(second.id)
        print(self.temmates)

    def __sub__(self, second):
        del self.teammates[self.teammates.index(second.id)]
        print(self.temmates)

    def next_frame(self):
        self.now_position[1] = max(1, round(((self.now_position[1]) + NEXT_SPEED)%32, 1))

class Player(Persons):
    def __init__(self, my_id, basa_cursor):
        super().__init__(my_id, basa_cursor)
        self.screen_x = WIDHT // 2
        self.screen_y = HEIGHT // 2
        self.speed = 1
        self.now_position = ["normal", 15]

    def set_location(self, x, y):
        self.space_x = x
        self.space_y = y

    def set_route(self, direction):
        if direction == self.now_position[0]:
            if direction == "normal":
                if self.now_position[1] == STATIC_NORMAL_FRAME:
                    self.now_position[1] = round((self.now_position[1]) + NEXT_SPEED, 1)
                else:
                    self.now_position[1] = round((self.now_position[1]) + NEXT_SPEED, 1)
            if direction in ['left', 'right']:
                self.now_position[1] = round((self.now_position[1]) + NEXT_SPEED*2, 1)
            if self.now_position[1] > max(list(COUNT_FRAMES[self.now_position[0]].values())):
                self.now_position[1] = 1
        else:
            self.now_position[1] = 1
            self.now_position[0] = direction

    def move(self, x, y, field):
        if field.can_move(self.space_x+x, self.space_y):
            self.move_history.append([x, y])
            if (abs(self.screen_x + x - WIDHT//2) <= MOVE_RANGE-0.5) and (x!=0):
                if ((self.screen_x >= WIDHT//2) and (x >= 0)) or (((self.screen_x <= WIDHT//2))and(x<=0)):
                    field_move =  (abs(self.screen_x + x - WIDHT//2)/MOVE_RANGE)*abs(x)*(-abs(x)/x)
                    hero_move = (1 - abs(self.screen_x + x - WIDHT//2)/MOVE_RANGE)*abs(x)*(abs(x)/x)
                if ((self.screen_x > WIDHT//2) and (x < 0)) or (((self.screen_x < WIDHT//2))and(x>0)):
                    field_move =  0
                    hero_move = x
                self.screen_x += hero_move
                self.space_x += x
                field.move(field_move, 0)
            else:
                field.move(x*-1, 0)
                self.space_x += x
        if field.can_move(self.space_x, self.space_y+y):
            self.move_history.append([x, y])
            if (abs(self.screen_y+y - HEIGHT // 2) <= MOVE_RANGE-0.5) and (y!=0):
                if ((self.screen_y >= HEIGHT // 2) and (y >= 0)) or (((self.screen_y <= HEIGHT // 2)) and (y <= 0)):
                    field_move = (abs(self.screen_y + y - HEIGHT // 2) / MOVE_RANGE) * abs(y) * (-abs(y) / y)
                    hero_move = (1 - abs(self.screen_y + y - HEIGHT // 2) / MOVE_RANGE) * abs(y) * (abs(y) / y)
                if ((self.screen_y >= HEIGHT // 2) and (y <= 0)) or (((self.screen_y <= HEIGHT // 2)) and (y >= 0)):
                    field_move = 0
                    hero_move = y
                self.screen_y += hero_move
                self.space_y += y
                field.move(0, field_move)
            else:
                field.move(0, -y)
                self.space_y += y
        return field


