""" 
Filename: settings.py
Purpose: Contains the settings for Ghost Town.
Author: Matthew Peres Tino

"""

#####################################################################################################
# imports
import pygame as pg
import numpy as np
import os, sys, math

#####################################################################################################
# settings
pg.init()

# SCREEN SETTINGS
os.environ['SDL_VIDEO_CENTERED'] = '1'
WIDTH, HEIGHT = 1400, 950 # width and height of game window
WIN = pg.display.set_mode((WIDTH,HEIGHT)) # create window object
pg.display.set_caption("Ghost Town - Menu") # game name
FPS = 60

# FONTS
pg.font.init() # font
TITLE_FONT = pg.font.SysFont('consolas', bold=True, size=150)
PLAY_FONT = pg.font.SysFont('consolas', bold=True, size=100)
ALL_FONT = pg.font.SysFont('consolas', bold=True, size=30)
HEALTH_FONT = pg.font.SysFont('consolas',bold=True, size=22)

# COLOURS
WHITE = (255,255,225)
BUTTON_CLICK = (220, 220, 220)
BLACK = (0,0,0)
RED = (255, 0, 0)
SCREEN_COL = pg.color.Color('blue')

# OBJECT DIMENSIONS
ENTITY_W, ENTITY_H = 60, 60
FENCE_W, FENCE_H = 1.2*ENTITY_W, ENTITY_H
FENCE_DRAW_Y = 150 # the y coordinate to draw fence

# IMAGES TO LOAD AND DRAW
grass = pg.image.load('images/grass_main.jpg').convert()
grass_dark = pg.image.load('images/grass_dark.jpg').convert()
fence = pg.transform.rotate(pg.transform.scale(pg.image.load('images/fence.png'), (FENCE_W, FENCE_H)), 0)
house_main = pg.transform.scale(pg.image.load('images/house_main.png'), (1.5*ENTITY_W, 1.5*ENTITY_H))
house_side = pg.transform.scale(pg.image.load('images/house_side.png'), (1.5*ENTITY_W, 1.5*ENTITY_H))

# Collision events
PLAYER_HIT = pg.USEREVENT + 1
ENEMY_SPAWN, ENEMY_TIME = pg.USEREVENT + 2, 500
pg.time.set_timer(ENEMY_SPAWN, ENEMY_TIME)

# now initialize 


    