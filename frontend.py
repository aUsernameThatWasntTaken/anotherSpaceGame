import pygame
import pygame_gui
import os
from BackendCode.gameLogic import GameHandler
from BackendCode.errors import StopGame, NotEnoughMoney
from BackendCode.saves import getTechTree

# note for future us: this was 849 lines at one point

# also, there's a bunch of UserWarning from pygame_gui, such as 
# Clamping shape_corner_radius of: 25, to: 18
# and
# Label Rect is too small for text: placeholder text - size diff: (154, -2)
# and the GUI isn't showing.
# I downloaded the source code before my newest changes, it still didn't show, so I didn't break anything.

SCREEN_W = 1920
SCREEN_H = 1080

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
manager = pygame_gui.UIManager((SCREEN_W, SCREEN_H), theme_path="theme.json")


# helpers
def scale_to_offset(scale_size, width_height):
    if width_height == "width":
        return scale_size * SCREEN_W
    elif width_height == "height":
        return scale_size * SCREEN_H
    else:
        raise Exception('Incorrect Parameter. Use "width" or "height".')


def centered_rect(center_x_scale, center_y_scale, width_scale, height_scale):
    width = scale_to_offset(width_scale, "width")
    height = scale_to_offset(height_scale, "height")
    center_x = scale_to_offset(center_x_scale, "width")
    center_y = scale_to_offset(center_y_scale, "height")

    top_left_x = center_x - width / 2
    top_left_y = center_y - height / 2

    return pygame.Rect((top_left_x, top_left_y), (width, height))


# hardcoded but whatever
# 30 techs, 3 trees (2 large, 1 small)
# Positions are (x, y) in pixels from tree origin
# Trees branch OUT (end with multiple techs, not converge to 1)

TECH_TREE = getTechTree()

# === TREE 1 (Top - Large, techs 1-12) - branches outward ===
# === TREE 2 (Middle - Large, techs 13-24) - branches outward ===
# === TREE 3 (Bottom - Small, techs 25-30) - branches outward ===
  
# Tree layout constants
TREE_NODE_WIDTH = 140
TREE_NODE_HEIGHT = 40
TREE_ORIGINS = [
    (100, 50),       # Tree 1 origin (top)
    (100, 400),      # Tree 2 origin (middle)
    (100, 750),      # Tree 3 origin (bottom)
]
TREE_LABELS = ["TREE 1", "TREE 2", "TREE 3"]


