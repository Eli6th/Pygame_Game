import pygame
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

all_sprites_list = pygame.sprite.Group()

guards_list = pygame.sprite.Group()

bushes_list = pygame.sprite.Group()

player = Player(PLAYER_COLOR, 10, 10)
guard1 = Guard(GUARD_COLOR, 10, 10, 0)
bush1 = Bush(BUSH_COLOR, 30, 30)

player.rect.x = 450
player.rect.y = 450

guard1.rect.x = random.randint(50, 350)
guard1.rect.y = random.randint(50, 350)

bush1.rect.x = random.randint(50, 350)
bush1.rect.y = random.randint(50, 350)

all_sprites_list.add(player)
all_sprites_list.add(guard1)
all_sprites_list.add(bush1)

guards_list.add(guard1)

bushes_list.add(bush1)

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(SURFACE_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.K_w and player.rect.y < 500:
            player.rect.y += 1
        elif event.type == pygame.K_s and player.rect.y > 0:
            player.rect.y -= 1
        elif event.type == pygame.K_d and player.rect.x < 500:
            player.rect.x += 1
        elif event.type == pygame.K_a and player.rect.x > 0:
            player.rect.x -= 1
        elif event.type == pygame.K_UP and player.rect.y < 470 and jumps > 0:
            player.rect.y += 30
            jumps -= 1
        elif event.type == pygame.K_DOWN and player.rect.y > 30 and jumps > 0:
            player.rect.y -= 30
            jumps -= 1
        elif event.type == pygame.K_RIGHT and player.rect.x < 470 and jumps > 0:
            player.rect.x += 30
            jumps -= 1
        elif event.type == pygame.K_LEFT and player.rect.x > 30 and jumps > 0:
            player.rect.x -= 30
            jumps -= 1
        else:
            player.rect.x += 0

    for bush in bushes_list:
        if pygame.sprite.collide_rect(player, bush):
            is_hidden = True
        else:
            is_hidden = False

    for guard in guards_list:
        if guard.rect.x > 475 or guard.rect.x < 25:
            guard.bounces += 1

        if ((abs(guard.rect.x - player.rect.x) < 100) and (abs(guard.rect.y - player.rect.y) < 100) and not is_hidden):
            if guard.rect.x < player.rect.x and guard.rect.y < player.rect.y:
                guard.rect.x += 2
                guard.rect.y += 2
            elif guard.rect.x < player.rect.x and guard.rect.y > player.rect.y:
                guard.rect.x += 2
                guard.rect.y -= 2
            elif guard.rect.x > player.rect.x and guard.rect.y < player.rect.y:
                guard.rect.x -= 2
                guard.rect.y += 2
            else:
                guard.rect.x -= 2
                guard.rect.x -= 2
        else:
            if guard.bounces % 2 == 0:
                guard.rect.x += 1
            else:
                guard.rect.x -= 1

        if pygame.sprite.collide_rect(guard, player):
            running = False

        if pygame.time.get_ticks() % 1000 == 0 and jumps == 0:
            jumps += 1

        if player.rect.x < 50 and player.rect.y < 50:
            level += 1

            new_guard = Guard(GUARD_COLOR, 10, 10, 0)

            new_guard.rect.x = random.randint(50, 350)
            new_guard.rect.y = random.randint(50, 350)

            all_sprites_list.add(new_guard)

            guards_list.add(new_guard)

            if level < 4:
                new_bush = Bush(BUSH_COLOR, 30, 30)
                new_bush.rect.x = random.randint(50, 350)
                new_bush.rect.y = random.randint(50, 350)

                all_sprites_list.add(new_bush)
                bushes_list.add(new_bush)

            for guard in all_sprites_list:
                guard.rect.x = random.randint(50, 350)
                guard.rect.y = random.randint(50, 350)

            player.rect.x = 450
            player.rect.y = 450

    all_sprites_list.draw(screen)

    pygame.draw.circle(screen, (0, 0, 255), (25, 25), 50)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()