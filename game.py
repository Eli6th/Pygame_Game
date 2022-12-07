import pygame
from pygame.locals import *
import numpy
import random
import time

pygame.init()

PLAYER_SPEED = 5

PLAYER_COLOR = (0, 0, 0)
PLAYER_HIDDEN_COLOR = (102, 102, 102)
SURFACE_COLOR = (167, 255, 100)

GUARD_PATROL_COLOR = (255, 0, 0)
GUARD_CHASING_COLOR = (171, 9, 0)
GUARD_SHOOTER_COLOR = (255, 71, 61)

BUSH_COLOR = (0, 255, 0)
WIN_AREA_COLOR = (255, 255, 0)

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
    
    def guard_movement(self, player_pos):
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
    def __init__(self, color, width, height, speed):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       self.speed = speed

       self.rect = self.image.get_rect()

    def guard_movement(self, player_pos):
        if is_hidden:
            return
        elif (
            (self.rect.x >= player_pos.x - 100 and self.rect.x <= player_pos.x + 100)
            and
            (self.rect.y >= player_pos.y - 100 and self.rect.y <= player_pos.y + 100)
            ):
            if (1225 > (player_pos.x - self.rect.x) * (player_pos.x - self.rect.x) + (player_pos.y - self.rect.y) * (player_pos.y - self.rect.y)):
                if (self.rect.x < player_pos.x + 35):
                    self.rect.x -= self.speed
                elif (self.rect.x > player_pos.x - 35):
                    self.rect.x += self.speed

                if (self.rect.y < player_pos.y + 35):
                    self.rect.y += self.speed
                elif (self.rect.y > player_pos.y - 35):
                    self.rect.y -= self.speed
            return
        else:
            if (self.rect.x > player_pos.x + self.speed):
                self.rect.x -= self.speed
            elif (self.rect.x < player_pos.x - self.speed):
                self.rect.x += self.speed

            if (self.rect.y > player_pos.y + self.speed):
                self.rect.y -= self.speed
            elif (self.rect.y < player_pos.y - self.speed):
                self.rect.y += self.speed

class ChasingGuard(pygame.sprite.Sprite):
    def __init__(self, color, width, height, speed):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       self.speed = speed

       self.rect = self.image.get_rect()
    
    def guard_movement(self, player_pos):
        if (
            (self.rect.x >= player_pos.x - 5 and self.rect.x <= player_pos.x + 5)
            and
            (self.rect.y >= player_pos.y - 5 and self.rect.y <= player_pos.y + 5)
            or
            is_hidden
            ):
            return
        else:
            if (self.rect.x > player_pos.x + self.speed):
                self.rect.x -= self.speed
            elif (self.rect.x < player_pos.x - self.speed):
                self.rect.x += self.speed

            if (self.rect.y > player_pos.y + self.speed):
                self.rect.y -= self.speed
            elif (self.rect.y < player_pos.y - self.speed):
                self.rect.y += self.speed

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

class Powerup(pygame.sprite.Sprite):
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

class WinArea(pygame.sprite.Sprite):
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


def random_positions():
    positions = []
    for i in range(random.randint(3, 6)):
        positions.append([random.randint(50, 450),random.randint(50, 450)])
    
    return positions


all_sprites_list = pygame.sprite.Group()
guards_list = pygame.sprite.Group()
bushes_list = pygame.sprite.Group()

# Level variables
level = 1
size = (WIDTH, HEIGHT)

# Player variables
jumps = 1
is_hidden = False

screen = pygame.display.set_mode(size)

# Functions to create enemies
def create_patrol_guard():
    guard = PatrolGuard(GUARD_PATROL_COLOR, 10, 10, 5, random_positions())
    guard.rect.x = random.randint(0, 500)
    guard.rect.y = random.randint(0, 500)
    all_sprites_list.add(guard)
    guards_list.add(guard)

def create_chasing_guard():
    guard = ChasingGuard(GUARD_CHASING_COLOR, 10, 10, 1)
    guard.rect.x = random.randint(0, 500)
    guard.rect.y = random.randint(0, 500)
    all_sprites_list.add(guard)
    guards_list.add(guard)

def create_shooting_guard():
    guard = ShootingGuard(GUARD_SHOOTER_COLOR, 10, 10, 6)
    guard.rect.x = random.randint(0, 500)
    guard.rect.y = random.randint(0, 500)
    all_sprites_list.add(guard)
    guards_list.add(guard)

# Player
player = Player(PLAYER_COLOR, 10, 10)

player.rect.x = 50
player.rect.y = 50

all_sprites_list.add(player)

# Guards
for i in range(1):
    create_patrol_guard()
    create_chasing_guard()

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

bush3 = Bush(BUSH_COLOR, 30, 30)
bush3.rect.x = player.rect.x - player.width
bush3.rect.y = player.rect.y - player.height
all_sprites_list.add(bush3)
bushes_list.add(bush3)

winArea = WinArea(WIN_AREA_COLOR, 70, 70)
winArea.rect.x = 450
winArea.rect.y = 450
all_sprites_list.add(winArea)

running = True
clock = pygame.time.Clock()

# Player movement
move = {}
move["up"] = False
move["down"] = False
move["left"] = False
move["right"] = False

def reset_game():
    global level
    pygame.display.set_caption(f'Level: {level}')

    # Sprite groups
    global all_sprites_list, guards_list, bushes_list
    all_sprites_list = pygame.sprite.Group()
    guards_list = pygame.sprite.Group()
    bushes_list = pygame.sprite.Group()

    player.rect.x = 50
    player.rect.y = 50

    all_sprites_list.add(player)

    global bush3
    bush3 = Bush(BUSH_COLOR, 30, 30)
    bush3.rect.x = player.rect.x - player.width
    bush3.rect.y = player.rect.y - player.height
    all_sprites_list.add(bush3)
    bushes_list.add(bush3)

    for i in range(level):
        create_patrol_guard()
        create_chasing_guard()
    return

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
    is_hidden = False
    player.image.fill(PLAYER_COLOR)
    for bush in bushes_list:
        if pygame.sprite.collide_rect(player, bush):
            is_hidden = True
            player.image.fill(PLAYER_HIDDEN_COLOR)
    
    # Testing if player collides with guard
    for guard in guards_list:
        guard.guard_movement(player.rect)
        if pygame.sprite.collide_rect(player, guard) and not is_hidden:
            level = 1

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

            reset_game()

    if pygame.sprite.collide_rect(player, winArea) and not is_hidden:
        level += 1
        pygame.display.set_caption(f'Level: {level}')
        reset_game()

    # Displaying the objects in our scene
    for object in bushes_list:
        screen.blit(object.image, object.rect)

    screen.blit(winArea.image, winArea.rect)

    for object in guards_list:
        screen.blit(object.image, object.rect)

    screen.blit(player.image, player.rect)
    
    pygame.display.update()