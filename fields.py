from constants import *
from player import *


class Field():
    def __init__(self, basa_cursor):
        self.basa_cursor = basa_cursor
        self.spawn_point = [WIDHT//2, HEIGHT//2]
        self.center = [WIDHT//2, HEIGHT//2]
        objects_1 = list(self.basa_cursor.execute('''SELECT * FROM Object''').fetchall())
        npc_1 = list(filter(lambda x: x[0]!=1, list(self.basa_cursor.execute('''SELECT * FROM Person''').fetchall())))
        self.npc = []
        for i in npc_1:
            self.npc.append(Persons(i[0], basa_cursor))
        self.objects = []
        for i in objects_1:
            if i[1] == 0:
                self.objects.append(Object_not_through(i))
            elif i[1] == 1:
                self.objects.append(Object_through(i))
            elif i[1] == 2:
                self.objects.append(Object_with_interaction(i))
        self.interaction = 0
        self.speak = 0
        self.interaction_object = 0

    def set_interaction(self, id, object):
        self.interaction = id
        self.interaction_object = object

    def set_speak(self, id_person):
        self.speak = id_person


    def can_move(self, x, y):
        check = True
        for i in list(filter((lambda x: x._type in NOT_THROUGH_OBJECT), self.objects)):
            if ((i.coord_x + HERO_MERGER[0] <= x <= i.coord_x+i.size_x - HERO_MERGER[1]) and
                    (i.coord_y + HERO_MERGER[2] <= y <= i.coord_y+i.size_y- HERO_MERGER[3])):
                check = False
                break
            if ((i.coord_x + HERO_MERGER[0] <= x+SIZE_PERSON[0] <= i.coord_x+i.size_x - HERO_MERGER[1]) and
                    (i.coord_y + HERO_MERGER[2]<= y+SIZE_PERSON[1] <= i.coord_y+i.size_y- HERO_MERGER[3])):
                check = False
                break
            if ((i.coord_x + HERO_MERGER[0] <= x+SIZE_PERSON[0] <= i.coord_x+i.size_x-HERO_MERGER[1]) and
                    (i.coord_y + HERO_MERGER[2]<= y <= i.coord_y+i.size_y- HERO_MERGER[3])):
                check = False
                break
            if ((i.coord_x + HERO_MERGER[0] <= x <= i.coord_x+i.size_x-HERO_MERGER[1]) and
                    (i.coord_y + HERO_MERGER[2]<= y+SIZE_PERSON[1] <= i.coord_y+i.size_y- HERO_MERGER[3])):
                check = False
                break
        return check

    def move(self, x, y):
        self.center = [self.center[0] + x, self.center[1] + y]

    def get_center(self):
        return self.center

class Object():
    def __init__(self, sp):
        (self.id, self._type, self.stage, self.name, self.move, self.coord_x, self.coord_y,
         self.size_x, self.size_y, self.interaction, self.point_interaction_x, self.point_interaction_y, self.image) = sp

    def address(self):
        return str("images/objects/" +  self.name + '_'+str(self.id).zfill(4) + '/' +  self.image)


class Object_with_interaction(Object): #type=2
    def __init__(self, sp):
        super().__init__(sp)

    def can_interaction(self, x, y, field):
        if self.interaction == 0:
            return False
        else:
            if ((x-10 <= self.coord_x+self.point_interaction_x <= x+SIZE_PERSON[0]+10) and
                    (y-10 <= self.coord_y+self.point_interaction_y <= y+SIZE_PERSON[1]+10)):
                check = self.id
                field.set_interaction(check, self)
                return check
            else:
                field.set_interaction(0, 0)

class Object_through(Object): #type=1
    def __init__(self, sp):
        super().__init__(sp)

class Object_not_through(Object): #type=0
    def __init__(self, sp):
        super().__init__(sp)