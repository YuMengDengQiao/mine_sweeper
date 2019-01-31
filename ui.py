#coding: utf-8
import pygame
from pygame.locals import *

class Button(pygame.sprite.Sprite):
    def __init__(self, img_file, (x, y)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_file)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
 
    def update(self):
        pass

    def checkClick(self, button, pos):
        if button == 1:
            if pos[0] > self.rect.left and pos[0] < self.rect.right and \
               pos[1] < self.rect.bottom and pos[1] > self.rect.top:
                return True
            else: return False


      
