from pygame import Rect

SCREEN_W = 1920
SCREEN_H = 1080

# Tree layout constants
TREE_NODE_WIDTH = 140
TREE_NODE_HEIGHT = 40
TREE_ORIGINS = [
    (100, 50),       # Tree 1 origin (top)
    (100, 400),      # Tree 2 origin (middle)
    (100, 750),      # Tree 3 origin (bottom)
]
TREE_LABELS = ["TREE 1", "TREE 2", "TREE 3"]

def scale_to_offset(scale_size, width_height):
    if width_height == "width":
        return scale_size * SCREEN_W
    elif width_height == "height":
        return scale_size * SCREEN_H
    else:
        raise ValueError('Incorrect Parameter. Use "width" or "height".') # Why were you raising a bloody base Exception?


def centered_rect(center_x_scale, center_y_scale, width_scale, height_scale):
    width = scale_to_offset(width_scale, "width")
    height = scale_to_offset(height_scale, "height")
    center_x = scale_to_offset(center_x_scale, "width")
    center_y = scale_to_offset(center_y_scale, "height")

    top_left_x = center_x - width / 2
    top_left_y = center_y - height / 2

    return Rect((top_left_x, top_left_y), (width, height))