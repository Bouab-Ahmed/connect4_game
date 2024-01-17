import pygame
from constants import (
    ROW_COUNT,
    COLUMN_COUNT,
    SQUARESIZE,
    RADIUS,
    PLAYER_PIECE,
    AI_PIECE,
    screen,
    height,
)

# Define colors to match the menu theme
BOARD_COLOR = (15, 17, 26)  # Dark blue-gray, resembling a digital interface
SLOT_COLOR = (0, 255, 255)  # Bright cyan for neon effect
PLAYER_COLOR = (255, 0, 0)  # Bright red for player pieces
AI_COLOR = (255, 255, 0)  # Bright yellow for AI pieces


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen,
                BOARD_COLOR,  # Use the board color from the menu theme
                (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE),
            )
            pygame.draw.circle(
                screen,
                SLOT_COLOR,  # Use the slot color from the menu theme
                (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2),
                ),
                RADIUS,
            )

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(
                    screen,
                    PLAYER_COLOR,  # Use the player piece color
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        height - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(
                    screen,
                    AI_COLOR,  # Use the AI piece color
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        height - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )
    pygame.display.update()
