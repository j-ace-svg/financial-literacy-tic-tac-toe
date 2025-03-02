#!/usr/bin/env python

import pygame
from pygame.locals import *
import random
import os
import read_file

pygame.init()

print()
print()
print()
print()
print("HEY!!! You!")
print()
print("Yeah, you running the program.")
print()
print("This program is designed to use Pygame-CE (Pygame Community Edition), not regular Pygame. They're very similar, but there might be some slight differences, and I only test this on Pygame-CE.")
print()
print("So, if you get an error that seems weird (or, if you aren't familiar with python, any error), MAKE SURE YOU'RE USING PYGAME-CE.")
print()
print("You can install pygame-ce the same way you installed pygame (if you weren't the person who installed pygame on this computer, talk to them). If you used pip, then you would run `pip uninstall pygame` and then `pip install pygame-ce`.")
print()
print("Thank you for your time, and have fun running the program.")
print()
print()
print()
print()

fps = 60
clock = pygame.Clock()

screen_width = 864
screen_height = 936
monitor_width, monitor_height = pygame.display.get_desktop_sizes()[0]
window_scaling_width, window_scaling_height = monitor_width / 1920, monitor_height / 1080
window_scaling = min(window_scaling_width, window_scaling_height)
# Team Colors:
# Main blue: 4, 60, 127
# Less light main blue: 35, 69, 114
# Sky blue: 0, 146, 255
# Pastel blue: 185, 212, 239
# Lighter blue: 5, 92, 157
# Main grey: 231, 233, 236
bg_color = (185, 212, 239)
tile_color = (0, 146, 255)
global_tile_color = (231, 233, 236)
text_color = (4, 60, 127)
primary_board_icon_color = (255, 0, 0)
hover_border_color = (4, 60, 127)

screen = pygame.display.set_mode((screen_width * window_scaling, screen_height * window_scaling))
screen_unscaled = pygame.Surface((screen_width, screen_height))
pygame.display.set_caption('Financial Literacy Tic-Tac-Toe')

font = pygame.font.SysFont(None, 30)

with open("questions.txt", "r", encoding="utf8") as questions_file:
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
        scaled_coords = (coords[0] / window_scaling, coords[1] / window_scaling)
        return self.rect.collidepoint(scaled_coords)

