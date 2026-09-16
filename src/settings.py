"""
Module: settings.py
Description: Game settings, dimensions, and color constants.
Inputs: None
Outputs: Constants imported by main.py and sprites.py
Author: [Your Full Name]
Date: September 2026
External Sources:
- Base configuration layout adapted from Tech & Gaming Pygame tutorial
- Custom dimensions and vector color palette written for EECS 581
"""

# Board dimensions (10x10 for project requirements)
TILESIZE = 40
ROWS = 10
COLS = 10

# Margins to leave room for HUD and row/col labels
MARGIN_TOP = 80
MARGIN_LEFT = 40

# Window size and game title
WIDTH = (TILESIZE * COLS) + MARGIN_LEFT + 30
HEIGHT = (TILESIZE * ROWS) + MARGIN_TOP + 30
FPS = 60
TITLE = "EECS 581 - Minesweeper"

# UI and cell colors (RGB)
BG_COLOR = (230, 230, 230)
TILE_UNREVEALED = (180, 180, 180)
TILE_REVEALED = (215, 215, 215)
GRID_COLOR = (100, 100, 100)
TEXT_COLOR = (20, 20, 20)
FLAG_COLOR = (220, 50, 50)
MINE_COLOR = (30, 30, 30)

# Standard Minesweeper number colors (1 through 8)
NUM_COLORS = {
    1: (0, 0, 255),       # Blue
    2: (0, 128, 0),       # Green
    3: (255, 0, 0),       # Red
    4: (0, 0, 128),       # Dark Blue
    5: (128, 0, 0),       # Dark Red
    6: (0, 128, 128),     # Cyan / Teal
    7: (0, 0, 0),         # Black
    8: (128, 128, 128)    # Gray
}
