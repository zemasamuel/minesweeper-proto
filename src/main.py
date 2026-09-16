"""
Module: main.py
Description: Main game loop, rendering UI text, and input handling.
Inputs: Console setup inputs, Mouse click events
Outputs: Pygame display surface
Author: [Your Full Name(s)]
Date: September 2026
External Sources: 
- "How to make Minesweeper in Pygame" by Tech & Gaming (YouTube).
- Generative AI (Gemini) utilized to modify tutorial to strictly match EECS 581 constraints.
"""

import pygame
import sys
from settings import *
from sprites import Board

class Game:
    """Combined: Follows tutorial state machine, adapted for EECS 581 specific rules."""
    def __init__(self, num_mines):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        
        self.num_mines = num_mines
        self.flags_placed = 0
        
    def new(self):
        """Sourced: Starts a new game state."""
        self.board = Board()
        self.playing = True
        self.first_click = True
        self.game_over = False
        self.win = False

    def run(self):
        """Sourced: Tutorial's main loop structure."""
        while self.playing:
            self.events()
            self.draw()
            self.clock.tick(FPS)
            
        while self.game_over:
            self.end_screen()

    def events(self):
        """Combined: Input handling with custom coordinate translation and bounds."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                # Check that click is actually inside the play grid area
                if mx >= MARGIN_LEFT and my >= MARGIN_TOP:
                    x = (mx - MARGIN_LEFT) // TILESIZE
                    y = (my - MARGIN_TOP) // TILESIZE
                    
                    if 0 <= x < COLS and 0 <= y < ROWS:
                        tile = self.board.board_list[x][y]
                        
                        # Left Click (Reveal)
                        if event.button == 1 and not tile.flagged:
                            # Rubric: Populate mines only on first click for safety
                            if self.first_click:
                                self.board.place_mines(x, y, self.num_mines)
                                self.board.place_clues()
                                self.first_click = False
                                
                            safe = self.board.dig(x, y)
                            if not safe:
                                self.playing = False
                                self.game_over = True
                                self.reveal_all_mines()
                                
                            self.check_win()

                        # Right Click (Flag)
                        elif event.button == 3 and not tile.revealed:
                            if tile.flagged:
                                tile.flagged = False
                                self.flags_placed -= 1
                            else:
                                tile.flagged = True
                                self.flags_placed += 1

    def reveal_all_mines(self):
        """Sourced: Reveals all remaining mines upon loss condition."""
        for x in range(COLS):
            for y in range(ROWS):
                if self.board.board_list[x][y].type == 'X':
                    self.board.board_list[x][y].revealed = True

    def check_win(self):
        """Sourced: Win logic checks if only mines are left unrevealed."""
        unrevealed = 0
        for x in range(COLS):
            for y in range(ROWS):
                if not self.board.board_list[x][y].revealed and self.board.board_list[x][y].type != 'X':
                    unrevealed += 1
        
        if unrevealed == 0:
            self.playing = False
            self.game_over = True
            self.win = True

    def draw(self):
        """Combined: Draws screen and rubric-required A-J/1-10 headers."""
        self.screen.fill(BG_COLOR)
        
        status_msg = "Victory! (Click to Restart)" if self.win else ("Game Over (Click to Restart)" if self.game_over else "Playing")
        status = self.font.render(f"Status: {status_msg}", True, TEXT_COLOR)
        mines = self.font.render(f"Flags Left: {self.num_mines - self.flags_placed}", True, TEXT_COLOR)
        self.screen.blit(status, (20, 15))
        self.screen.blit(mines, (WIDTH - 150, 15))

        # Original: Column labels A-J (EECS Rubric)
        cols_text = "ABCDEFGHIJ"
        for i in range(COLS):
            lbl = self.font.render(cols_text[i], True, TEXT_COLOR)
            self.screen.blit(lbl, (MARGIN_LEFT + (i * TILESIZE) + 14, MARGIN_TOP - 25))

        # Original: Row labels 1-10 (EECS Rubric)
        for i in range(ROWS):
            lbl = self.font.render(str(i + 1), True, TEXT_COLOR)
            offset = 25 if i < 9 else 32
            self.screen.blit(lbl, (MARGIN_LEFT - offset, MARGIN_TOP + (i * TILESIZE) + 8))

        self.board.draw(self.screen, self.font)
        pygame.display.flip()

    def end_screen(self):
        """Sourced: Waits for any click to restart after win/loss."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game_over = False
                self.win = False
                self.flags_placed = 0
                self.new()
                self.run()
        
        self.draw()

if __name__ == "__main__":
    """Original: EECS Rubric terminal prompt requesting 10 to 20 mines."""
    print("--- EECS 581: Minesweeper ---")
    while True:
        try:
            val = input("Enter number of mines (10 to 20): ").strip()
            num = int(val)
            if 10 <= num <= 20:
                break
            print("Constraint Error: Mine count must be between 10 and 20.")
        except ValueError:
            print("Type Error: Please enter a valid integer.")

    g = Game(num)
    g.new()
    g.run()
