import pygame
from pygame.locals import *
import numpy
import random
import time

pygame.init()

PLAYER_SPEED = 2

PLAYER_COLOR = (0, 0, 0)
PLAYER_HIDDEN_COLOR = (102, 102, 102)
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

class PatrolGuard(pygame.sprite.Sprite):
    def __init__(self, color, width, height, speed, positions):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       self.rect = self.image.get_rect()

       self.speed = speed

       self.patrolPositions = positions
       self.positionCounter = 0
       self.currentPosition = self.patrolPositions[self.positionCounter]
    
    def guard_movement(self):
        if (
            (self.rect.x >= self.currentPosition[0] - 5 and self.rect.x <= self.currentPosition[0] + 5)
            and
            (self.rect.y >= self.currentPosition[1] - 5 and self.rect.y <= self.currentPosition[1] + 5)
            ):
            self.positionCounter += 1
            if (self.positionCounter == len(self.patrolPositions)):
                self.positionCounter = 0

            self.currentPosition = self.patrolPositions[self.positionCounter]
        else:
            if (self.rect.x > self.currentPosition[0] + self.speed):
                self.rect.x -= self.speed
            elif (self.rect.x < self.currentPosition[0] - self.speed):
                self.rect.x += self.speed

            if (self.rect.y > self.currentPosition[1] + self.speed):
                self.rect.y -= self.speed
            elif (self.rect.y < self.currentPosition[1] - self.speed):
                self.rect.y += self.speed

class ShootingGuard(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       self.rect = self.image.get_rect()

class ChasingGuard(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       self.rect = self.image.get_rect()

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

# Sprite groups
all_sprites_list = pygame.sprite.Group()

guards_list = pygame.sprite.Group()

bushes_list = pygame.sprite.Group()

# Player
player = Player(PLAYER_COLOR, 10, 10)

player.rect.x = 300
player.rect.y = 100

all_sprites_list.add(player)

# Guards
guard1 = PatrolGuard(GUARD_COLOR, 10, 10, 5, [[50, 50], [450, 450], [50, 450], [50, 50], [450, 50], [450, 450]])
guard1.rect.x = random.randint(50, 350)
guard1.rect.y = random.randint(50, 350)
all_sprites_list.add(guard1)
guards_list.add(guard1)

guard2 = PatrolGuard(GUARD_COLOR, 10, 10, 5, [[50, 50], [450, 450], [50, 450], [50, 50], [450, 50], [450, 450]])
guard2.rect.x = random.randint(50, 350)
guard2.rect.y = random.randint(50, 350)
all_sprites_list.add(guard2)
guards_list.add(guard2)

guard3 = PatrolGuard(GUARD_COLOR, 10, 10, 5, [[50, 50], [450, 450], [50, 450], [50, 50], [450, 50], [450, 450]])
guard3.rect.x = random.randint(50, 350)
guard3.rect.y = random.randint(50, 350)
all_sprites_list.add(guard3)
guards_list.add(guard3)

# Bushes
bush1 = Bush(BUSH_COLOR, 30, 30)
bush1.rect.x = random.randint(50, 350)
bush1.rect.y = random.randint(50, 350)
all_sprites_list.add(bush1)
bushes_list.add(bush1)

bush2 = Bush(BUSH_COLOR, 30, 30)
bush2.rect.x = random.randint(50, 350)
bush2.rect.y = random.randint(50, 350)
all_sprites_list.add(bush2)
bushes_list.add(bush2)

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
        player.rect.y -= PLAYER_SPEED
    if (move["down"]):
        player.rect.y += PLAYER_SPEED
    if (move["right"]):
        player.rect.x += PLAYER_SPEED
    if (move["left"]):
        player.rect.x -= PLAYER_SPEED

    if (player.rect.x > WIDTH - player.width):
        player.rect.x = WIDTH - player.width
    if (player.rect.x < 0):
        player.rect.x = 0
    if (player.rect.y > HEIGHT - player.height):
        player.rect.y = HEIGHT - player.height
    if (player.rect.y < 0):
        player.rect.y = 0
    
    # Allowing player to be hidden if behind guard
    for bush in bushes_list:
        if pygame.sprite.collide_rect(player, bush):
            is_hidden = True
            player.image.fill(PLAYER_HIDDEN_COLOR)
        else:
            is_hidden = False
            player.image.fill(PLAYER_COLOR)
    
    # Testing if player collides with guard
    for guard in guards_list:
        guard.guard_movement()
        if pygame.sprite.collide_rect(player, guard) and not is_hidden:
            running = False

    for object in all_sprites_list:
        screen.blit(object.image, object.rect)

    screen.blit(player.image, player.rect)
    screen.blit(guard1.image, guard1.rect)
    
    pygame.display.update()