# 文件: dice.py
import random
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
#Random: Used to generate random dice points (1 to 6)
#Pygame: A necessary Pygame library 
#Constants: Import the width and height of the screen to calculate the position of the dice


class Dice:
    def __init__(self):
        self.value = 1
        self.size = 80
        self.rect = pygame.Rect(SCREEN_WIDTH - self.size - 20, 
                                SCREEN_HEIGHT - self.size - 20, 
                                self.size, self.size)
        # Defined the position and clickable area of the dice



        self.font = pygame.font.Font(None, 48)
        # Initialize font to display the number of points within the dice rectangle



    def roll(self):
        self.value = random.randint(1, 6)
        return self.value
    # Generate a random number: Generate a random integer between 1 and 6. 
    # Assign this random number to the instance property 'self. value'. there self value is 1 before



    def draw(self, screen):
        
        pygame.draw.rect(screen, (255, 255, 255), self.rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=10)
        #Draw the appearance of dice 


        txt = self.font.render(str(self.value), True, (0, 0, 0))
        txt_r = txt.get_rect(center=self.rect.center)
        screen.blit(txt, txt_r)