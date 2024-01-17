__all__ = ["main"]

import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
import numpy as np

from typing import Tuple, Any, Optional, List

# Constants and global variables
ABOUT = [
    "Authors:",
    "BOUAB Ahmed",
    "TERRAF Imad",
]
DIFFICULTY = ["EASY"]
FPS = 60
WINDOW_SIZE = (640, 580)

# Define constants for colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIME_GREEN = (50, 205, 50)

# Game board dimensions
ROW_AMOUNT = 6
COLUMN_AMOUNT = 7
CHIP_SIZE = 80
RADIUS = int(CHIP_SIZE / 2 - 5)
screen = pygame.display.set_mode(
    (COLUMN_AMOUNT * CHIP_SIZE, (ROW_AMOUNT + 1) * CHIP_SIZE)
)
gameboard = np.zeros((ROW_AMOUNT, COLUMN_AMOUNT), dtype=int)

# Sidebar dimensions
SIDEBAR_WIDTH = 200
TOTAL_WIDTH = COLUMN_AMOUNT * CHIP_SIZE
TOTAL_HEIGHT = (ROW_AMOUNT + 1) * CHIP_SIZE

# Board position offset
BOARD_OFFSET_X = SIDEBAR_WIDTH
BOARD_OFFSET_Y = 0


clock: Optional["pygame.time.Clock"] = None
main_menu: Optional["pygame_menu.Menu"] = None
surface: Optional["pygame.Surface"] = None


def play_easy():
    DIFFICULTY[0] = "EASY"
    play_function(DIFFICULTY, pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))


def play_medium():
    DIFFICULTY[0] = "MEDIUM"
    play_function(DIFFICULTY, pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))


def play_hard():
    DIFFICULTY[0] = "HARD"
    play_function(DIFFICULTY, pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))


def draw_board():
    screen.fill((255, 255, 255))

    # Draw the game board with offset
    for c in range(COLUMN_AMOUNT):
        for r in range(ROW_AMOUNT):
            # Adjusted coordinates with BOARD_OFFSET_X and BOARD_OFFSET_Y
            rect_x = c * CHIP_SIZE
            rect_y = r * CHIP_SIZE + CHIP_SIZE
            circle_x = int(rect_x + CHIP_SIZE / 2)
            circle_y = int(rect_y + CHIP_SIZE / 2)

            pygame.draw.rect(screen, BLUE, (rect_x, rect_y, CHIP_SIZE, CHIP_SIZE))
            pygame.draw.circle(screen, BLACK, (circle_x, circle_y), RADIUS)

    for c in range(COLUMN_AMOUNT):
        for r in range(ROW_AMOUNT):
            circle_x = int(c * CHIP_SIZE + CHIP_SIZE / 2 + BOARD_OFFSET_X)
            circle_y = int(
                (ROW_AMOUNT - r) * CHIP_SIZE + CHIP_SIZE / 2 + BOARD_OFFSET_Y
            )

            if gameboard[r][c] == 1:
                pygame.draw.circle(screen, RED, (circle_x, circle_y), RADIUS)
            elif gameboard[r][c] == 2:
                pygame.draw.circle(screen, LIME_GREEN, (circle_x, circle_y), RADIUS)

    # Update the display
    pygame.display.update()


def start_ai_vs_ai_game():
    draw_board()


def start_player_vs_ai_game(difficulty):
    draw_board()


def load_game(game_mode: str = "player_vs_ai", difficulty: str = None) -> None:
    """
    Load and start the game with the given mode or difficulty.

    :param game_mode: A string indicating the game mode.
    :param difficulty: A string indicating the difficulty of the game.
    """
    if game_mode == "AI_VS_AI":
        start_ai_vs_ai_game()
    else:
        start_player_vs_ai_game(difficulty)


def play_function(
    difficulty: List,
    game_mode: str = "player_vs_ai",
) -> None:
    """
    Main game function.

    :param difficulty: Difficulty of the game
    :param font: Pygame font
    :param game_mode: Game mode
    """
    assert isinstance(difficulty, list)
    difficulty = difficulty[0]
    assert isinstance(difficulty, str)

    # Define globals
    global main_menu
    global clock

    if game_mode == "player_vs_ai":
        load_game(difficulty)
    else:
        load_game(game_mode)
    main_menu.disable()
    main_menu.full_reset()

    frame = 0

    while True:
        # noinspection PyUnresolvedReferences
        clock.tick(60)
        frame += 1

        # Application events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    main_menu.enable()

                    # Quit this function, then skip to loop of main-menu on line 221
                    return

        # Pass events to main_menu
        if main_menu.is_enabled():
            main_menu.update(events)
        pygame.display.flip()


def play_ai_vs_ai():
    DIFFICULTY[0] = "AI_VS_AI"
    play_function(
        DIFFICULTY,
        game_mode="ai_vs_ai",
    )


def main_background() -> None:
    """
    Function used by menus, draw on background while menu is active.
    """
    global surface
    surface.fill((128, 0, 128))


def main(test: bool = False) -> None:
    """
    Main program.

    :param test: Indicate function is being tested
    """

    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global clock
    global main_menu
    global surface

    # -------------------------------------------------------------------------
    # Create window
    # -------------------------------------------------------------------------
    surface = create_example_window("Connect 4 game", WINDOW_SIZE)
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Create menus: Play Menu
    # -------------------------------------------------------------------------
    play_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7, title="Play Menu", width=WINDOW_SIZE[0] * 0.75
    )

    submenu_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    submenu_theme.widget_font_size = 15
    play_submenu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.5,
        theme=submenu_theme,
        title="Submenu",
        width=WINDOW_SIZE[0] * 0.7,
    )

    play_submenu.add.button("Easy", play_easy)
    play_submenu.add.button("Medium", play_medium)
    play_submenu.add.button("Hard", play_hard)
    play_submenu.add.button("Return to main menu", pygame_menu.events.RESET)

    play_menu.add.button(
        "Ai vs Ai",  # When pressing return -> play(DIFFICULTY[0], font)
        play_ai_vs_ai,
        # type="ai_vs_ai",
    )
    play_menu.add.button("Player vs Ai", play_submenu)
    play_menu.add.button("Return to main menu", pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus:About
    # -------------------------------------------------------------------------
    about_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    about_theme.widget_margin = (0, 0)

    about_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        theme=about_theme,
        title="About",
        width=WINDOW_SIZE[0] * 0.6,
    )

    for m in ABOUT:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=20)
    about_menu.add.vertical_margin(20)
    about_menu.add.button("Return to menu", pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus: Main
    # -------------------------------------------------------------------------
    main_theme = pygame_menu.themes.THEME_DEFAULT.copy()

    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        theme=main_theme,
        title="Main Menu",
        width=WINDOW_SIZE[0] * 0.6,
    )

    main_menu.add.button("Play", play_menu)
    main_menu.add.button("About", about_menu)
    main_menu.add.button("Quit", pygame_menu.events.EXIT)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:
        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Main menu
        if main_menu.is_enabled():
            main_menu.mainloop(
                surface, main_background, disable_loop=test, fps_limit=FPS
            )

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == "__main__":
    main()
