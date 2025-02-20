#!/usr/bin/env python

import pygame
from pygame.locals import *
import random
import os
import read_file

pygame.init()

fps = 60
clock = pygame.Clock()

screen_width = 864
screen_height = 936
bg_color = (150, 150, 150)
tile_color = (100, 100, 100)
global_tile_color = (255, 255, 255)
text_color = (255, 255, 255)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Financial Literacy Tic-Tac-Toe')

font = pygame.font.SysFont(None, 30)

with open("questions.txt", "r") as questions_file:
    questions = read_file.read_questions_file(questions_file)

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
            text_coords = ((tile_dims[0] - text_image.get_width()) / 2, (tile_dims[1] - text_image.get_height()) / 2)
        tile_image.blit(text_image, text_coords)

        return tile_image

    def mk_tile_surface_wrap(tile_dims, text, text_rect=None, bg_color=tile_color, fg_color=text_color):
        tile_image = pygame.Surface(tile_dims)
        tile_image.fill(bg_color)
        tile_rect = tile_image.get_rect()
        if not text_rect:
            text_rect = pygame.Rect(tile_rect)
        text_image = pygame.Surface(text_rect.size)
        text_image.fill(bg_color)
        y = text_rect.top
        line_spacing = -2
        font_height = font.size("Tg")[1]

        while text:
            i = 1

            if y + font_height > text_rect.bottom:
                break

            while font.size(text[:i+1])[0] < text_rect.width and i < len(text):
                i += 1

            if i < len(text) or (" " in text and font.size(text[:i+1])[0] > text_rect.width):
                i = text.rfind(" ", 0, i) + 1

            letter_image = font.render(text[:i], True, fg_color)

            text_image.blit(letter_image, (text_rect.left, y))
            y += font_height + line_spacing

            text = text[i:]

        tile_image.blit(text_image, text_rect.topleft)

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
            self.primary_board_screen,
            self.secondary_board_screen,
            self.question_screen,
        ]
        self.run = True
        self.elems = {}
        self.click_elem = None
        self.primary_coord = (0, 0)
        self.secondary_coord = (0, 0)
        self.correct_answer = 0
        self.primary_board_state = [[0 for _ in range(3)] for _ in range(3)]
        self.secondary_board_state = [[[[0 for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]

        # Tiles
        self.grid_pad = 20
        self.tile_size = 160
        self.empty_tile = Elem.mk_tile_surface((self.tile_size, self.tile_size), "")

        icon_radius = 3 * self.tile_size / 8

        self.o_tile = self.empty_tile.copy()
        pygame.draw.circle(self.o_tile, text_color, (self.tile_size / 2, self.tile_size / 2), icon_radius, int(self.tile_size / 16))

        self.x_tile = self.empty_tile.copy()
        pygame.draw.line(self.x_tile, text_color, (self.tile_size - 2 * icon_radius, self.tile_size - 2 * icon_radius), (2 * icon_radius, 2 * icon_radius), int(self.tile_size / 16))
        pygame.draw.line(self.x_tile, text_color, (self.tile_size - 2 * icon_radius, 2 * icon_radius), (2 * icon_radius, self.tile_size - 2 * icon_radius), int(self.tile_size / 16))

    def main(self, screen):
        self.screen_list[self.current_screen](screen)
        return self.run

    def disp_scene(self):
        for category in self.elems:
            for elem in self.elems[category]:
                screen.blit(self.elems[category][elem].image, self.elems[category][elem].rect.topleft)

    def start_click(self, event):
        if not event.button == 1: return
        mouse_pos = pygame.mouse.get_pos()
        for elem in self.elems["buttons"]:
            if self.elems["buttons"][elem].eval_click(mouse_pos):
                self.click_elem = elem

    def end_click(self, event):
        if not event.button == 1: return
        self.click_elem = None

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
                    self.start_click(event)
                case pygame.MOUSEBUTTONUP:
                    match self.click_elem:
                        case "quit":
                            self.run = False
                        case "start":
                            self.primary_board_screen_init()
                    self.end_click(event)

    def primary_board_screen_init(self):
        sub_boards = [ [ None for primary_col in range(3) ] for primary_row in range(3) ]
        for primary_row in range(3):
            for primary_col in range(3):
                sub_board_large = Elem.mk_tile_surface((self.tile_size * 3 + self.grid_pad * 4, self.tile_size * 3 + self.grid_pad * 4), "", bg_color = global_tile_color)
                for secondary_row in range(3):
                    for secondary_col in range(3):
                        sub_board_large.blit(self.empty_tile if self.secondary_board_state[primary_row][primary_col][secondary_row][secondary_col] == 0 else self.x_tile, (secondary_col * (self.tile_size + self.grid_pad) + self.grid_pad, secondary_row * (self.tile_size + self.grid_pad) + self.grid_pad))

                sub_boards[primary_row][primary_col] = pygame.transform.scale(sub_board_large, (self.tile_size, self.tile_size))

        self.elems = {
                "buttons": {
                    (row, col): Button(
                    #    self.empty_tile if self.primary_board_state[row][col] == 0 else self.x_tile,
                        sub_boards[row][col],
                        (
                            (screen_width - self.tile_size) / 2 + (self.tile_size + self.grid_pad) * (col - 1),
                            (screen_height - self.tile_size) / 2 + (self.tile_size + self.grid_pad) * (row - 1),
                        ),
                     ) for row in range(3) for col in range(3)
                },
                "text": {
                    "title": Elem(Elem.mk_tile_surface((450, 40), "Financial Literacy Tic-Tac-Toe", bg_color=bg_color), ((screen_width - 450) / 2, 50)),
                },
        }
        self.current_screen = 1

    def primary_board_screen(self, screen):
        self.disp_scene()
        self.update_click()

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.run = False
                case pygame.MOUSEBUTTONDOWN:
                    self.start_click(event)
                case pygame.MOUSEBUTTONUP:
                    if self.click_elem:
                        self.primary_coord = self.click_elem
                        self.secondary_board_screen_init()
                    self.end_click(event)

    def secondary_board_screen_init(self):
        self.elems = {
                "buttons": {
                    (row, col): Button(
                        self.empty_tile if self.secondary_board_state[self.primary_coord[0]][self.primary_coord[1]][row][col] == 0 else self.x_tile,
                        (
                            (screen_width - self.tile_size) / 2 + (self.tile_size + self.grid_pad) * (col - 1),
                            (screen_height - self.tile_size) / 2 + (self.tile_size + self.grid_pad) * (row - 1),
                        ),
                    ) for row in range(3) for col in range(3)
                },
                "text": {
                    "title": Elem(Elem.mk_tile_surface((450, 40), questions[self.primary_coord[0]][self.primary_coord[1]]["title"], bg_color=bg_color), ((screen_width - 450) / 2, 50)),
                },
        }
        self.current_screen = 2

    def secondary_board_screen(self, screen):
        self.disp_scene()
        self.update_click()

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.run = False
                case pygame.MOUSEBUTTONDOWN:
                    self.start_click(event)
                case pygame.MOUSEBUTTONUP:
                    if self.click_elem:
                        self.secondary_coord = self.click_elem
                        self.question_screen_init()
                    self.end_click(event)

    def question_screen_init(self):
        question = questions[self.primary_coord[0]][self.primary_coord[1]]["questions"][self.secondary_coord[0]][self.secondary_coord[1]]
        answers = [(question["answers"]["correct"], True)]
        answers.extend((answer, False) for answer in question["answers"]["incorrect"])
        random.shuffle(answers)

        for index, answer in enumerate(answers):
            if answer[1]: self.correct_answer = index

        answer_y = 400
        answer_width = 180
        answer_height = 150
        answer_margin = 5
        answer_pad = 20

        prompt_y = 100
        prompt_width = 700
        prompt_height = 160
        prompt_border = 5
        prompt_margin = 5

        prompt_tile = Elem(
            Elem.mk_tile_surface((prompt_width + prompt_border * 2, prompt_height + prompt_border * 2), "", bg_color=tile_color),
            ((screen_width - prompt_width) / 2 - prompt_border, prompt_y),
        )
        prompt_tile.image.blit(
            Elem.mk_tile_surface_wrap(
                (prompt_width, prompt_height),
                question["prompt"],
                bg_color=bg_color,
                text_rect=pygame.Rect(prompt_margin, prompt_margin, prompt_width - prompt_margin * 2, prompt_height - prompt_margin * 2),
            ),
            (prompt_border, prompt_border),
        )

        self.elems = {
                "buttons": {
                    "answer-" + str(index): Button(
                        Elem.mk_tile_surface_wrap(
                            (answer_width, answer_height),
                            answer[0],
                            text_rect=pygame.Rect(answer_margin, answer_margin, answer_width - answer_margin * 2, answer_height - answer_margin * 2),
                        ),
                        (
                            (screen_width - answer_pad) / 2 + (answer_width + answer_pad) * (index - 2),
                            answer_y,
                        ),
                    ) for (index, answer) in enumerate(answers)
                },
                "text": {
                    "title": Elem(Elem.mk_tile_surface((450, 40), "Financial Literacy Tic-Tac-Toe", bg_color=bg_color), ((screen_width - 450) / 2, 50)),
                    "prompt": prompt_tile,
                },
        }
        self.current_screen = 3

    def question_screen(self, screen):
        self.disp_scene()
        self.update_click()

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.run = False
                case pygame.MOUSEBUTTONDOWN:
                    self.start_click(event)
                case pygame.MOUSEBUTTONUP:
                    if self.click_elem == "answer-" + str(self.correct_answer):
                        self.secondary_board_state[self.primary_coord[0]][self.primary_coord[1]][self.secondary_coord[0]][self.secondary_coord[1]] = 1
                        self.primary_board_screen_init()
                    elif self.click_elem:
                        self.primary_board_screen_init()
                    self.end_click(event)

state = GameState()
state.main_screen_init()

run = True
while run:
    clock.tick(fps)
    screen.fill(bg_color)

    run = state.main(screen)

    pygame.display.update()
