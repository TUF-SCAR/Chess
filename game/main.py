import pygame
from sys import exit

TILE = 75
BOARD_PX = TILE * 8
BOARD_X = (1280 - BOARD_PX) // 2
BOARD_Y = (720 - BOARD_PX) // 2
LIGHT = (180, 175, 165)
DARK = (145, 140, 125)


def make_board_data():
    board_data = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
    ]
    return board_data


def move_piece(board, from_rc, to_rc):
    r1, c1 = from_rc
    r2, c2 = to_rc

    moving_piece = board[r1][c1]
    if moving_piece is None:
        return False

    target = board[r2][c2]
    if target is not None and target[0] == moving_piece[0]:
        return False

    board[r2][c2] = moving_piece
    board[r1][c1] = None
    return True


pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
running = True
board_data = make_board_data()
selected = None
turn = "w"
top = BOARD_Y
bottom = BOARD_Y + BOARD_PX
left = BOARD_X
right = BOARD_X + BOARD_PX

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                selected = None

            if event.button == 1:
                mx, my = event.pos

                if (mx < left or mx >= right) or (my < top or my >= bottom):
                    continue

                col = (mx - BOARD_X) // TILE
                row = (my - BOARD_Y) // TILE

                if selected is None:
                    piece = board_data[row][col]
                    if piece is not None and piece[0] == turn:
                        selected = (row, col)
                else:
                    if selected == (row, col):
                        selected = None
                    else:
                        ok = move_piece(board_data, selected, (row, col))
                        if ok:
                            turn = "b" if turn == "w" else "w"
                        selected = None
    screen.fill((6, 10, 50))

    for row in range(8):
        for col in range(8):
            x = BOARD_X + col * TILE
            y = BOARD_Y + row * TILE
            cell = pygame.Rect(x, y, TILE, TILE)
            if (row + col) % 2 == 0:
                pygame.draw.rect(screen, LIGHT, cell)
            else:
                pygame.draw.rect(screen, DARK, cell)

            piece = board_data[row][col]
            piece_x = x + TILE // 2
            piece_y = y + TILE // 2
            piece_r = TILE // 3
            if piece is not None:
                if piece[0] == "w":
                    pygame.draw.circle(
                        screen, (235, 235, 235), (piece_x, piece_y), piece_r
                    )
                else:
                    pygame.draw.circle(
                        screen, (25, 25, 25), (piece_x, piece_y), piece_r
                    )
            if selected == (row, col):
                pygame.draw.rect(screen, (100, 149, 237), cell, width=4)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
exit()
