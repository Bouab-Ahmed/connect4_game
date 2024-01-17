import numpy as np
import pygame
import sys
import random
import math
import time
import pygame_menu
from game_logic import *
from constants import *
from minimax import minimax, ai_move
from game_board import draw_board

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect 4")
myfont = pygame.font.SysFont("monospace", 75)

# Global variables to store game mode and difficulty
game_mode = "player_vs_ai"  # Default game mode
difficulty = "Easy"  # Default difficulty


def set_game_mode(value, mode):
    global game_mode
    game_mode = mode


def set_difficulty(value, diff):
    global difficulty
    difficulty = diff


def start_game():
    # Start the game based on selected game mode and difficulty
    if game_mode == "ai_vs_ai":
        ai_vs_ai_game_loop(difficulty)
        pass
    elif game_mode == "player_vs_ai":
        print(difficulty)
        game_loop(difficulty)


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def ai_vs_ai_game_loop(difficulty):
    board = create_board()
    game_over = False
    turn = random.randint(PLAYER, AI)

    while not game_over:
        if turn == PLAYER:
            _, row = ai_move(board, PLAYER_PIECE, difficulty)

        else:
            _, row = ai_move(board, AI_PIECE, difficulty)

        if winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE):
            game_over = True

        turn += 1
        turn = turn % 2

        draw_board(board)  # Assuming screen is a global or passed variable

        if game_over:
            pygame.time.wait(3000)
            break


def game_loop(difficulty):
    board = create_board()

    print_board(board)
    game_over = False

    pygame.init()

    SQUARESIZE = 100

    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE

    size = (width, height)

    RADIUS = int(SQUARESIZE / 2 - 5)

    screen = pygame.display.set_mode(size)
    # here include a menu to choose between AI vs AI or player vs AI
    # if player vs AI, include a menu to choose the difficulty
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    turn = random.randint(PLAYER, AI)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        print_board(board)
                        draw_board(board)

        # # Ask for Player 2 Input
        if turn == AI and not game_over:
            time.sleep(0.5)
            # col = random.randint(0, COLUMN_COUNT-1)
            # col = pick_best_move(board, AI_PIECE)
            if difficulty == "Easy":
                col = random.randint(0, COLUMN_COUNT - 1)
            elif difficulty == "Medium":
                col, minimax_score = minimax(board, 3, -math.inf, math.inf, True)
            else:
                col, minimax_score = minimax(board, 1, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = myfont.render("Player 2 wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)


def main_menu():
    menu = pygame_menu.Menu("Welcome", 400, 300, theme=pygame_menu.themes.THEME_DARK)

    menu.add.selector(
        "Mode :",
        [("Player vs AI", "player_vs_ai"), ("AI vs AI", "ai_vs_ai")],
        onchange=set_game_mode,
    )
    menu.add.selector(
        "Difficulty :",
        [("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")],
        onchange=set_difficulty,
    )
    about_theme = pygame_menu.themes.THEME_DARK.copy()
    about_theme.widget_margin = (0, 0)

    about_menu = pygame_menu.Menu(
        height=height * 0.6,
        theme=about_theme,
        title="About",
        width=width * 0.6,
    )

    for m in ABOUT:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=20)
    about_menu.add.vertical_margin(20)
    about_menu.add.button("Return to menu", pygame_menu.events.BACK)
    menu.add.button("Play", start_game)
    menu.add.button("About", about_menu)
    menu.add.button("Quit", pygame_menu.events.EXIT)

    menu.mainloop(screen)


# Main Function
def main():
    main_menu()


# Entry Point
if __name__ == "__main__":
    main()
