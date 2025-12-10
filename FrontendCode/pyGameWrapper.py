import pygame
import pygame_gui

from typing import Protocol

from FrontendCode.helpers import SCREEN_H,SCREEN_W

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
manager = pygame_gui.UIManager((SCREEN_W, SCREEN_H), theme_path="theme.json")

class Togglable(Protocol):
    def show(self): ...
    def hide(self): ...

class ToggledPanel:
    """While designed with gygame_gui UIPanels in mind, works with any object with a hide and show method"""
    def __init__(self, panel: Togglable, visible = False):
        self.panel = panel
        self.visible = visible
        self.hide = self.panel.hide
        self.show = self.panel.show
    
    def toggle(self):
        self.visible = not self.visible
        if self.visible:
            self.panel.show()
        else:
            self.panel.hide()