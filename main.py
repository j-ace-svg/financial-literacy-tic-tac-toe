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
text_color = (255, 255, 255)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Financial Literacy Tic-Tac-Toe')

font = pygame.font.SysFont(None, 30)

"""
questions = [
    [ # Row 0
        { # (0, 0)
            "prompt": "What is 1 + 1?",
            "answers": {
                "correct": "1 + 1",
                "incorrect": [
                    "",
                    "",
                    "",
                ],
            },
        },
        { # (0, 1)
            "prompt": "What is 1 + 2?",
            "answers": {
                "correct": "1 + 2",
                "incorrect": [
                    "",
                    "",
                    "",
                ],
            },
        },
        { # (0, 2)
            "prompt": "What is 1 + 3?",
            "answers": {
                "correct": "1 + 3",
                "incorrect": [
                    "",
                    "",
                    "",
                ],
            },
        },
    ],
    [ # Row 1
        { # (1, 0)
            "prompt": "What is 2 + 1?",
            "answers": {
                "correct": "2 + 1",
                "incorrect": [
                    "",
                    "",
                    "",
                ],
            },
        },
        { # (1, 1)
            "prompt": "What is 2 + 2?",
            "answers": {
                "correct": "2 + 2",
                "incorrect": [
                    "",
                    "",
                    "",
                ],
            },
        },
        { # (1, 2)
            "prompt": "What is 2 + 3?",
            "answers": {
                "correct": "2 + 3",
                "incorrect": [
                    "",
                    "",
                    "",
                ],
            },
        },
    ],
    [ # Row 2
        { # (2, 0)
            "prompt": "What is 3 + 1?",
            "answers": {
                "correct": "3 + 1",
                "incorrect": [
                    "",
                    "",
                    "",
                ],
            },
        },
        { # (2, 1)
            "prompt": "What is 3 + 2?",
            "answers": {
                "correct": "3 + 2",
                "incorrect": [
                    "",
                    "",
                    "",
                ],
            },
        },
        { # (2, 2)
            "prompt": "What is 3 + 3?",
            "answers": {
                "correct": "3 + 3",
                "incorrect": [
                    "",
                    "",
                    "",
                ],
            },
        },
    ],
]
"""

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
            self.board_screen,
            self.question_screen,
        ]
        self.run = True
        self.elems = {}
        self.click_elem = None
        self.coord = (0, 0)
        self.correct_answer = 0
        self.board_state = [ [0 for _ in range(3)] for _ in range(3) ]

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

    def board_screen_init(self):
        grid_pad = 20
        tile_size = 160

        empty_tile = Elem.mk_tile_surface((tile_size, tile_size), "")

        icon_radius = 3 * tile_size / 8

        o_tile = empty_tile.copy()
        pygame.draw.circle(o_tile, text_color, (tile_size / 2, tile_size / 2), icon_radius, int(tile_size / 16))

        x_tile = empty_tile.copy()
        pygame.draw.line(x_tile, text_color, (tile_size - 2 * icon_radius, tile_size - 2 * icon_radius), (2 * icon_radius, 2 * icon_radius), int(tile_size / 16))
        pygame.draw.line(x_tile, text_color, (tile_size - 2 * icon_radius, 2 * icon_radius), (2 * icon_radius, tile_size - 2 * icon_radius), int(tile_size / 16))

        self.elems = {
                "buttons": {
                    (row, col): Button(
                        empty_tile if self.board_state[row][col] == 0 else x_tile,
                        (
                            (screen_width - tile_size) / 2 + (tile_size + grid_pad) * (col - 1),
                            (screen_height - tile_size) / 2 + (tile_size + grid_pad) * (row - 1),
                        ),
                    ) for row in range(3) for col in range(3)
                },
                "text": {
                    "title": Elem(Elem.mk_tile_surface((450, 40), "Financial Literacy Tic-Tac-Toe", bg_color=bg_color), ((screen_width - 450) / 2, 50)),
                },
        }
        self.current_screen = 1

    def board_screen(self, screen):
        self.disp_scene()
        self.update_click()

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.run = False
                case pygame.MOUSEBUTTONDOWN:
                    self.start_click()
                case pygame.MOUSEBUTTONUP:
                    if self.click_elem:
                        self.coord = self.click_elem
                        self.question_screen_init()
                    self.click_elem = None

    def question_screen_init(self):
        question = random.choice(questions[self.coord[0]][self.coord[1]])
        answers = [(question["answers"]["correct"], True)]
        answers.extend((answer, False) for answer in question["answers"]["incorrect"])
        random.shuffle(answers)

        for index, answer in enumerate(answers):
            if answer[1]: self.correct_answer = index

        answer_width = 160
        answer_pad = 20

        self.elems = {
                "buttons": {
                    "answer-" + str(index): Button(
                        Elem.mk_tile_surface((answer_width, 80), answer[0]),
                        (
                            (screen_width - answer_pad) / 2 + (answer_width + answer_pad) * (index - 2),
                            400,
                        ),
                    ) for (index, answer) in enumerate(answers)
                },
                "text": {
                    "title": Elem(Elem.mk_tile_surface((450, 40), "Financial Literacy Tic-Tac-Toe", bg_color=bg_color), ((screen_width - 450) / 2, 50)),
                    "prompt": Elem(Elem.mk_tile_surface((450, 40), question["prompt"], bg_color=bg_color), ((screen_width - 450) / 2, 100)),
                },
        }
        self.current_screen = 2

    def question_screen(self, screen):
        self.disp_scene()
        self.update_click()

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.run = False
                case pygame.MOUSEBUTTONDOWN:
                    self.start_click()
                case pygame.MOUSEBUTTONUP:
                    if self.click_elem == "answer-" + str(self.correct_answer):
                        self.board_state[self.coord[0]][self.coord[1]] = 1
                        self.board_screen_init()
                    elif self.click_elem:
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
