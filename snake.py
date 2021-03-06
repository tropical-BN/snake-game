import numpy as np
import pygame as pg
import random
import sys
import time
pg.init()
pg.font.init()

block_dim = 20  # body parts are squares with width of 20
screenscale = 10  # >= 5
size = width, height = screenscale*block_dim, screenscale*block_dim
speed = block_dim
saved_velocity = (0, 0)  # velcoity as given by the keys pressed by the player
grey,red, col_head = (47, 79, 79), (255, 90, 0), (200, 255, 0)
start = [0]*2
half_b_dim = int(block_dim/2)
SURFACE = pg.display.set_mode(size)
pg.display.set_caption("Snake")
gameover = False


def newgame():
    global gameover, score,blocks, apple_y, apple_x, start, saved_velocity
    gameover = False
    score = 0
    start[0] = block_dim * np.random.randint(1, screenscale-2)  # x start
    start[1] = block_dim * np.random.randint(1, screenscale-2)  # y start

    pg.display.set_caption("Snake")
    blocks = np.array([[start[0], start[1]]])
    start = [-1, -1]
    apple_x, apple_y = 0, 0
    saved_velocity = (0, 0)
    pg.event.clear()
    play()


def play():
    global blocks, saved_velocity
    new_spawn = True
    t= int(round(time.time() * 10))
    t_prev = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.event.clear()
                sys.exit()
            getKeys(event)

        if t != t_prev:
            if not gameover:
                movesnake()
                checkcollisions()
                if new_spawn:
                    assign_apple_coords()
                    new_spawn = False

            SURFACE.fill(grey)
            for coord in blocks:
                pg.draw.rect(SURFACE, col_head, (coord[0] + 2, coord[1] + 2, block_dim - 2, block_dim - 2))
            pg.draw.circle(SURFACE, red, (apple_x, apple_y), int(block_dim/2), 0)

            if gameover:
                font = pg.font.SysFont('Calibri', 20)
                text = font.render("GAME OVER : score = %s" % score, True, (80, 10, 10))
                print("GAME OVER : score = %s" % score)
                SURFACE.blit(text, (width/2 - 100, height/2))
                pg.display.flip()
                secsStart = time.time()
                while time.time() - secsStart <= 2:
                    pass
                newgame()
            else:
                SURFACE.blit(SURFACE, (0, 0))
                pg.display.flip()
            t_prev = t
        t = int(round(time.time() * 10))


def getKeys(event):
    # gets the keys from the keyboard
    global saved_velocity,speed,gameover
    if event.type == pg.KEYDOWN and not gameover:
        if saved_velocity != (0, speed) and (event.key == pg.K_w or event.key == pg.K_UP):
            saved_velocity = (0, -speed)
        if saved_velocity != (speed, 0) and (event.key == pg.K_a or event.key == pg.K_LEFT):
            saved_velocity = (-speed, 0)
        if saved_velocity != ( 0, -speed) and (event.key == pg.K_s or event.key == pg.K_DOWN):
            saved_velocity = (0, speed)
        if saved_velocity != (-speed, 0) and (event.key == pg.K_d or event.key == pg.K_RIGHT):
            saved_velocity = (speed, 0)


def movesnake():
    # move the snake
    global blocks
    blocks = np.concatenate((np.array([blocks[0] + saved_velocity]), blocks), axis=0)
    blocks = np.delete(blocks, len(blocks) - 1, 0)


def checkcollisions():
    global blocks, saved_velocity, gameover, score
    # check if outside boundaries
    h = blocks[0]
    if h[0] > width - block_dim or h[0] < 0:
        gameover = True
    elif h[1] > height - block_dim or h[1] < 0:
        gameover = True

    else:
        mask = blocks == blocks[0]
        copies = np.array(mask.all(axis=1))
        if copies.sum(axis=0) > 1:
            gameover = True

    if not gameover:
        if blocks[0][0] == apple_x - half_b_dim and blocks[0][1] == apple_y - half_b_dim:
            # add to tail, this will happen if an apple is hit
            blocks = np.concatenate((np.array([[apple_x - half_b_dim, apple_y - half_b_dim]]), blocks), axis=0)
            assign_apple_coords()
            score += 1
    else:
        saved_velocity = (0, 0)


def assign_apple_coords():
    global apple_x, apple_y, blocks, gameover
    coords = [0]*2
    redo = True
    while redo:
        redo = False
        coords[0] = block_dim * np.random.randint(0, screenscale) + half_b_dim
        np.random.seed(int(time.time()))
        coords[1] = block_dim * random.randint(0, screenscale) + half_b_dim  # y start
        if coords[0] == blocks[0][0] and coords[1] == blocks[0][1]:
            redo = True
        if coords[0] > width or coords[1] > height:
            redo = True

    # ensure apple isnt spawned inside snake
    search = coords[0] - half_b_dim + (coords[1] - half_b_dim)*1j
    jblocks = blocks[:, 0] + blocks[:, 1]*1j
    result = np.in1d(search, jblocks, assume_unique=True)
    if result:
        if len(jblocks) <= (screenscale*screenscale):
            assign_apple_coords()
        else:
            gameover = True
    else:
        apple_x = coords[0]
        apple_y = coords[1]


newgame()

