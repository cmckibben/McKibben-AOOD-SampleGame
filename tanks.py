#!/usr/bin/env python
import pygame, math, sys, os, random
from pygame.locals import *
import ball
import level
import tank

# Globals

rootpath = ''  # '/home/chris/docs/Documents/Programming/tanks'
SCREENW = 800
SCREENH = 600
BALLSPEED = 4
SHOTDELAY = 10
player1delay = 0
player2delay = 0
Player1Score = 0
Player2Score = 0

THRESHOLD = 0.1

pygame.init()

screen = pygame.display.set_mode((SCREENW, SCREENH))
pygame.display.set_caption('Tanks by Mr. McKibben')
clock = pygame.time.Clock()
background_file_name = os.path.join(rootpath, "gfx", "background.png")
background = pygame.image.load(background_file_name)
pygame.font.init()
font = pygame.font.Font(None, 90)
balls = pygame.sprite.Group()

currentlevel = 1
points = 0
# This dict can be left as-is, since pygame will generate a
# pygame.JOYDEVICEADDED event for every joystick connected
# at the start of the program.
joysticks = {}

def end_game():
    print('Thanks for playing')
    pygame.quit()
    sys.exit(0)

def init():
    pass


def main():
    screen.blit(background, (0, 0))
    player1 = pygame.sprite.GroupSingle(tank.Tank(1, (80, 340), 180))
    player2 = pygame.sprite.GroupSingle(tank.Tank(2, (720, 340), 0))
    balls.empty()
    global player1delay, player2delay, Player1Score, Player2Score, currentlevel, points



    walls = level.makelevel(currentlevel)
    while 1:
        # clear the screen
        balls.clear(screen, background)
        player1.clear(screen, background)
        player2.clear(screen, background)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game()

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")


        if pygame.key.get_pressed()[K_ESCAPE]: end_game()

        for joystick in joysticks.values():
            if joystick.get_instance_id()==0:
                if joystick.get_button(0):
                    if player1delay <= 0:
                        balls.add(ball.Ball(BALLSPEED, player1.sprite.get_shot_location(), player1.sprite.angle))
                        player1delay = SHOTDELAY
                if joystick.get_axis(1) > THRESHOLD: player1.sprite.move_backward(walls)
                if joystick.get_axis(1) < -THRESHOLD: player1.sprite.move_forward(walls)
                if joystick.get_axis(0) > THRESHOLD: player1.sprite.rotate_right()
                if joystick.get_axis(0) < -THRESHOLD: player1.sprite.rotate_left()
                if joystick.get_hat(0)[1] == -1: player1.sprite.move_backward(walls)
                if joystick.get_hat(0)[1] == 1: player1.sprite.move_forward(walls)
                if joystick.get_hat(0)[0] == -1: player1.sprite.rotate_left()
                if joystick.get_hat(0)[0] == 1: player1.sprite.rotate_right()

        if pygame.key.get_pressed()[K_w]: player1.sprite.move_forward(walls)
        if pygame.key.get_pressed()[K_s]: player1.sprite.move_backward(walls)
        if pygame.key.get_pressed()[K_d]: player1.sprite.rotate_right()
        if pygame.key.get_pressed()[K_a]: player1.sprite.rotate_left()
        if pygame.key.get_pressed()[K_SPACE]:
            if player1delay <= 0:
                balls.add(ball.Ball(BALLSPEED, player1.sprite.get_shot_location(), player1.sprite.angle))
                player1delay = SHOTDELAY

        if pygame.key.get_pressed()[K_UP]:   player2.sprite.move_forward(walls)
        if pygame.key.get_pressed()[K_DOWN]: player2.sprite.move_backward(walls)
        if pygame.key.get_pressed()[K_RIGHT]: player2.sprite.rotate_right()
        if pygame.key.get_pressed()[K_LEFT]: player2.sprite.rotate_left()
        if pygame.key.get_pressed()[K_RETURN]:
            if player2delay <= 0:
                balls.add(ball.Ball(BALLSPEED, player2.sprite.get_shot_location(), player2.sprite.angle))
                player2delay = SHOTDELAY

        if pygame.sprite.spritecollide(player1.sprite, balls, False):  # player 1 got shot
            Player2Score += 1
            points += 1
            break

        if pygame.sprite.spritecollide(player2.sprite, balls, False):  # player 2 got shot
            Player1Score += 1
            points += 1
            break


        collisions = pygame.sprite.groupcollide(balls, walls, False, False)
        for ballcollide in collisions:
            for wall in collisions[ballcollide]:
                ballcollide.reflect(wall)

        score = repr(Player1Score)
        text = font.render(score, True, (255, 255, 255))
        screen.blit(text, (20, 20))

        score = repr(Player2Score)
        text = font.render(score, True, (255, 255, 255))
        screen.blit(text, (760, 20))

        balls.update()
        player1.update()
        player2.update()

        walls.draw(screen)
        player1.draw(screen)
        player2.draw(screen)
        balls.draw(screen)
        pygame.display.flip()
        if player1delay > 0: player1delay -= 1
        if player2delay > 0: player2delay -= 1
        clock.tick(30)  # 30 fps

while 1:
    # global currentlevel, points
    main()

    if points % 4 == 0:
        currentlevel += 1
        if currentlevel > 3: currentlevel = 1
