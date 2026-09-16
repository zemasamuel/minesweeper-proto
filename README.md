# EECS 581 — Minesweeper Project

A classic single-player Minesweeper implementation built in Python using Pygame for **EECS 581: Software Engineering II** at the University of Kansas.

---

## Features

* **10x10 Grid:** Columns labeled **A–J** and rows numbered **1–10**.
* **Configurable Difficulty:** Terminal prompt allows entering **10 to 20** mines.
* **Guaranteed Safe First Click:** First clicked cell and its 8 adjacent neighbors are guaranteed safe; mines are placed dynamically after click 1.
* **Recursive Flood Fill:** Zero-clue empty cells automatically uncover adjacent clear tiles and boundary clues.
* **Flagging System:** Right-click marks suspected mine locations with red flags; flagged cells cannot be clicked.
* **Live HUD:** Tracks game state (`Playing`, `Victory!`, `Game Over`) and remaining flags (`Total Mines - Placed Flags`).
* **Instant Reset:** Non-blocking game loop restarts cleanly on click without stack overflow or memory leaks.
* **Standalone Vector Graphics:** Native Pygame drawing primitives—no external asset files or directories required.

---

## Requirements

* **Operating System:** Windows, macOS, or Linux
* **Python Version:** Python 3.10+
* **Dependencies:** Pygame

---

## Step-by-Step Instructions to Run

Run the following commands directly in Git Bash (Windows) or terminal (macOS/Linux):

1. Open Git Bash and navigate into the repository:
   cd ~/minesweeper-proto

2. Make sure you are on the main branch and up to date:
   git checkout main
   git pull origin main

3. Create a clean virtual environment:
   python -m venv venv

4. Activate the virtual environment:
   # For Windows (Git Bash):
   source venv/Scripts/activate

   # For macOS / Linux:
   source venv/bin/activate

   (Your terminal prompt will display (venv) once activated.)

5. Upgrade pip and install Pygame:
   python -m pip install --upgrade pip
   pip install pygame

6. Launch the game:
   python src/main.py

7. Select Mine Count:
   When prompted in your terminal, type an integer between 10 and 20 and press Enter:
   === EECS 581: Minesweeper ===
   Enter number of mines (10 to 20): 12

---

## Game Controls

* **Left Click:** Reveal a cell.
* **Right Click:** Place or remove a flag.
* **Click After Game Over:** Restarts the board immediately for a new match.
