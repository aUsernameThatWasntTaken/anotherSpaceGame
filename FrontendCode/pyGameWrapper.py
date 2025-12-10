import pygame
import pygame_gui

from FrontendCode.helpers import SCREEN_H,SCREEN_W

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
manager = pygame_gui.UIManager((SCREEN_W, SCREEN_H), theme_path="theme.json")