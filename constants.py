import pygame

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game board dimensions
ROW_COUNT = 6
COLUMN_COUNT = 7

# Player identifiers
PLAYER = 0
AI = 1

# Cell states
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

# Window parameters
WINDOW_LENGTH = 4
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
ABOUT = [
    "Authors:",
    "BOUAB Ahmed",
    "TERRAF Imad",
]


# Initialize screen
width, height = COLUMN_COUNT * SQUARESIZE, (ROW_COUNT + 1) * SQUARESIZE
screen = pygame.display.set_mode((width, height))
