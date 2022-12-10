import pygame
from pygame.locals import *
import sys
import numpy
import random
import time

pygame.init()

PLAYER_SPEED = 5
PLAYER_HIDDEN_COLOR = (102, 102, 102)
SURFACE_COLOR = (167, 255, 100)

GUARD_PATROL_COLOR = (255, 0, 0)
GUARD_CHASING_COLOR = (171, 9, 0)
GUARD_EDGE_COLOR = (255, 71, 61)

BUSH_COLOR = (0, 255, 0)
WIN_AREA_COLOR = (255, 255, 0)

WIDTH = 500
HEIGHT = 500

# Global Variables
player_color = (0, 0, 0)
running = True
clock = pygame.time.Clock()

# Game variables
is_playing = False
is_paused = False
font = pygame.font.SysFont(None, 30)

# Level variables
level = 1
size = (WIDTH, HEIGHT)
enemies = [1, 1, 0]

# Player variables
lives = 1
is_hidden = False

all_sprites_list = pygame.sprite.Group()
guards_list = pygame.sprite.Group()
bushes_list = pygame.sprite.Group()

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
    for i in range(2):
        positions.append([random.randint(50, 450),random.randint(50, 450)])
    
    return positions

screen = pygame.display.set_mode(size)

# Functions to create enemies
def create_patrol_guard():
    guard = PatrolGuard(GUARD_PATROL_COLOR, 10, 10, 5, random_positions())
    guard.rect.x = random.randint(0, 500)
    guard.rect.y = random.randint(0, 500)
    all_sprites_list.add(guard)
    guards_list.add(guard)

def create_edge_guard():
    guard = PatrolGuard(GUARD_EDGE_COLOR, 10, 10, 5, [[10, 10], [490, 10], [490, 490], [10, 490]])
    guard.rect.x = random.randint(0, 500)
    guard.rect.y = 10
    all_sprites_list.add(guard)
    guards_list.add(guard)

def create_chasing_guard():
    guard = ChasingGuard(GUARD_CHASING_COLOR, 10, 10, 1)
    guard.rect.x = random.randint(0, 500)
    guard.rect.y = random.randint(0, 500)
    all_sprites_list.add(guard)
    guards_list.add(guard)

# def create_shooting_guard():
#     guard = ShootingGuard(GUARD_SHOOTER_COLOR, 10, 10, 6)
#     guard.rect.x = random.randint(0, 500)
#     guard.rect.y = random.randint(0, 500)
#     all_sprites_list.add(guard)
#     guards_list.add(guard)

def summon_guards():
    for i in range(len(enemies)):
        if (i == 0):
            for a in range(enemies[i]):
                create_patrol_guard()
        elif (i == 1):
            for a in range(enemies[i]):
                create_chasing_guard()
        elif (i == 2):
            for a in range(enemies[i]):
                create_edge_guard()

def next_level_animation():
    screen.fill(SURFACE_COLOR)

    block_width = 50
    block_height = 50

    for i in range(int(WIDTH / block_width)):
        for a in range(int(HEIGHT / block_height)):
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            img = pygame.Surface([block_width, block_height])
            img.fill((0, 0, 0))
            screen.blit(img, [block_width * (i), block_height * (a)])
            time.sleep(0.01)
            pygame.display.update()
    
    time.sleep(0.2)

def reset_game():
    next_level_animation()

    global move
    move["up"] = False
    move["down"] = False
    move["left"] = False
    move["right"] = False

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
    
    global enemies
    enemies[0] = level
    enemies[1] = level
    if (level % 5 == 0):
        enemies[2] = int(level / 5)
        
    summon_guards()
    return

def update_player_color():
    global player_color
    global lives

    if (lives == 1):
        player_color = (0, 0, 0) # Black
    elif (lives == 2):
        player_color = (255, 0, 255) # Purple
    elif (lives == 3):
        player_color = (115, 0, 255) # Dark Purple
    elif (lives == 4):
        player_color = (0, 10, 255) # Blue
    elif (lives == 5):
        player_color = (0, 208, 255) # Green -> Blends in with the background
    elif (lives > 5):
        lives = 5
    
    player.image.fill(player_color)

"""
A function that can be used to write text on our screen and buttons
"""
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False

def main_menu():
    running = True

    while running:
        clock.tick(30)

        screen.fill(SURFACE_COLOR)
        draw_text('Main Menu', font, (0,0,0), screen, 200, 40)

        mx, my = pygame.mouse.get_pos()

        #creating buttons
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 180, 200, 50)

        #defining functions when a certain button is pressed
        global click
        if (click):
            print(click)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()

        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #writing text on top of button
        draw_text('PLAY', font, (0,0,0), screen, 220, 115)
        draw_text('SETTINGS', font, (0,0,0), screen, 200, 195)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()

def start_game():
    # Player
    global player
    player = Player(player_color, 10, 10)

    player.rect.x = 50
    player.rect.y = 50

    all_sprites_list.add(player)

    # Guards
    summon_guards()

    # Bushes
    bush3 = Bush(BUSH_COLOR, 30, 30)
    bush3.rect.x = player.rect.x - player.width
    bush3.rect.y = player.rect.y - player.height
    all_sprites_list.add(bush3)
    bushes_list.add(bush3)

    global winArea
    winArea = WinArea(WIN_AREA_COLOR, 70, 70)
    winArea.rect.x = 450
    winArea.rect.y = 450
    all_sprites_list.add(winArea)

    pygame.display.set_caption(f'Level: {level}')

    # Player movement
    global move
    move = {}
    move["up"] = False
    move["down"] = False
    move["left"] = False
    move["right"] = False

def game():
    global level
    global lives
    global player_color

    running = True
    start_game()
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
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    move["up"] = True
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    move["down"] = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    move["right"] = True
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    move["left"] = True

                if event.key == pygame.K_ESCAPE:
                    if (is_paused == True):
                        is_paused = False
                    else:
                        is_paused = True
            
            if event.type == pygame.KEYUP:
                # if keydown event happened
                # than printing a string to output
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    move["up"] = False
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    move["down"] = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    move["right"] = False
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
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
        global is_hidden
        is_hidden = False
        player.image.fill(player_color)
        for bush in bushes_list:
            if pygame.sprite.collide_rect(player, bush):
                is_hidden = True
                player.image.fill(PLAYER_HIDDEN_COLOR)
        
        # Testing if player collides with guard
        for guard in guards_list:
            guard.guard_movement(player.rect)
            if pygame.sprite.collide_rect(player, guard) and not is_hidden:
                lives -= 1
                if (lives == 0):
                    lives = 1

                    level = 1
                    global enemies
                    enemies = [1, 1, 0]
                
                update_player_color()
                reset_game()

        if pygame.sprite.collide_rect(player, winArea) and not is_hidden:
            level += 1
            if level % 5 == 0:
                lives += 1
                update_player_color()
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


"""
This function is called when the "OPTIONS" button is clicked.
"""
def options():
    running = True
    while running:
        clock.tick(30)

        screen.fill(SURFACE_COLOR)
 
        draw_text('SETTINGS', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
       
        pygame.display.update()

game()