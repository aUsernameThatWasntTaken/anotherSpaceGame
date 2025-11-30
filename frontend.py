import pygame
import pygame_gui
import os
from BackendCode.gameLogic import GameHandler
from BackendCode.errors import StopGame

SCREEN_W = 1280
SCREEN_H = 720

pygame.init()
screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
manager = pygame_gui.UIManager((SCREEN_W,SCREEN_H), theme_path="theme.json")
running = True #I think this is no longer needed -Max

# helpers
def scale_to_offset(scale_size, width_height):
    if width_height == "width":
        return (scale_size*SCREEN_W)
    elif width_height == "height":
        return (scale_size*SCREEN_H)
    else:
        raise Exception('Incorrect Parameter. Use "width" or "height".')

def centered_rect(center_x_scale, center_y_scale, width_scale, height_scale):
    width = scale_to_offset(width_scale, "width")
    height = scale_to_offset(height_scale, "height")
    center_x = scale_to_offset(center_x_scale, "width")
    center_y = scale_to_offset(center_y_scale, "height")
    
    top_left_x = center_x - width/2
    top_left_y = center_y - height/2
    
    return pygame.Rect((top_left_x, top_left_y), (width, height))
class GUIhandler: #rename if you want
    def __init__(self, gameHandler: GameHandler):
        self.selectedPayload = "com"
        def preparePayload():
            gameHandler.payloadFuncs[self.selectedPayload]() #gets function for selected payload and calls it
        # UI
        prepare_payload_button = pygame_gui.elements.UIButton(relative_rect=centered_rect(0.15, 0.9, 0.2, 0.1),
                                                                text='PREPARE PAYLOAD',
                                                                manager=manager,
                                                                command=preparePayload)
        # bottom right buttons in a horizontal line
        build_button = pygame_gui.elements.UIButton(relative_rect=centered_rect(0.75, 0.9, 0.1, 0.1),
                                                    text='BUILD',
                                                    manager=manager,
                                                    object_id='#build_btn',
                                                    command=gameHandler.world.buildRocket)
        research_button = pygame_gui.elements.UIButton(relative_rect=centered_rect(0.875, 0.9, 0.1, 0.1),
                                                    text='RESEARCH',
                                                    manager=manager,
                                                    object_id='#research_btn')
        payload_button = pygame_gui.elements.UIButton(relative_rect=centered_rect(0.625, 0.9, 0.1, 0.1),
                                                    text='CIV',
                                                    manager=manager,
                                                    object_id='#payload_btn')

    def update(self, gameHandler: GameHandler, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise StopGame()
            
            manager.process_events(event)
        
        manager.update(dt)
        manager.draw_ui(screen)
        pygame.display.update()

saveFile = "None"
GameHandler(saveFile).run(GUIhandler)

# things we need

# save and quit option
# launchpad INFO (get stats using gameHandler.world.getStats())
# "buy new launchpad" and "upgrade VAB" buttons (I will add the functionality soon -Max)
# tech tree & research
# cargo selection (COMMERCIAL/SCIENTIFIC/SPACESHIP)
# money!