class GUIhandler:
    def __init__(self, gameHandler: GameHandler):
        self.gameHandler = gameHandler
        self.selectedPayload = "COMMERCIAL"
        self.info_panel_visible = False
        self.research_panel_visible = False
        self.settings_panel_visible = False

        # Store tech buttons for event handling
        self.tech_buttons = {}
        self.tech_node_positions = {}  # Base positions of each node center

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

        self._create_ui()
        self._create_tech_tree()

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
        self._create_info_panel()

    def _create_settings_panel(self):
        panel_width = 400
        panel_height = 200
        self.settings_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                (SCREEN_W - panel_width) // 2,
                (SCREEN_H - panel_height) // 2,
                panel_width,
                panel_height
            ),
            manager=manager
        )
        self.settings_panel.hide()

        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), (380, 30)),
            text="Settings",
            manager=manager,
            container=self.settings_panel,
        )

        self.save_quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((panel_width - 200) // 2, 70), (200, 50)),
            text="Save & Quit",
            manager=manager,
            container=self.settings_panel,
        )

    def _create_info_panel(self):
        panel_width = 350
        panel_height = 400
        self.info_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                (SCREEN_W - panel_width) // 2,
                (SCREEN_H - panel_height) // 2,
                panel_width,
                panel_height
            ),
            manager=manager
        )
        self.info_panel.hide()

        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), (330, 30)),
            text="placeholder text",
            manager=manager,
            container=self.info_panel,
        )

        self.launches_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 60), (330, 25)),
            text="placeholder text",
            manager=manager,
            container=self.info_panel,
        )

        self.success_rate_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 90), (330, 25)),
            text="placeholder text",
            manager=manager,
            container=self.info_panel,
        )

        self.payload_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 120), (330, 25)),
            text="placeholder text",
            manager=manager,
            container=self.info_panel,
        )

        self.vab_level_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 150), (330, 25)),
            text="placeholder text",
            manager=manager,
            container=self.info_panel,
        )

        button_width = 200
        self.buy_launchpad_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((panel_width - button_width) // 2, 200), (button_width, 50)),
            text="Buy New Launchpad",
            manager=manager,
            container=self.info_panel,
        )

        self.upgrade_vab_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((panel_width - button_width) // 2, 270), (button_width, 50)),
            text="Upgrade VAB",
            manager=manager,
            container=self.info_panel,
        )

    def _create_tech_tree(self):
        # Calculate total tree bounds
        max_x = 0
        max_y = 0

        for tech_name, tech_data in TECH_TREE.items():
            tree_idx = tech_data["tree"]
            origin_x, origin_y = TREE_ORIGINS[tree_idx]
            pos_x, pos_y = tech_data["pos"]

            abs_x = origin_x + pos_x + TREE_NODE_WIDTH
            abs_y = origin_y + pos_y + TREE_NODE_HEIGHT

            max_x = max(max_x, abs_x)
            max_y = max(max_y, abs_y)

        self.tree_surface_size = (max_x + 100, max_y + 100)

        # Create research panel (contains tech tree) - not full screen
        panel_width = 1400
        panel_height = 800
        panel_x = (SCREEN_W - panel_width) // 2
        panel_y = (SCREEN_H - panel_height) // 2
        
        self.research_panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        
        self.research_panel = pygame_gui.elements.UIPanel(
            relative_rect=self.research_panel_rect,
            manager=manager,
            object_id="#research_panel",
        )
        self.research_panel.hide()

        # Create research title label inside panel
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((panel_width // 2 - 100, 10), (200, 40)),
            text="Research",
            manager=manager,
            container=self.research_panel,
        )

        # Create buttons for each tech INSIDE the research panel (auto-clipped)
        for tech_name, tech_data in TECH_TREE.items():
            tree_idx = tech_data["tree"]
            origin_x, origin_y = TREE_ORIGINS[tree_idx]
            pos_x, pos_y = tech_data["pos"]

            # Calculate position relative to panel
            center_x = origin_x + pos_x + TREE_NODE_WIDTH // 2
            center_y = origin_y + pos_y + TREE_NODE_HEIGHT // 2

            self.tech_node_positions[tech_name] = (center_x, center_y)

            # Button position (will be offset by pan later)
            btn_x = center_x - TREE_NODE_WIDTH // 2
            btn_y = center_y - TREE_NODE_HEIGHT // 2

            # Short display name for button
            short_name = tech_name.replace("Dummy Tech ", "Tech ")

            # Buttons are children of the panel - pygame_gui clips them automatically
            tech_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((btn_x, btn_y), (TREE_NODE_WIDTH, TREE_NODE_HEIGHT)),
                text=short_name,
                manager=manager,
                container=self.research_panel,
                object_id="#tech_btn",
            )
            self.tech_buttons[tech_name] = tech_button

        # Pre-render tree lines surface
        self._render_tree_lines()

    def _render_tree_lines(self):
        self.tree_surface = pygame.Surface(self.tree_surface_size, pygame.SRCALPHA)
        self.tree_surface.fill((0, 0, 0, 0))

        line_color = (100, 150, 200)
        line_width = 3

        # Draw tree labels
        font = pygame.font.Font(None, 36)
        for i, label in enumerate(TREE_LABELS):
            origin_x, origin_y = TREE_ORIGINS[i]
            text_surface = font.render(label, True, (150, 180, 220))
            self.tree_surface.blit(text_surface, (origin_x, origin_y - 40))

        # Draw connections
        for tech_name, tech_data in TECH_TREE.items():
            end_pos = self.tech_node_positions[tech_name]

            for prereq_name in tech_data["prerequisites"]:
                if prereq_name in self.tech_node_positions:
                    start_pos = self.tech_node_positions[prereq_name]

                    # Draw bezier-like connection
                    start_x = start_pos[0] + TREE_NODE_WIDTH // 2
                    start_y = start_pos[1]
                    end_x = end_pos[0] - TREE_NODE_WIDTH // 2
                    end_y = end_pos[1]

                    mid_x = (start_x + end_x) // 2

                    # Draw line segments
                    pygame.draw.line(self.tree_surface, line_color, (start_x, start_y), (mid_x, start_y), line_width)
                    pygame.draw.line(self.tree_surface, line_color, (mid_x, start_y), (mid_x, end_y), line_width)
                    pygame.draw.line(self.tree_surface, line_color, (mid_x, end_y), (end_x, end_y), line_width)

                    # Draw connection points
                    pygame.draw.circle(self.tree_surface, line_color, (start_x, start_y), 5)
                    pygame.draw.circle(self.tree_surface, line_color, (end_x, end_y), 5)

    def _update_tech_tree_positions(self):
        for tech_name, tech_button in self.tech_buttons.items():
            base_pos = self.tech_node_positions[tech_name]

            # Position relative to panel container
            new_x = base_pos[0] - TREE_NODE_WIDTH // 2 + self.pan_offset_x
            new_y = base_pos[1] - TREE_NODE_HEIGHT // 2 + self.pan_offset_y

            tech_button.set_relative_position((new_x, new_y))

    def _show_tech_tree(self):
        # Center the tree within the panel
        self.pan_offset_x = 50
        self.pan_offset_y = 50
        
        self.research_panel.show()
        self._update_tech_tree_positions()

    def _hide_tech_tree(self):
        self.research_panel.hide()
        self.hovered_tech = None

    def _draw_tech_tree_lines(self):
        if not self.research_panel_visible or not self.tree_surface:
            return
        
        panel = self.research_panel_rect
        
        # Set clip to panel bounds
        old_clip = screen.get_clip()
        screen.set_clip(panel)
        
        # Draw at panel position + pan offset
        draw_x = panel.x + self.pan_offset_x
        draw_y = panel.y + self.pan_offset_y
        screen.blit(self.tree_surface, (draw_x, draw_y))
        
        # Restore clip
        screen.set_clip(old_clip)
    
    def _check_tech_hover(self):
        if not self.research_panel_visible:
            self.hovered_tech = None
            return
            
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_tech = None
        
        # Check if mouse is in panel first
        if not self.research_panel_rect.collidepoint(mouse_pos):
            return
        
        for tech_name, tech_button in self.tech_buttons.items():
            if tech_button.rect.collidepoint(mouse_pos):
                self.hovered_tech = tech_name
                break
    
    def _draw_custom_tooltip(self):
        if not self.hovered_tech or not self.research_panel_visible:
            return
            
        tech_data = TECH_TREE[self.hovered_tech]
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Build tooltip lines
        lines = []
        lines.append((self.hovered_tech, True))  # Bold title
        lines.append(("", False))  # Spacer
        lines.append((f"Cost: ${tech_data['cost']}", False))
        lines.append(("", False))  # Spacer
        lines.append((tech_data['description'], False))
        lines.append(("", False))  # Spacer
        prereq_text = ", ".join(tech_data["prerequisites"]) if tech_data["prerequisites"] else "None"
        lines.append((f"Prerequisites: {prereq_text}", False))
        
        # Calculate tooltip size
        padding = 10
        line_height = 22
        max_width = 0
        
        for text, is_bold in lines:
            font = self.tooltip_font_bold if is_bold else self.tooltip_font
            text_surface = font.render(text, True, (255, 255, 255))
            max_width = max(max_width, text_surface.get_width())
        
        tooltip_width = max_width + padding * 2
        tooltip_height = len(lines) * line_height + padding * 2
        
        # Position tooltip (offset from mouse, keep on screen)
        tooltip_x = mouse_x + 15
        tooltip_y = mouse_y + 15
        
        # Keep on screen
        if tooltip_x + tooltip_width > SCREEN_W:
            tooltip_x = mouse_x - tooltip_width - 10
        if tooltip_y + tooltip_height > SCREEN_H:
            tooltip_y = mouse_y - tooltip_height - 10
        
        # Draw tooltip background
        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
        pygame.draw.rect(screen, (30, 35, 45), tooltip_rect)
        pygame.draw.rect(screen, (100, 150, 200), tooltip_rect, 2)
        
        # Draw tooltip text
        y_offset = tooltip_y + padding
        for text, is_bold in lines:
            if text:
                font = self.tooltip_font_bold if is_bold else self.tooltip_font
                text_surface = font.render(text, True, (255, 255, 255))
                screen.blit(text_surface, (tooltip_x + padding, y_offset))
            y_offset += line_height

    def _toggle_info_panel(self):
        self.info_panel_visible = not self.info_panel_visible
        if self.info_panel_visible:
            self._update_info_panel()
            self.info_panel.show()
        else:
            self.info_panel.hide()

    def _toggle_research_panel(self):
        self.research_panel_visible = not self.research_panel_visible
        if self.research_panel_visible:
            self._show_tech_tree()
        else:
            self.is_panning = False
            self._hide_tech_tree()

    def _toggle_settings_panel(self):
        self.settings_panel_visible = not self.settings_panel_visible
        if self.settings_panel_visible:
            self.settings_panel.show()
        else:
            self.settings_panel.hide()

    def _cycle_payload(self):
        payload_types = ["COMMERCIAL", "SCIENTIFIC", "SPACESHIP"]
        current_index = payload_types.index(self.selectedPayload)
        self.selectedPayload = payload_types[(current_index + 1) % len(payload_types)]
        self.payload_button.set_text(self.selectedPayload[:3])

    def _prepare_payload(self):
        self.gameHandler.payloadFuncs[self.selectedPayload]()

    def _update_info_panel(self):
        try:
            stats = self.gameHandler.world.getStats()
            self.launches_label.set_text(f"Launches: {stats.get('launches', 0)}")
            self.success_rate_label.set_text(
                f"Success Rate: {stats.get('success_rate', 0)}%"
            )
            self.payload_label.set_text(
                f"Total Payload: {stats.get('total_payload', 0)} kg"
            )
            self.vab_level_label.set_text(f"VAB Level: {stats.get('vab_level', 1)}")
        except (AttributeError, KeyError):
            pass

    def _update_money_display(self):
        try:
            money = self.gameHandler.world.getMoney()
            self.money_label.set_text(f"${money:,}")
        except AttributeError:
            pass

    def _handle_button_event(self, event):
        ui_element = event.ui_element

        # Main buttons
        if ui_element == self.prepare_payload_button:
            self._prepare_payload()
        elif ui_element == self.build_button:
            self.gameHandler.world.buildRocket()
        elif ui_element == self.research_button:
            self._toggle_research_panel()
        elif ui_element == self.payload_button:
            self._cycle_payload()
        elif ui_element == self.settings_button:
            self._toggle_settings_panel()
        elif ui_element == self.info_button:
            self._toggle_info_panel()

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

    def update(self, gameHandler: GameHandler, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise StopGame()

            # Handle panning for research panel
            if self.research_panel_visible:
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
                        self._update_tech_tree_positions()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                try:
                    self._handle_button_event(event)
                except NotEnoughMoney:
                    pass

            manager.process_events(event)

        # Update dynamic displays
        self._update_money_display()
        
        # Check tech hover for custom tooltip
        self._check_tech_hover()

        # Clear screen
        screen.fill((20, 25, 30))

        # Draw overlay if research visible
        if self.research_panel_visible:
            screen.blit(self.overlay_surface, (0, 0))

        manager.update(dt)
        manager.draw_ui(screen)
        
        # Draw tech tree lines AFTER panel but they get covered by buttons
        # So we draw them, then redraw just the buttons on top
        self._draw_tech_tree_lines()
        
        # Draw custom tooltip AFTER gui elements (on top)
        self._draw_custom_tooltip()
        
        pygame.display.update()


saveFile = "None"
GameHandler(saveFile).run(GUIhandler)

# things we need

# save and quit option
# IMPORTANT: launchpad INFO (get stats using gameHandler.world.getStats())
# "buy new launchpad" and "upgrade VAB" buttons (I will add the functionality soon -Max)
# tech tree & research
# cargo selection (COMMERCIAL/SCIENTIFIC/SPACESHIP)
# money!