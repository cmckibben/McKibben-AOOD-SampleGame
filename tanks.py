#!/usr/bin/env python
import pygame, math, sys, os, random
from pygame.locals import *
pygame.init()
import ball
import level
import tank


class Main:
    def __init__(self):
        # Globals

        self.rootpath = ''
        self.SCREENW = 800
        self.SCREENH = 600
        self.BALLSPEED = 4
        self.SHOTDELAY = 10
        self.player1delay = 0
        self.player2delay = 0
        self.Player1Score = 0
        self.Player2Score = 0

        self.THRESHOLD = 0.1

        self.screen = pygame.display.set_mode((self.SCREENW, self.SCREENH))
        pygame.display.set_caption('Tanks by Mr. McKibben')
        self.clock = pygame.time.Clock()
        background_file_name = os.path.join(self.rootpath, "gfx", "background.png")
        self.background = pygame.image.load(background_file_name)
        pygame.font.init()
        self.font = pygame.font.Font(None, 90)
        self.balls = pygame.sprite.Group()

        self.boom_sound = pygame.mixer.Sound(os.path.join(self.rootpath, "snd", "boom.mp3"))
        self.currentlevel = 1
        self.points = 0
        # This dict can be left as-is, since pygame will generate a
        # pygame.JOYDEVICEADDED event for every joystick connected
        # at the start of the program.
        self.joysticks = {}

        self.main()

    def main(self):
        while True:
            self.game_loop()
            if self.points % 4 == 0:
                self.currentlevel += 1
                if self.currentlevel > 3: self.currentlevel = 1

    def init_level(self):
        #### Initialize the level
        self.screen.blit(self.background, (0, 0))
        self.player1 = pygame.sprite.GroupSingle(tank.Tank(1, (80, 340), 180))
        self.player2 = pygame.sprite.GroupSingle(tank.Tank(2, (720, 340), 0))
        self.balls.empty()
        self.walls = level.makelevel(self.currentlevel)

    def end_game(self):
        print('Thanks for playing')
        pygame.quit()
        sys.exit(0)

    def destroy(self, player: tank):
        self.balls.clear(self.screen, self.background)
        self.player1.clear(self.screen, self.background)
        self.player2.clear(self.screen, self.background)
    def game_loop(self):
        self.init_level()
        while 1:
    #### Step 1 clear the screen
            self.balls.clear(self.screen, self.background)
            self.player1.clear(self.screen, self.background)
            self.player2.clear(self.screen, self.background)

    #### Step 2 process input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_game()

                # Handle hotplugging of joysticks
                if event.type == pygame.JOYDEVICEADDED:
                    # This event will be generated when the program starts for every
                    # joystick, filling up the list without needing to create them manually.
                    joy = pygame.joystick.Joystick(event.device_index)
                    self.joysticks[joy.get_instance_id()] = joy

                if event.type == pygame.JOYDEVICEREMOVED:
                    del self.joysticks[event.instance_id]

            if pygame.key.get_pressed()[K_ESCAPE]: self.end_game()

    ### Joystick input, only if a joystick is plugged in
            for joystick in self.joysticks.values():
                if joystick.get_instance_id()==0:
                    if joystick.get_button(0):
                        if self.player1delay <= 0:
                            self.balls.add(ball.Ball(self.BALLSPEED, self.player1.sprite.get_shot_location(), self.player1.sprite.angle))
                            self.player1delay = self.SHOTDELAY
                    if joystick.get_axis(1) > self.THRESHOLD: self.player1.sprite.move_backward(self.walls)
                    if joystick.get_axis(1) < -self.THRESHOLD: self.player1.sprite.move_forward(self.walls)
                    if joystick.get_axis(0) > self.THRESHOLD: self.player1.sprite.rotate_right()
                    if joystick.get_axis(0) < -self.THRESHOLD: self.player1.sprite.rotate_left()
                    if joystick.get_hat(0)[1] == -1: self.player1.sprite.move_backward(self.walls)
                    if joystick.get_hat(0)[1] == 1: self.player1.sprite.move_forward(self.walls)
                    if joystick.get_hat(0)[0] == -1: self.player1.sprite.rotate_left()
                    if joystick.get_hat(0)[0] == 1: self.player1.sprite.rotate_right()
                if joystick.get_instance_id()==1:
                    if joystick.get_button(0):
                        if self.player2delay <= 0:
                            self.balls.add(ball.Ball(self.BALLSPEED, self.player2.sprite.get_shot_location(), self.player2.sprite.angle))
                            self.player1delay = self.SHOTDELAY
                    if joystick.get_axis(1) > self.THRESHOLD: self.player2.sprite.move_backward(self.walls)
                    if joystick.get_axis(1) < -self.THRESHOLD: self.player2.sprite.move_forward(self.walls)
                    if joystick.get_axis(0) > self.THRESHOLD: self.player2.sprite.rotate_right()
                    if joystick.get_axis(0) < -self.THRESHOLD: self.player2.sprite.rotate_left()
                    if joystick.get_hat(0)[1] == -1: self.player2.sprite.move_backward(self.walls)
                    if joystick.get_hat(0)[1] == 1: self.player2.sprite.move_forward(self.walls)
                    if joystick.get_hat(0)[0] == -1: self.player2.sprite.rotate_left()
                    if joystick.get_hat(0)[0] == 1: self.player2.sprite.rotate_right()

    #### Handle Keyboard Controls
            if pygame.key.get_pressed()[K_w]: self.player1.sprite.move_forward(self.walls)
            if pygame.key.get_pressed()[K_s]: self.player1.sprite.move_backward(self.walls)
            if pygame.key.get_pressed()[K_d]: self.player1.sprite.rotate_right()
            if pygame.key.get_pressed()[K_a]: self.player1.sprite.rotate_left()
            if pygame.key.get_pressed()[K_SPACE]:
                if self.player1delay <= 0:
                    self.balls.add(ball.Ball(self.BALLSPEED, self.player1.sprite.get_shot_location(), self.player1.sprite.angle))
                    self.player1delay = self.SHOTDELAY

            if pygame.key.get_pressed()[K_UP]:   self.player2.sprite.move_forward(self.walls)
            if pygame.key.get_pressed()[K_DOWN]: self.player2.sprite.move_backward(self.walls)
            if pygame.key.get_pressed()[K_RIGHT]: self.player2.sprite.rotate_right()
            if pygame.key.get_pressed()[K_LEFT]: self.player2.sprite.rotate_left()
            if pygame.key.get_pressed()[K_RETURN]:
                if self.player2delay <= 0:
                    self.balls.add(ball.Ball(self.BALLSPEED, self.player2.sprite.get_shot_location(), self.player2.sprite.angle))
                    self.player2delay = self.SHOTDELAY

    #### Step 3 Game Logic
    #### Handle if a player is destroyed
            if pygame.sprite.spritecollide(self.player1.sprite, self.balls, False):  # player 1 got shot
                self.Player2Score += 1
                self.points += 1
                self.destroy(self.player1)
                break

            if pygame.sprite.spritecollide(self.player2.sprite, self.balls, False):  # player 2 got shot
                self.Player1Score += 1
                self.points += 1
                self.destroy(self.player2)
                break

    #### Make the shots bounce
            collisions = pygame.sprite.groupcollide(self.balls, self.walls, False, False)
            for ballcollide in collisions:
                for wall in collisions[ballcollide]:
                    ballcollide.reflect(wall)


    #### Decrement the delay until the next shot
            if self.player1delay > 0: self.player1delay -= 1
            if self.player2delay > 0: self.player2delay -= 1

    ##### update the sprites
            self.balls.update()
            self.player1.update()
            self.player2.update()

    #### Step 4 Draw the screen
            score = str(self.Player1Score)
            text = self.font.render(score, True, (255, 255, 255))
            self.screen.blit(text, (20, 20))

            score = str(self.Player2Score)
            text = self.font.render(score, True, (255, 255, 255))
            self.screen.blit(text, (760, 20))

            self.walls.draw(self.screen)
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)
            self.balls.draw(self.screen)
            pygame.display.flip()

    #### Step 5 Wait until the next clock cycle to start the loop again
            self.clock.tick(30)  # 30 fps

if __name__ == '__main__':
    Main()