class GameState():
    def __init__(self):
        self.current_screen = 0
        self.screen_list = [
            self.main_screen,
            self.primary_board_screen,
            self.secondary_board_screen,
            self.question_screen,
            self.winner_screen
        ]
        self.run = True
        self.elems = {}
        self.click_elem = None
        self.setup_game()
        self.tutorial = True

        # Tiles
        self.grid_pad = 20
        self.tile_size = 160
        self.checkbox_size = 40
        self.hover_border_size = 3
        self.empty_tile = Elem.mk_tile_surface((self.tile_size, self.tile_size), "")

        icon_radius = 3 * self.tile_size / 8

        self.o_tile_transparent = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        pygame.draw.circle(self.o_tile_transparent, text_color, (self.tile_size / 2, self.tile_size / 2), icon_radius, int(self.tile_size / 16))

        self.o_tile_transparent_primary = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        pygame.draw.circle(self.o_tile_transparent_primary, primary_board_icon_color, (self.tile_size / 2, self.tile_size / 2), icon_radius, int(self.tile_size / 16))

        self.o_tile = self.empty_tile.copy()
        self.o_tile.blit(self.o_tile_transparent, (0, 0))

        self.x_tile_transparent = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        pygame.draw.line(self.x_tile_transparent, text_color, (self.tile_size - 2 * icon_radius, self.tile_size - 2 * icon_radius), (2 * icon_radius, 2 * icon_radius), int(self.tile_size / 16))
        pygame.draw.line(self.x_tile_transparent, text_color, (self.tile_size - 2 * icon_radius, 2 * icon_radius), (2 * icon_radius, self.tile_size - 2 * icon_radius), int(self.tile_size / 16))

        self.x_tile_transparent_primary = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        pygame.draw.line(self.x_tile_transparent_primary, primary_board_icon_color, (self.tile_size - 2 * icon_radius, self.tile_size - 2 * icon_radius), (2 * icon_radius, 2 * icon_radius), int(self.tile_size / 16))
        pygame.draw.line(self.x_tile_transparent_primary, primary_board_icon_color, (self.tile_size - 2 * icon_radius, 2 * icon_radius), (2 * icon_radius, self.tile_size - 2 * icon_radius), int(self.tile_size / 16))

        self.x_tile = self.empty_tile.copy()
        self.x_tile.blit(self.x_tile_transparent, (0, 0))

        self.checkmark_transparent = pygame.Surface((self.checkbox_size, self.checkbox_size), pygame.SRCALPHA)
        pygame.draw.line(self.checkmark_transparent, text_color, (0.1 * self.checkbox_size, self.checkbox_size * 2 / 3 * 0.9), (self.checkbox_size / 3 * 0.9, self.checkbox_size * 0.9), int(self.checkbox_size / 16))
        pygame.draw.line(self.checkmark_transparent, text_color, (self.checkbox_size / 3 * 0.9, self.checkbox_size * 0.9), (self.checkbox_size * 0.9, 0.1 * self.checkbox_size), int(self.checkbox_size / 16))

        self.empty_checkbox = Elem.mk_tile_surface((self.checkbox_size, self.checkbox_size), "")
        self.filled_checkbox = self.empty_checkbox.copy()
        self.filled_checkbox.blit(self.checkmark_transparent, (0, 0))

    def setup_game(self):
        self.primary_coord = (0, 0)
        self.secondary_coord = (0, 0)
        self.correct_answer = 0
        self.responded_correctly = -1
        self.primary_board_state = [[0 for _ in range(3)] for _ in range(3)]
        self.secondary_board_state = [[[[0 for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.winner = 0

    def main(self, screen):
        self.screen_list[self.current_screen](screen)
        return self.run

    def disp_scene(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        for category in self.elems:
            for elem in self.elems[category]:
                if category == "buttons" and self.elems[category][elem].eval_click(mouse_pos):
                    unbordered_image = self.elems[category][elem].image
                    bordered_image = pygame.Surface((unbordered_image.get_size()[0] + self.hover_border_size * 2, unbordered_image.get_size()[1] + self.hover_border_size * 2))
                    bordered_image.fill(hover_border_color)
                    bordered_image.blit(unbordered_image, (self.hover_border_size, self.hover_border_size))
                    screen.blit(bordered_image, (self.elems[category][elem].rect.x - self.hover_border_size, self.elems[category][elem].rect.y - self.hover_border_size))
                else:
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

    def check_win(self, board):
        """
        Check the supplied board state for a winner. A 1 or 2 indicates a player win, a 0 indicates an unfinished game, and -1 indicates a draw
        """
        for row in range(3):
            value = board[row][0]
            if (not value == 0) and (value == board[row][1]) and (value == board[row][2]):
                return value

        for col in range(3):
            value = board[0][col]
            if (not value == 0) and (value == board[1][col]) and (value == board[2][col]):
                return value

        for i in range(2):
            sign = i*2 - 1
            value = board[1 + sign][0]
            if (not value == 0) and (value == board[1][1]) and (value == board[1 - sign][2]):
                return value

        for row in range(3):
            for col in range(3):
                if board[row][col] == 0:
                    return 0

        return -1
    
    def opponent_move(self):
        available_spots = []

        # Find available squares in last played secondary board
        last_secondary_board = self.secondary_board_state[self.primary_coord[0]][self.primary_coord[1]]
        if self.check_win(self.secondary_board_state[self.primary_coord[0]][self.primary_coord[1]]) == 0:
            for row in range(3):
                for col in range(3):
                    if last_secondary_board[row][col] == 0:
                        available_spots.append((row, col))

        # Can play in last played secondary board
        if available_spots:
            selected_coord = random.choice(available_spots)
            self.secondary_board_state[self.primary_coord[0]][self.primary_coord[1]][selected_coord[0]][selected_coord[1]] = 2

        # Cannot play in last played secondary board
        else:
            unfinished_boards = []
            unfinished_played_boards = []
            for primary_row in range(3):
                for primary_col in range(3):
                    if self.primary_board_state[primary_row][primary_col] == 0:
                        unfinished_boards.append(((primary_row, primary_col), self.secondary_board_state[primary_row][primary_col]))

                        board_empty = True
                        for secondary_row in range(3):
                            for secondary_col in range(3):
                                if not self.secondary_board_state[primary_row][primary_col][secondary_row][secondary_col] == 0:
                                    board_empty = False

                        if not board_empty:
                            unfinished_played_boards.append(((primary_row, primary_col), self.secondary_board_state[primary_row][primary_col]))

            selected_primary_board = None
            if unfinished_played_boards:
                selected_primary_board = random.choice(unfinished_played_boards)
            elif unfinished_boards:
                selected_primary_board = random.choice(unfinished_boards)
            else:
                return

            for row in range(3):
                for col in range(3):
                    if selected_primary_board[1][row][col] == 0:
                        available_spots.append((row, col))

            selected_coord = random.choice(available_spots)
            self.secondary_board_state[selected_primary_board[0][0]][selected_primary_board[0][1]][selected_coord[0]][selected_coord[1]] = 2

    def main_screen_init(self):
        self.elems = {
                "buttons": {
                    "quit": Button(Elem.mk_tile_surface((160, 40), "Quit"), ((screen_width - 160) / 2, 600)),
                    "start": Button(Elem.mk_tile_surface((160, 40), "Start"), ((screen_width - 160) / 2, 450)),
                    "tutorial": Button(self.filled_checkbox, (screen_width - 100, 500))
                },
                "text": {
                    "title": Elem(Elem.mk_tile_surface((450, 40), "Financial Literacy Tic-Tac-Toe", bg_color=bg_color), ((screen_width - 450) / 2, 300)),
                    "tutorial-label": Elem(Elem.mk_tile_surface((450, 40), "Enable tutorial:", bg_color=bg_color), (screen_width - 330, 450))
                },
        }
        self.current_screen = 0

    def main_screen(self, screen):
        self.disp_scene(screen)
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
                        case "tutorial":
                            self.tutorial = not self.tutorial
                            if self.tutorial:
                                self.elems["buttons"]["tutorial"].image = self.filled_checkbox
                            else:
                                self.elems["buttons"]["tutorial"].image = self.empty_checkbox
                    self.end_click(event)

    def primary_board_screen_init(self):
        sub_boards = [ [ None for primary_col in range(3) ] for primary_row in range(3) ]
        for primary_row in range(3):
            for primary_col in range(3):
                sub_board_large = Elem.mk_tile_surface((self.tile_size * 3 + self.grid_pad * 4, self.tile_size * 3 + self.grid_pad * 4), "", bg_color = global_tile_color)
                for secondary_row in range(3):
                    for secondary_col in range(3):
                        player = self.secondary_board_state[primary_row][primary_col][secondary_row][secondary_col]
                        sub_board_large.blit(self.empty_tile if player == 0 else self.x_tile if player == 1 else self.o_tile, (secondary_col * (self.tile_size + self.grid_pad) + self.grid_pad, secondary_row * (self.tile_size + self.grid_pad) + self.grid_pad))

                sub_boards[primary_row][primary_col] = pygame.transform.scale(sub_board_large, (self.tile_size, self.tile_size))
                if self.primary_board_state[primary_row][primary_col] == 1:
                    sub_boards[primary_row][primary_col].blit(self.x_tile_transparent_primary, (0, 0))
                elif self.primary_board_state[primary_row][primary_col] == 2:
                    sub_boards[primary_row][primary_col].blit(self.o_tile_transparent_primary, (0, 0))

        response_notification_text = ""
        if self.responded_correctly == 0:
            response_notification_text = "Incorrect"
        elif self.responded_correctly == 1:
            response_notification_text = "Correct"

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
                    "response_notification": Elem(Elem.mk_tile_surface((450, 40), response_notification_text, bg_color=bg_color), ((screen_width - 450) / 2, 100)),
                    "tutorial-text-top": Elem(Elem.mk_tile_surface((600, 40), "You are X. Select a mini tic-tac-toe board to play in." if self.tutorial else "", bg_color=bg_color), ((screen_width - 600) / 2, 150)),
                    "tutorial-text-bottom": Elem(Elem.mk_tile_surface((800, 40), "Winning mini boards lets you capture squares in the main game of tic-tac-toe" if self.tutorial else "", bg_color=bg_color), ((screen_width - 800) / 2, 750)),
                },
        }
        self.current_screen = 1

    def primary_board_screen(self, screen):
        self.disp_scene(screen)
        self.update_click()

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.run = False
                case pygame.MOUSEBUTTONDOWN:
                    self.start_click(event)
                case pygame.MOUSEBUTTONUP:
                    if self.click_elem and self.primary_board_state[self.click_elem[0]][self.click_elem[1]] == 0:
                        self.primary_coord = self.click_elem
                        self.secondary_board_screen_init()
                    self.end_click(event)

    def secondary_board_screen_init(self):
        secondary_board = self.secondary_board_state[self.primary_coord[0]][self.primary_coord[1]]
        self.elems = {
                "buttons": {
                    (row, col): Button(
                        self.empty_tile if secondary_board[row][col] == 0 else self.x_tile if secondary_board[row][col] == 1 else self.o_tile,
                        (
                            (screen_width - self.tile_size) / 2 + (self.tile_size + self.grid_pad) * (col - 1),
                            (screen_height - self.tile_size) / 2 + (self.tile_size + self.grid_pad) * (row - 1),
                        ),
                    ) for row in range(3) for col in range(3)
                } | {
                    "back": Button(Elem.mk_tile_surface((160, 40), "Back"), ((screen_width - 160) / 2, 800)),
                },
                "text": {
                    "title": Elem(Elem.mk_tile_surface((450, 40), questions[self.primary_coord[0]][self.primary_coord[1]]["title"], bg_color=bg_color), ((screen_width - 450) / 2, 50)),
                    "tutorial-text": Elem(Elem.mk_tile_surface((450, 40), "Select a square to try to capture" if self.tutorial else "", bg_color=bg_color), ((screen_width - 450) / 2, 150)),
                },
        }
        self.current_screen = 2

    def secondary_board_screen(self, screen):
        self.disp_scene(screen)
        self.update_click()

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.run = False
                case pygame.MOUSEBUTTONDOWN:
                    self.start_click(event)
                case pygame.MOUSEBUTTONUP:
                    if self.click_elem:
                        if self.click_elem == "back":
                            self.primary_board_screen_init()
                        elif self.secondary_board_state[self.primary_coord[0]][self.primary_coord[1]][self.click_elem[0]][self.click_elem[1]] == 0:
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
                    "tutorial-text": Elem(Elem.mk_tile_surface((600, 40), "Answer the question correctly to capture the square" if self.tutorial else "", bg_color=bg_color), ((screen_width - 600) / 2, 300)),
                },
        }
        self.current_screen = 3

    def question_screen(self, screen):
        self.disp_scene(screen)
        self.update_click()

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.run = False
                case pygame.MOUSEBUTTONDOWN:
                    self.start_click(event)
                case pygame.MOUSEBUTTONUP:
                    if self.click_elem == "answer-" + str(self.correct_answer):
                        self.responded_correctly = 1
                        self.secondary_board_state[self.primary_coord[0]][self.primary_coord[1]][self.secondary_coord[0]][self.secondary_coord[1]] = 1
                        self.primary_board_state[self.primary_coord[0]][self.primary_coord[1]] = self.check_win(self.secondary_board_state[self.primary_coord[0]][self.primary_coord[1]])
                        self.opponent_move()
                        self.primary_board_state[self.primary_coord[0]][self.primary_coord[1]] = self.check_win(self.secondary_board_state[self.primary_coord[0]][self.primary_coord[1]])

                        self.winner = self.check_win(self.primary_board_state)
                        if self.winner == 0:
                            self.primary_board_screen_init()
                        else:
                            self.winner_screen_init()
                    elif self.click_elem:
                        self.responded_correctly = 0
                        self.primary_board_screen_init()

                        self.opponent_move()
                        self.primary_board_state[self.primary_coord[0]][self.primary_coord[1]] = self.check_win(self.secondary_board_state[self.primary_coord[0]][self.primary_coord[1]])

                        self.winner = self.check_win(self.primary_board_state)
                        if self.winner == 0:
                            self.primary_board_screen_init()
                        else:
                            self.winner_screen_init()
                    self.end_click(event)

    def winner_screen_init(self):
        winner_text = ""
        if self.winner == 1:
            winner_text = "You won!"
        elif self.winner == 2:
            winner_text = "The computer won!"
        else:
            winner_text = "It was a tie"

        self.elems = {
                "buttons": {
                    "quit": Button(Elem.mk_tile_surface((160, 40), "Quit"), ((screen_width - 160) / 2, 600)),
                    "restart": Button(Elem.mk_tile_surface((160, 40), "Restart"), ((screen_width - 160) / 2, 450)),
                },
                "text": {
                    "title": Elem(Elem.mk_tile_surface((450, 40), "Financial Literacy Tic-Tac-Toe", bg_color=bg_color), ((screen_width - 450) / 2, 50)),
                    "winner": Elem(Elem.mk_tile_surface((450, 40), winner_text, bg_color=bg_color), ((screen_width - 450) / 2, 300)),
                },
        }
        self.current_screen = 4

    def winner_screen(self, screen):
        self.disp_scene(screen)
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
                        case "restart":
                            self.setup_game()
                            self.main_screen_init()
                    self.end_click(event)

state = GameState()
state.main_screen_init()

run = True
while run:
    clock.tick(fps)
    screen_unscaled.fill(bg_color)

    run = state.main(screen_unscaled)
    screen.blit(pygame.transform.scale(screen_unscaled, (screen_width * window_scaling, screen_height * window_scaling)), (0, 0))

    pygame.display.update()
