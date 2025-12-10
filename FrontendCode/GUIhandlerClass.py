from FrontendCode.pyGameWrapper import pygame, pygame_gui # Uses the same instances as pyGameWrapper (In the future, we will not interact with this directly)

from BackendCode.backendInterface import Backend, StopGame, NotEnoughMoney

from FrontendCode.pyGameWrapper import screen, manager, ToggledPanel
from FrontendCode.helpers import SCREEN_H, SCREEN_W
from FrontendCode.techTree import TechTreeHandler
from FrontendCode.infoPanel import InfoPanel

class GUIhandler:
    def __init__(self, gameHandler: Backend, techTree):
        # self.gameHandler = gameHandler  # please don't do this, The gameHandler should be passed into
                                          # update() each time to ensure that the data updates properly
        self.selectedPayload = "COMMERCIAL"

        self.techTree = techTree

        self.buildRocketFunction = gameHandler.buildRocket

        # Panning state for tech tree
        self.is_panning = False
        self.pan_start_pos = (0, 0)
        self.pan_offset_x = 0
        self.pan_offset_y = 0

        # Surface for drawing tech tree lines
        self.tree_surface = None
        self.tree_surface_size = (0, 0)
        
        # Semi-transparent overlay for research view
        self.overlay_surface = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        self.overlay_surface.fill((0, 0, 0, 180))
        
        # Custom tooltip state
        self.hovered_tech = None
        self.tooltip_font = pygame.font.Font(None, 24)
        self.tooltip_font_bold = pygame.font.Font(None, 28)

        # Tech tree handler
        self.techTreeHandler = TechTreeHandler(techTree)

        self._create_ui()

    def _create_ui(self):
        # Money display (top center)
        self.money_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((SCREEN_W // 2 - 100, 10), (200, 40)),
            text="$0",
            manager=manager,
            object_id="#money_label",
        )

        # Bottom center button row
        button_width = 160
        button_height = 70
        button_spacing = 20
        total_buttons = 4
        total_width = total_buttons * button_width + (total_buttons - 1) * button_spacing
        start_x = (SCREEN_W - total_width) // 2
        button_y = SCREEN_H - 100

        # Prepare payload button
        self.prepare_payload_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((start_x, button_y), (button_width, button_height)),
            text="PREPARE",
            manager=manager,
        )

        # Payload type button
        self.payload_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((start_x + button_width + button_spacing, button_y), (button_width, button_height)),
            text="COM",
            manager=manager,
            object_id="#payload_btn",
        )

        # Build button
        self.build_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((start_x + 2 * (button_width + button_spacing), button_y), (button_width, button_height)),
            text="BUILD",
            manager=manager,
            object_id="#build_btn",
        )

        # Research button
        self.research_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((start_x + 3 * (button_width + button_spacing), button_y), (button_width, button_height)),
            text="RESEARCH",
            manager=manager,
            object_id="#research_btn",
        )

        # Settings button (top right)
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_W - 130, 10), (120, 40)),
            text="SETTINGS",
            manager=manager,
        )

        # Info button (top left)
        self.info_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (130, 40)),
            text="LAUNCHPAD",
            manager=manager,
        )

        self._create_settings_panel()
        self.info_panel = InfoPanel(manager)

    def _create_settings_panel(self):
        panel_width = 400
        panel_height = 200
        self.settings_panel = ToggledPanel(pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                (SCREEN_W - panel_width) // 2,
                (SCREEN_H - panel_height) // 2,
                panel_width,
                panel_height
            ),
            manager=manager
        ))
        self.settings_panel.hide()

        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), (380, 30)),
            text="Settings",
            manager=manager,
            container=self.settings_panel.panel,
        )

        self.save_quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((panel_width - 200) // 2, 70), (200, 50)),
            text="Save & Quit",
            manager=manager,
            container=self.settings_panel.panel,
        )

    def _cycle_payload(self):
        payload_types = ["COMMERCIAL", "SCIENTIFIC", "SPACESHIP"]
        current_index = payload_types.index(self.selectedPayload)
        self.selectedPayload = payload_types[(current_index + 1) % len(payload_types)]
        self.payload_button.set_text(self.selectedPayload[:3]) # hehe :3 -Max

    def _prepare_payload(self, gameHandler: Backend):
        gameHandler.payloadFuncs[self.selectedPayload]()

    def _update_money_display(self, gameHandler: Backend):
        try:
            money = gameHandler.getMoney()
            self.money_label.set_text(f"${money:,}")
        except AttributeError:
            pass

    def _handle_button_event(self, event):
        ui_element = event.ui_element

        # Main buttons
        if ui_element == self.prepare_payload_button:
            self._prepare_payload()
        elif ui_element == self.build_button:
            self.buildRocketFunction()
        elif ui_element == self.research_button:
            self.techTreeHandler.toggle()
        elif ui_element == self.payload_button:
            self._cycle_payload()
        elif ui_element == self.settings_button:
            self.settings_panel.toggle()
        elif ui_element == self.info_button:
            self.info_panel.toggle()

        # Panel buttons
        elif ui_element == self.save_quit_button:
            pygame.quit()
            raise StopGame()
        elif ui_element == self.buy_launchpad_button:
            pass
        elif ui_element == self.upgrade_vab_button:
            pass

        # Tech tree buttons
        else:
            for tech_name, tech_button in self.tech_buttons.items():
                if ui_element == tech_button:
                    print(f"Research: {tech_name}")
                    break

    def update(self, gameHandler: Backend, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise StopGame()

            # Handle panning for research panel
            if self.techTreeHandler.visible:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click to pan
                        self.is_panning = True
                        self.pan_start_pos = pygame.mouse.get_pos()
                    elif event.button == 2:  # Middle click also pans
                        self.is_panning = True
                        self.pan_start_pos = pygame.mouse.get_pos()

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 or event.button == 2:
                        self.is_panning = False

                elif event.type == pygame.MOUSEMOTION:
                    if self.is_panning:
                        mouse_pos = pygame.mouse.get_pos()
                        dx = mouse_pos[0] - self.pan_start_pos[0]
                        dy = mouse_pos[1] - self.pan_start_pos[1]
                        self.pan_offset_x += dx
                        self.pan_offset_y += dy
                        self.pan_start_pos = mouse_pos
                        self.techTreeHandler._update_tech_tree_positions()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                try:
                    self._handle_button_event(event)
                except NotEnoughMoney:
                    pass

            manager.process_events(event)

        # Update dynamic displays
        self._update_money_display(gameHandler)
        
        # Check tech hover for custom tooltip
        self.techTreeHandler._check_tech_hover()

        # Clear screen
        screen.fill((20, 25, 30))

        # Draw overlay if research visible
        if self.techTreeHandler.visible:
            screen.blit(self.overlay_surface, (0, 0))

        manager.update(dt)
        manager.draw_ui(screen)
        
        # Draw tech tree lines AFTER panel but they get covered by buttons
        # So we draw them, then redraw just the buttons on top
        self.techTreeHandler._draw_tech_tree_lines()
        
        # Draw custom tooltip AFTER gui elements (on top)
        self.techTreeHandler._draw_custom_tooltip()
        
        pygame.display.update()