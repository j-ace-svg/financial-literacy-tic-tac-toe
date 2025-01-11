#!/usr/bin/env python

import pygame
from pygame.locals import *
import random
import os

pygame.init()

fps = 60
clock = pygame.Clock()

screen_width = 864
screen_height = 936
bg = (255, 255, 255)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Financial Literacy Tic-Tac-Toe')

class Button():
    def __init__(self, image, coords):
        self.image = image
        self.rect = pygame.Rect(coords[0], coords[1], image.get_size()[0], image.get_size()[1])
       
    def eval_click(self, coords):
        return self.rect.collidepoint(rect)

class GameState():
    def __init__(self):
        self.current_screen = 0
        self.screen_list = [
            self.main_screen,
        ]
        self.run = True
        self.elems = {}
    
    def main(self, screen):
        self.screen_list[self.current_screen](screen)
        return self.run

    def main_screen_init(self, screen):
        quit_button_image = pygame.Surface(40, 20)
        quit_button_image.fill((150, 150, 150))
        self.elems = {
                "quit": Button(quit_button_image, (30, 30)),
        }

    def main_screen(self, screen):
        for event in pygame.event.get():
            match event:
                case pygame.QUIT:
                    self.run = False
                case pygame.MOUSEBUTTONDOWN:
                    if self.elems["quit"].eval_click(get_pos()):
                        self.run = False



state = GameState()

run = True
while run:
    clock.tick(fps)
    screen.fill(bg)

    run = state.main(screen)

    pygame.display.update()
