"""
Module: settings.py
Description: Configuration constants for the Minesweeper game.
Inputs: None
Outputs: Constant values used across modules
Author: [Your Full Name(s)]
Date: September 2026
External Sources: 
- "How to make Minesweeper in Pygame" by Tech & Gaming (YouTube).
"""

# Original/Combined: Adjusted game grid settings for 10x10 requirement
TILESIZE = 40
ROWS = 10
COLS = 10

# Original: UI Offsets for the A-J and 1-10 labels (Rubric requirement)
MARGIN_TOP = 80
MARGIN_LEFT = 40

# Sourced: Screen dimensions logic from tutorial
WIDTH = (TILESIZE * COLS) + MARGIN_LEFT + 30
HEIGHT = (TILESIZE * ROWS) + MARGIN_TOP + 30
FPS = 60
TITLE = "EECS 581 - Minesweeper"

# Original: Colors for standalone rendering (replacing tutorial image assets)
BG_COLOR = (230, 230, 230)
TILE_UNREVEALED = (180, 180, 180)
TILE_REVEALED = (215, 215, 215)
GRID_COLOR = (100, 100, 100)
TEXT_COLOR = (20, 20, 20)
FLAG_COLOR = (220, 50, 50)
MINE_COLOR = (30, 30, 30)

NUM_COLORS = {
    1: (0, 0, 255), 2: (0, 128, 0), 3: (255, 0, 0),
    4: (0, 0, 128), 5: (128, 0, 0), 6: (0, 128, 128),
    7: (0, 0, 0), 8: (128, 128, 128)
}
