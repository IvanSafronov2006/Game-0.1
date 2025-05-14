import ctypes
import pygame

class Exception():
    def load_image(self, address):
        try:
            pygame.image.load(address)
            return address
        except:
            return str("images/test.png")