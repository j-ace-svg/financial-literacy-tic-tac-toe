#!/usr/bin/env python

import pygame
from pygame.locals import *
import random
import os

pygame.init()

fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Financial Literacy Tic-Tac-Toe')

while True:
    clock.tick(fps)

    pygame.display.update()
