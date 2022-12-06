import pygame
from pygame.locals import *
import numpy
import random
import time

pygame.init()

PLAYER_COLOR = (0, 0, 0)
SURFACE_COLOR = (167, 255, 100)
GUARD_COLOR = (255, 0, 0)
BUSH_COLOR = (0, 255, 0)
WIDTH = 500
HEIGHT = 500

class Player(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       self.width = width
       self.height = height

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

class Guard(pygame.sprite.Sprite):
    def __init__(self, color, width, height, bounces):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       self.rect = self.image.get_rect()
       self.bounces = bounces

class Bush(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

class Popwerup(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

jumps = 1
is_hidden = False
level = 1
size = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(size)
pygame.display.set_caption(f'Level: {level}')

# Not exactly sure what these are for????
# all_sprites_list = pygame.sprite.Group()

# guards_list = pygame.sprite.Group()

# bushes_list = pygame.sprite.Group()

player = Player(PLAYER_COLOR, 10, 10)
guard1 = Guard(GUARD_COLOR, 10, 10, 0)
bush1 = Bush(BUSH_COLOR, 30, 30)

player.rect.x = 100
player.rect.y = 100

guard1.rect.x = random.randint(50, 350)
guard1.rect.y = random.randint(50, 350)

bush1.rect.x = random.randint(50, 350)
bush1.rect.y = random.randint(50, 350)

# all_sprites_list.add(player)
# all_sprites_list.add(guard1)
# all_sprites_list.add(bush1)

# guards_list.add(guard1)

# bushes_list.add(bush1)

running = True
clock = pygame.time.Clock()

# Player movement
move = {}
move["up"] = False
move["down"] = False
move["left"] = False
move["right"] = False

while running:
    # Setting the framerate to 30fps just
    # to see the result properly
    clock.tick(30)

    screen.fill(SURFACE_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # if keydown event happened
            # than printing a string to output
            if event.key == pygame.K_w:
                move["up"] = True
            if event.key == pygame.K_s:
                move["down"] = True
            if event.key == pygame.K_d:
                move["right"] = True
            if event.key == pygame.K_a:
                move["left"] = True
        
        if event.type == pygame.KEYUP:
            # if keydown event happened
            # than printing a string to output
            if event.key == pygame.K_w:
                move["up"] = False
            if event.key == pygame.K_s:
                move["down"] = False
            if event.key == pygame.K_d:
                move["right"] = False
            if event.key == pygame.K_a:
                move["left"] = False

    # Actually moving the player character
    if (move["up"]):
        player.rect.y -= 2
    if (move["down"]):
        player.rect.y += 2
    if (move["right"]):
        player.rect.x += 2
    if (move["left"]):
        player.rect.x -= 2

    if (player.rect.x > WIDTH - player.width):
        player.rect.x = WIDTH - player.width
    if (player.rect.x < 0):
        player.rect.x = 0
    if (player.rect.y > HEIGHT - player.height):
        player.rect.y = HEIGHT - player.height
    if (player.rect.y < 0):
        player.rect.y = 0

    screen.blit(player.image, player.rect)
    screen.blit(guard1.image, guard1.rect)
    
    pygame.display.update()