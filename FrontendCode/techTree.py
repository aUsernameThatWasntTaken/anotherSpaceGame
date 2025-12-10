from FrontendCode.pyGameWrapper import pygame, pygame_gui

from FrontendCode.helpers import SCREEN_H, SCREEN_W, TREE_ORIGINS, TREE_NODE_WIDTH, TREE_NODE_HEIGHT, TREE_LABELS
from FrontendCode.pyGameWrapper import manager

class TechTreeHandler:
    def __init__(self, techTree):
        self.techTree = techTree

        # Calculate total tree bounds
        max_x = 0
        max_y = 0

        for tech_name, tech_data in techTree.items():
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
        for tech_name, tech_data in self.techTree.items():
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

    def _render_tree_lines(self, TECH_TREE):
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

    def _draw_tech_tree_lines(self, screen):
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
    
    def _draw_custom_tooltip(self, screen):
        if not self.hovered_tech or not self.research_panel_visible:
            return
            
        tech_data = self.techTree[self.hovered_tech]
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
