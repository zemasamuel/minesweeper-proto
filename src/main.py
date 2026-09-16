"""
Module: main.py
Description: Application entry point, Pygame main loop, UI status bar, 
             and coordinate grid labeling (A-J, 1-10).
Inputs: Console mine count (10-20), Mouse clicks
Outputs: Active Pygame display window
Author: [Your Full Name(s)]
Date: September 2026
External Sources: 
- "How to make Minesweeper in Pygame" by Tech & Gaming (YouTube).
- Restructured game loop to iterative while-loop to eliminate call stack recursion.
- Adaptations for EECS 581 requirements.
"""

import sys
import pygame
from settings import *
from sprites import Board

class Game:
    """Manages display presentation, game state, and input routing."""
    def __init__(self, num_mines):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        
        self.num_mines = num_mines
        self.flags_placed = 0
        self.board = None
        self.playing = False
        self.first_click = True
        self.game_over = False
        self.win = False

    def run(self):
        """
        Master iterative game loop. 
        Replaced tutorial's recursive run() pattern to prevent call stack memory leaks.
        """
        while True:
            # Initialize / Reset game session state
            self.board = Board()
            self.playing = True
            self.first_click = True
            self.game_over = False
            self.win = False
            self.flags_placed = 0

            # Active gameplay loop
            while self.playing:
                self.events()
                self.draw()
                self.clock.tick(FPS)
                
            # Post-game screen loop (loss or win)
            while self.game_over:
                self.end_screen()
                self.clock.tick(FPS)

    def events(self):
        """Handles mouse interactions and bound constraints."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                # Verify click is strictly inside the grid
                if mx >= MARGIN_LEFT and my >= MARGIN_TOP:
                    x = (mx - MARGIN_LEFT) // TILESIZE
                    y = (my - MARGIN_TOP) // TILESIZE
                    
                    if 0 <= x < COLS and 0 <= y < ROWS:
                        tile = self.board.board_list[x][y]
                        
                        # Left Click -> Uncover Cell
                        if event.button == 1 and not tile.flagged:
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

                        # Right Click -> Toggle Flag
                        elif event.button == 3 and not tile.revealed:
                            if tile.flagged:
                                tile.flagged = False
                                self.flags_placed -= 1
                            else:
                                tile.flagged = True
                                self.flags_placed += 1

    def reveal_all_mines(self):
        """Reveals all mine placements upon loss."""
        for x in range(COLS):
            for y in range(ROWS):
                if self.board.board_list[x][y].type == 'X':
                    self.board.board_list[x][y].revealed = True

    def check_win(self):
        """Checks if all safe, non-mine cells have been uncovered."""
        unrevealed_safe = 0
        for x in range(COLS):
            for y in range(ROWS):
                if not self.board.board_list[x][y].revealed and self.board.board_list[x][y].type != 'X':
                    unrevealed_safe += 1
        
        if unrevealed_safe == 0:
            self.playing = False
            self.game_over = True
            self.win = True

    def draw(self):
        """Draws header status, coordinate labels (A-J, 1-10), and the board."""
        self.screen.fill(BG_COLOR)
        
        # Status indicators
        status_msg = "Victory! (Click to Restart)" if self.win else ("Game Over (Click to Restart)" if self.game_over else "Playing")
        status = self.font.render(f"Status: {status_msg}", True, TEXT_COLOR)
        mines = self.font.render(f"Flags Left: {self.num_mines - self.flags_placed}", True, TEXT_COLOR)
        self.screen.blit(status, (20, 15))
        self.screen.blit(mines, (WIDTH - 150, 15))

        # Column labels: A-J
        cols_text = "ABCDEFGHIJ"
        for i in range(COLS):
            lbl = self.font.render(cols_text[i], True, TEXT_COLOR)
            self.screen.blit(lbl, (MARGIN_LEFT + (i * TILESIZE) + 14, MARGIN_TOP - 25))

        # Row labels: 1-10
        for i in range(ROWS):
            lbl = self.font.render(str(i + 1), True, TEXT_COLOR)
            offset = 25 if i < 9 else 32  # Alignment adjustment for '10'
            self.screen.blit(lbl, (MARGIN_LEFT - offset, MARGIN_TOP + (i * TILESIZE) + 8))

        self.board.draw(self.screen, self.font)
        pygame.display.flip()

    def end_screen(self):
        """
        Post-game freeze loop. 
        Breaks out naturally by flipping self.game_over to False, returning to run().
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game_over = False  # Exits while self.game_over loop naturally

        self.draw()

if __name__ == "__main__":
    print("=== EECS 581: Minesweeper System Development ===")
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
    g.run()
