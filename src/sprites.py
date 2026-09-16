"""
Module: sprites.py
Description: Contains the Tile and Board classes, handling game logic and grid management.
Inputs: Grid coordinates, mine configurations
Outputs: Game state data and UI rendering primitives
Author: [Your Full Name(s)]
Date: September 2026
External Sources: 
- "How to make Minesweeper in Pygame" by Tech & Gaming (YouTube).
- Generative AI (Gemini) utilized to modify tutorial to strictly match EECS 581 constraints.
"""

import pygame
import random
from settings import *

class Tile:
    """Sourced: Standard tutorial Tile class to hold grid states."""
    def __init__(self, x, y, type_val):
        self.x = x
        self.y = y
        self.type = type_val  # '.' = empty, 'X' = mine, 'C' = clue
        self.revealed = False
        self.flagged = False
        self.clue_num = 0

class Board:
    def __init__(self):
        # Sourced: 2D list comprehension for the board from tutorial
        self.board_list = [[Tile(col, row, '.') for row in range(ROWS)] for col in range(COLS)]
        self.dug = []  # Tracks revealed tiles for recursion

    def place_mines(self, safe_x, safe_y, num_mines):
        """
        Combined: Modified from tutorial to guarantee a safe first click 
        and safe adjacent neighbors based on rubric.
        """
        safe_zone = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                safe_zone.append((safe_x + dx, safe_y + dy))

        available = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in safe_zone]
        mine_spots = random.sample(available, num_mines)
        
        for x, y in mine_spots:
            self.board_list[x][y].type = 'X'

    def place_clues(self):
        """Sourced: Tutorial algorithm for calculating neighbor numbers."""
        for x in range(COLS):
            for y in range(ROWS):
                if self.board_list[x][y].type != 'X':
                    total_mines = self.check_neighbors(x, y)
                    if total_mines > 0:
                        self.board_list[x][y].type = 'C'
                        self.board_list[x][y].clue_num = total_mines

    def check_neighbors(self, x, y):
        """Sourced: Tutorial's 8-way neighbor coordinate check."""
        total = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS:
                    if self.board_list[nx][ny].type == 'X':
                        total += 1
        return total

    def dig(self, x, y):
        """
        Sourced: Tutorial's recursive flood-fill algorithm.
        Returns False if a mine is hit, True otherwise.
        """
        self.dug.append((x, y))
        tile = self.board_list[x][y]

        if tile.type == 'X':
            tile.revealed = True
            return False  # Loss condition triggered
        elif tile.type == 'C':
            tile.revealed = True
            return True   # Hit a clue, halt recursion this direction

        tile.revealed = True

        for row in range(max(0, x - 1), min(COLS - 1, x + 1) + 1):
            for col in range(max(0, y - 1), min(ROWS - 1, y + 1) + 1):
                if (row, col) not in self.dug:
                    self.dig(row, col)
        return True

    def draw(self, surface, font):
        """
        Original: Replaced tutorial's image blitting with native Pygame shapes.
        Ensures the game runs without needing an external assets folder.
        """
        for x in range(COLS):
            for y in range(ROWS):
                tile = self.board_list[x][y]
                pos_x = MARGIN_LEFT + (x * TILESIZE)
                pos_y = MARGIN_TOP + (y * TILESIZE)
                rect = pygame.Rect(pos_x, pos_y, TILESIZE, TILESIZE)

                if tile.revealed:
                    pygame.draw.rect(surface, TILE_REVEALED, rect)
                    if tile.type == 'X':
                        pygame.draw.circle(surface, MINE_COLOR, (pos_x + TILESIZE//2, pos_y + TILESIZE//2), 10)
                    elif tile.type == 'C':
                        color = NUM_COLORS.get(tile.clue_num, TEXT_COLOR)
                        text = font.render(str(tile.clue_num), True, color)
                        surface.blit(text, (pos_x + 13, pos_y + 8))
                else:
                    pygame.draw.rect(surface, TILE_UNREVEALED, rect)
                    if tile.flagged:
                        # Draws a red flag
                        pygame.draw.polygon(surface, FLAG_COLOR, [(pos_x+10, pos_y+10), (pos_x+25, pos_y+15), (pos_x+10, pos_y+20)])
                        pygame.draw.line(surface, TEXT_COLOR, (pos_x+10, pos_y+10), (pos_x+10, pos_y+30), 2)

                pygame.draw.rect(surface, GRID_COLOR, rect, 1)
