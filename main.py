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
bg_color = (150, 150, 150)
tile_color = (100, 100, 100)
text_color = (255, 255, 255)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Financial Literacy Tic-Tac-Toe')

font = pygame.font.SysFont(None, 30)

class Elem():
    def __init__(self, image, coords):
        self.image = image
        self.rect = pygame.Rect(coords[0], coords[1], image.get_size()[0], image.get_size()[1])

    @staticmethod
    def mk_tile_surface(tile_dims, text, text_coords=None, bg_color=tile_color, fg_color=text_color):
        tile_image = pygame.Surface(tile_dims)
        tile_image.fill(bg_color)
        text_image = font.render(text, True, fg_color)
        if not text_coords:
            text_coords = ((tile_dims[0] - text_image.width) / 2, (tile_dims[1] - text_image.height) / 2)
        tile_image.blit(text_image, text_coords)

        return tile_image

class Button(Elem):
    def __init__(self, image, coords):
        super().__init__(image, coords)

    def eval_click(self, coords):
        return self.rect.collidepoint(coords)

class GameState():
    def __init__(self):
        self.current_screen = 0
        self.screen_list = [
            self.main_screen,
        ]
        self.run = True
        self.elems = {}
        self.click_elem = None

    def main(self, screen):
        self.screen_list[self.current_screen](screen)
        return self.run

    def disp_scene(self):
        for category in self.elems:
            for elem in self.elems[category]:
                screen.blit(self.elems[category][elem].image, self.elems[category][elem].rect.topleft)

    def start_click(self):
        mouse_pos = pygame.mouse.get_pos()
        for elem in self.elems["buttons"]:
            if self.elems["buttons"][elem].eval_click(mouse_pos):
                self.click_elem = elem

    def update_click(self):
        if not self.click_elem: return
        mouse_pos = pygame.mouse.get_pos()
        if not self.elems["buttons"][self.click_elem].eval_click(mouse_pos):
            self.click_elem = None

    def main_screen_init(self):
        self.elems = {
                "buttons": {
                    "quit": Button(Elem.mk_tile_surface((160, 40), "Quit"), ((screen_width - 160) / 2, 600)),
                    "start": Button(Elem.mk_tile_surface((160, 40), "Start"), ((screen_width - 160) / 2, 450)),
                },
                "text": {
                    "title": Elem(Elem.mk_tile_surface((450, 40), "Financial Literacy Tic-Tac-Toe", bg_color=bg_color), ((screen_width - 450) / 2, 300)),
                },
        }
        self.current_screen = 0

    def main_screen(self, screen):
        self.disp_scene()
        self.update_click()

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.run = False
                case pygame.MOUSEBUTTONDOWN:
                    self.start_click()
                case pygame.MOUSEBUTTONUP:
                    match self.click_elem:
                        case "quit":
                            self.run = False
                        case "start":
                            self.board_screen_init()
                    self.click_elem = None



state = GameState()
state.main_screen_init()

run = True
while run:
    clock.tick(fps)
    screen.fill(bg_color)

    run = state.main(screen)

    pygame.display.update()
