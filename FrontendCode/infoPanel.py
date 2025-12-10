from pygame_gui.elements import UIPanel, UILabel, UIButton
from pygame import Rect

from FrontendCode.helpers import SCREEN_H, SCREEN_W
from FrontendCode.pyGameWrapper import ToggledPanel

class InfoPanel:
    def __init__(self, manager):
        panel_width = 350
        panel_height = 400
        self.info_panel = ToggledPanel(UIPanel(
            relative_rect=Rect(
                (SCREEN_W - panel_width) // 2,
                (SCREEN_H - panel_height) // 2,
                panel_width,
                panel_height
            ),
            manager=manager
        ))
        self.info_panel.hide()

        UILabel(
            relative_rect=Rect((10, 10), (330, 30)),
            text="placeholder text",
            manager=manager,
            container=self.info_panel.panel,
        )

        self.launches_label = UILabel(
            relative_rect=Rect((10, 60), (330, 25)),
            text="placeholder text",
            manager=manager,
            container=self.info_panel.panel,
        )

        self.success_rate_label = UILabel(
            relative_rect=Rect((10, 90), (330, 25)),
            text="placeholder text",
            manager=manager,
            container=self.info_panel.panel,
        )

        self.payload_label = UILabel(
            relative_rect=Rect((10, 120), (330, 25)),
            text="placeholder text",
            manager=manager,
            container=self.info_panel.panel,
        )

        self.vab_level_label = UILabel(
            relative_rect=Rect((10, 150), (330, 25)),
            text="placeholder text",
            manager=manager,
            container=self.info_panel.panel,
        )

        button_width = 200
        self.buy_launchpad_button = UIButton(
            relative_rect=Rect(((panel_width - button_width) // 2, 200), (button_width, 50)),
            text="Buy New Launchpad",
            manager=manager,
            container=self.info_panel.panel,
        )

        self.upgrade_vab_button = UIButton(
            relative_rect=Rect(((panel_width - button_width) // 2, 270), (button_width, 50)),
            text="Upgrade VAB",
            manager=manager,
            container=self.info_panel.panel,
        )

    def _update_info_panel(self, stats: dict):
        try:
            self.launches_label.set_text(f"Launches: {stats.get('launches', 0)}")
            self.success_rate_label.set_text(
                f"Success Rate: {stats.get('success_rate', 0)}%"
            )
            self.payload_label.set_text(
                f"Total Payload: {stats.get('total_payload', 0)} kg"
            )
            self.vab_level_label.set_text(f"VAB Level: {stats.get('vab_level', 1)}")
        except (AttributeError, KeyError):
            # I don't know how you expect this to happen when you set defaults for everything, 
            # but alas, I have some form of mild OCD and must handle these properly.
            raise RuntimeError("Updating info panel failed due to inconsistencies between stat dictionary writing and parsing code. Please contact devs.")
