import math
import random
from game_logic import (
    drop_piece,
    get_valid_locations,
    get_next_open_row,
    is_terminal_node,
    winning_move,
    score_position,
)
from constants import AI_PIECE, PLAYER_PIECE, COLUMN_COUNT


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def ai_move(board, piece, difficulty):
    if difficulty == "Easy":
        col = random.randint(0, COLUMN_COUNT - 1)
    elif difficulty == "Medium":
        col, _ = minimax(board, 3, -math.inf, math.inf, True)
    else:  # Hard
        col, _ = minimax(board, 5, -math.inf, math.inf, True)

    row = get_next_open_row(board, col)
    drop_piece(board, row, col, piece)
    return col, row
