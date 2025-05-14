#from main import *
def object_function(id, object):
    if id == 3:
        addr = ['test_house_0003_1.png', 'test_house_0003_2.png']
        object.image = addr[(addr.index(object.image)+1)%2]

def nps_speak(id):
    if id == 2:
        print('Hello')
