"""
Module: main.py
Description: Main driver for the minesweeper project. Handles the pygame window,
             input loops, game states, and board labels.
Inputs: Console mine input (10-20), mouse events
Outputs: Interactive Pygame window
Author: [Your Full Name]
Date: September 2026
External Sources:
- Tech & Gaming YouTube tutorial (basic game setup and layout)
- Adapted to meet EECS 581 requirements (labels, safe clicks, input constraints)
"""

import sys
import pygame
from settings import *
from sprites import Board


class Game:
    def __init__(self, num_mines):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        
        # User defined settings
        self.num_mines = num_mines
        self.flags_placed = 0
        
        # Game state flags
        self.board = None
        self.playing = False
        self.first_click = True
        self.game_over = False
        self.win = False

    def run(self):
        # Outer loop so restart resets the game without recursing
        while True:
            self.board = Board()
            self.playing = True
            self.first_click = True
            self.game_over = False
            self.win = False
            self.flags_placed = 0

            # Main game loop
            while self.playing:
                self.events()
                self.draw()
                self.clock.tick(FPS)
                
            # Wait loop when player wins or hits a mine
            while self.game_over:
                self.end_screen()
                self.clock.tick(FPS)

    def events(self):
        for event in pygame.event.get():
            # Handle window close
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                # Make sure the user actually clicked on the board
                if mx >= MARGIN_LEFT and my >= MARGIN_TOP:
                    # Convert pixel coordinates to grid row/col
                    x = (mx - MARGIN_LEFT) // TILESIZE
                    y = (my - MARGIN_TOP) // TILESIZE
                    
                    # Bounds check
                    if 0 <= x < COLS and 0 <= y < ROWS:
                        tile = self.board.board_list[x][y]
                        
                        # Left click: reveal tile
                        if event.button == 1 and not tile.flagged:
                            # Generate mines only after the first click (safe click requirement)
                            if self.first_click:
                                self.board.place_mines(x, y, self.num_mines)
                                self.board.place_clues()
                                self.first_click = False
                                
                            safe = self.board.dig(x, y)
                            if not safe:
                                # Hit a bomb
                                self.playing = False
                                self.game_over = True
                                self.reveal_all_mines()
                                
                            self.check_win()

                        # Right click: toggle flag
                        elif event.button == 3 and not tile.revealed:
                            if tile.flagged:
                                tile.flagged = False
                                self.flags_placed -= 1
                            else:
                                tile.flagged = True
                                self.flags_placed += 1

    def reveal_all_mines(self):
        # Show where all mines were once the player loses
        for x in range(COLS):
            for y in range(ROWS):
                if self.board.board_list[x][y].type == 'X':
                    self.board.board_list[x][y].revealed = True

    def check_win(self):
        # Count remaining non-mine tiles
        unrevealed_safe = 0
        for x in range(COLS):
            for y in range(ROWS):
                if not self.board.board_list[x][y].revealed and self.board.board_list[x][y].type != 'X':
                    unrevealed_safe += 1
        
        # If all safe cells are revealed, you win
        if unrevealed_safe == 0:
            self.playing = False
            self.game_over = True
            self.win = True

    def draw(self):
        self.screen.fill(BG_COLOR)
        
        # Setup HUD text
        if self.win:
            status_msg = "Victory! (Click to Restart)"
        elif self.game_over:
            status_msg = "Game Over (Click to Restart)"
        else:
            status_msg = "Playing"
            
        status = self.font.render(f"Status: {status_msg}", True, TEXT_COLOR)
        mines = self.font.render(f"Flags Left: {self.num_mines - self.flags_placed}", True, TEXT_COLOR)
        self.screen.blit(status, (20, 15))
        self.screen.blit(mines, (WIDTH - 150, 15))

        # Render column headers A through J
        cols_text = "ABCDEFGHIJ"
        for i in range(COLS):
            lbl = self.font.render(cols_text[i], True, TEXT_COLOR)
            self.screen.blit(lbl, (MARGIN_LEFT + (i * TILESIZE) + 14, MARGIN_TOP - 25))

        # Render row numbers 1 through 10
        for i in range(ROWS):
            lbl = self.font.render(str(i + 1), True, TEXT_COLOR)
            offset = 25 if i < 9 else 32  # Extra padding for "10"
            self.screen.blit(lbl, (MARGIN_LEFT - offset, MARGIN_TOP + (i * TILESIZE) + 8))

        # Draw actual tiles
        self.board.draw(self.screen, self.font)
        pygame.display.flip()

    def end_screen(self):
        # Freeze frame; reset game state on click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game_over = False  # Break out to start a new round

        self.draw()


if __name__ == "__main__":
    print("=== EECS 581: Minesweeper ===")
    
    # Prompt user for mine count between 10 and 20
    while True:
        try:
            val = input("Enter number of mines (10 to 20): ").strip()
            num = int(val)
            if 10 <= num <= 20:
                break
            print("Please enter a number between 10 and 20.")
        except ValueError:
            print("Invalid input, must be an integer.")

    game = Game(num)
    game.run()
