# chessplusplus_pygame_catapult_click_fix.py
# Pygame frontend for Chess++ (drag & drop for normal pieces, click->click for Catapult)
# Robust handling for different returnValidMoves signatures in your backend.
#
# Put your piece images in ./piece_images with names like:
#   white_pawn.png  black_queen.png  white_rook.png  etc.
#
# Drops and moves are executed against your ChessPlusPlusBoard.playMove(move, updateValue=True, storeMove=True)
# The frontend will try multiple calling conventions for returnValidMoves to match different backend versions.

import pygame
import sys
import os
from ChessPlusPlusBoard import ChessPlusPlusBoard

# -- Config --
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQ_SIZE = WIDTH // COLS
FPS = 60
PIECE_DIR = "images"

# Colors
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
HIGHLIGHT_RGBA = (0, 200, 0, 160)
WHITE_CIRCLE = (245, 245, 245)
BLACK_CIRCLE = (30, 30, 30)
TEXT_COLOR = (10, 10, 10)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess++ — Drag & Drop + Catapult Click")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 20)

# Load piece images (white_pawn.png, black_queen.png, ...)
piece_images = {}
if os.path.isdir(PIECE_DIR):
    for fn in os.listdir(PIECE_DIR):
        if fn.lower().endswith(".png"):
            key = fn[:-4]  # strip .png
            try:
                img = pygame.image.load(os.path.join(PIECE_DIR, fn)).convert_alpha()
                img = pygame.transform.smoothscale(img, (SQ_SIZE, SQ_SIZE))
                piece_images[key] = img
            except Exception as e:
                print("Failed to load", fn, ":", e)
else:
    print(f"Warning: '{PIECE_DIR}' not found. Using text fallback for pieces.")

# ----------------- Helpers -----------------
def draw_board():
    for r in range(ROWS):
        for c in range(COLS):
            color = LIGHT if (r + c) % 2 == 0 else DARK
            pygame.draw.rect(WIN, color, (c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_catapults(board):
    """Draw catapults (underBoard): white/black circles"""
    for r in range(ROWS):
        for c in range(COLS):
            under_piece = board.underBoard[r][c]
            if under_piece != 0:
                center = (c*SQ_SIZE + SQ_SIZE//2, r*SQ_SIZE + SQ_SIZE//2)
                radius = SQ_SIZE // 3
                if under_piece.color == 'White':
                    pygame.draw.circle(WIN, WHITE_CIRCLE, center, radius)
                    pygame.draw.circle(WIN, (120,120,120), center, radius, 2)
                else:
                    pygame.draw.circle(WIN, BLACK_CIRCLE, center, radius)
                    pygame.draw.circle(WIN, (200,200,200), center, radius, 2)

def draw_pieces(board, dragging_piece):
    """Draw board pieces. If dragging_piece is set, skip drawing it at its origin."""
    for r in range(ROWS):
        for c in range(COLS):
            piece = board.board[r][c]
            if piece == 0:
                continue
            if dragging_piece is not None and piece is dragging_piece:
                continue
            key = piece.color.lower() + "_" + piece.name.lower()
            img = piece_images.get(key)
            if img:
                WIN.blit(img, (c*SQ_SIZE, r*SQ_SIZE))
            else:
                rect = pygame.Rect(c*SQ_SIZE + 6, r*SQ_SIZE + 6, SQ_SIZE-12, SQ_SIZE-12)
                pygame.draw.rect(WIN, (220,220,220), rect)
                label = FONT.render(piece.name[0].upper() if piece.color=='White' else piece.name[0].lower(), True, TEXT_COLOR)
                WIN.blit(label, (c*SQ_SIZE + SQ_SIZE//3, r*SQ_SIZE + SQ_SIZE//4))

def highlight_squares(squares):
    """Draw translucent circle highlights on provided squares (list of (row,col))."""
    if not squares:
        return
    surf = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(surf, HIGHLIGHT_RGBA, (SQ_SIZE//2, SQ_SIZE//2), 12)
    for (r, c) in squares:
        if 0 <= r < ROWS and 0 <= c < COLS:
            WIN.blit(surf, (c*SQ_SIZE, r*SQ_SIZE))

def coord_from_mouse(pos):
    x, y = pos
    col = x // SQ_SIZE
    row = y // SQ_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        return (row, col)
    return None

# Safe wrapper to call returnValidMoves with several possible signatures
def safe_return_valid_moves(piece, board, checkRestricted=True):
    """
    Try calling piece.returnValidMoves with multiple possible signatures:
      - piece.returnValidMoves(board)
      - piece.returnValidMoves(checkRestricted)
      - piece.returnValidMoves()
    Returns a list (or [] on error).
    """
    # Try board param first (some older/alternate backends)
    try:
        return piece.returnValidMoves(board)
    except TypeError:
        pass
    except Exception:
        pass

    # Try boolean checkRestricted
    try:
        return piece.returnValidMoves(checkRestricted)
    except TypeError:
        pass
    except Exception:
        pass

    # Try no-arg
    try:
        return piece.returnValidMoves()
    except Exception:
        pass

    # Give up
    return []

def _extract_special_move_str(move):
    """Return the specialMove string if present (handles dict vs string)."""
    sm = None
    if move is None:
        return None
    # handle dict-like move
    if isinstance(move, dict):
        sm = move.get('specialMove')
        # if it's a dict nested, extract nested string
        if isinstance(sm, dict):
            sm = sm.get('specialMove', sm.get('special_move', None))
    else:
        # possibly a Move object with attribute specialMove
        sm = getattr(move, 'specialMove', None)
        if isinstance(sm, dict):
            sm = sm.get('specialMove', sm.get('special_move', None))
    if isinstance(sm, str):
        return sm
    return None

def _get_moved_by(move):
    if isinstance(move, dict):
        return move.get('movedBy')
    return getattr(move, 'movedBy', None)

def _special_move_destination(move):
    """
    Compute destination for special moves (En_Passant, Pawn_Promotion, Castling).
    Returns (row, col) or None.
    """
    sm = _extract_special_move_str(move)
    moved_by = _get_moved_by(move)
    if not sm:
        return None

    # split tokens robustly
    parts = sm.split('_')

    # En Passant -> format often includes last token as destination column
    if 'En_Passant' in sm:
        # last token should be end column
        try:
            endcol = int(parts[-1])
        except Exception:
            return None
        # white ends on row 2 (index 2) in this engine's convention, black on row 5
        return (2, endcol) if moved_by == 'White' else (5, endcol)

    # Pawn promotion -> last token usually end column
    if 'Pawn_Promotion' in sm:
        try:
            endcol = int(parts[-1])
        except Exception:
            return None
        return (0, endcol) if moved_by == 'White' else (7, endcol)

    # Castling
    if 'Castling' in sm:
        if 'W_Castling_KS' in sm:
            return (7, 6)
        if 'W_Castling_QS' in sm:
            return (7, 2)
        if 'B_Castling_KS' in sm:
            return (0, 6)
        if 'B_Castling_QS' in sm:
            return (0, 2)

    return None

def get_move_destination(move):
    """
    Return a destination (row, col) for a move.
    Handles dict moves and Move-class-like objects, catapultMove tuples, special moves.
    """
    if move is None:
        return None

    # If object has attribute endCoordinate (Move class)
    if not isinstance(move, dict) and hasattr(move, 'endCoordinate'):
        if getattr(move, 'endCoordinate') is not None:
            return getattr(move, 'endCoordinate')

    # dict style
    if isinstance(move, dict):
        if move.get('endCoordinate') is not None:
            return move['endCoordinate']
        if move.get('catapultMove') is not None:
            try:
                return move['catapultMove'][1]
            except Exception:
                pass

        # fallthrough to special move parsing
        dest = _special_move_destination(move)
        return dest

    # object style fallback
    # catapultMove attribute?
    catm = getattr(move, 'catapultMove', None)
    if catm:
        try:
            return catm[1]
        except Exception:
            pass
    # specialMove attribute
    sm_dest = _special_move_destination(move)
    if sm_dest:
        return sm_dest

    return None

# ----------------- Main -----------------
def main():
    board = ChessPlusPlusBoard()
    turn = 'White'
    dragging = False
    drag_piece = None
    drag_img = None
    valid_moves = []
    valid_squares = []
    selected_catapult = None
    catapult_moves = []

    running = True
    while running:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse down: select piece or catapult
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                coord = coord_from_mouse(pygame.mouse.get_pos())
                if coord is None:
                    continue
                r, c = coord
                piece = board.board[r][c]
                under_piece = board.underBoard[r][c]

                # If a catapult is already selected: second click -> try to execute a catapult move
                if selected_catapult:
                    executed = False
                    for mv in catapult_moves:
                        dest = get_move_destination(mv)
                        if dest == coord:
                            if isinstance(mv, dict):
                                mv['movedBy'] = turn
                            else:
                                try:
                                    setattr(mv, 'movedBy', turn)
                                except Exception:
                                    pass
                            board.playMove(mv, updateValue=True, storeMove=True)
                            turn = 'Black' if turn == 'White' else 'White'
                            executed = True
                            break
                    selected_catapult = None
                    catapult_moves = []
                    valid_squares = []
                    # if executed we already played; continue loop
                    continue

                # Select Catapult by clicking empty square that contains one in underBoard
                if piece == 0 and under_piece != 0 and under_piece.color == turn:
                    selected_catapult = under_piece
                    catapult_moves = safe_return_valid_moves(selected_catapult, board)
                    valid_squares = [get_move_destination(mv) for mv in catapult_moves if get_move_destination(mv)]
                    continue

                # If clicked a piece of current player's color
                if piece != 0 and piece.color == turn:
                    # Catapult on top of board (shouldn't normally happen - catapult is underBoard),
                    # but if you have piece named Catapult in board[][] treat as click->click too
                    if piece.name == 'Catapult':
                        selected_catapult = piece
                        catapult_moves = safe_return_valid_moves(selected_catapult, board)
                        valid_squares = [get_move_destination(mv) for mv in catapult_moves if get_move_destination(mv)]
                        continue

                    # Normal drag mode for other pieces
                    dragging = True
                    drag_piece = piece
                    drag_img = piece_images.get(piece.color.lower() + "_" + piece.name.lower())
                    valid_moves = safe_return_valid_moves(piece, board)
                    valid_squares = [get_move_destination(mv) for mv in valid_moves if get_move_destination(mv)]
                    continue

                # If clicked an empty square (no piece and no underpiece) -> clear any selection
                selected_catapult = None
                catapult_moves = []
                valid_squares = []
                dragging = False
                drag_piece = None
                drag_img = None
                valid_moves = []

            # Mouse up: finish dragging and attempt move
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and dragging:
                coord = coord_from_mouse(pygame.mouse.get_pos())
                chosen_move = None
                if coord:
                    for mv in valid_moves:
                        dest = get_move_destination(mv)
                        if dest == coord:
                            chosen_move = mv
                            break
                if chosen_move:
                    if isinstance(chosen_move, dict):
                        chosen_move['movedBy'] = turn
                    else:
                        try:
                            setattr(chosen_move, 'movedBy', turn)
                        except Exception:
                            pass
                    board.playMove(chosen_move, updateValue=True, storeMove=True)
                    turn = 'Black' if turn == 'White' else 'White'

                # cleanup drag state
                dragging = False
                drag_piece = None
                drag_img = None
                valid_moves = []
                valid_squares = []

        # --- Draw everything ---
        draw_board()
        highlight_squares(valid_squares)
        draw_catapults(board)
        draw_pieces(board, dragging_piece=drag_piece)

        # draw dragging piece under cursor
        if dragging and drag_img:
            mx, my = pygame.mouse.get_pos()
            WIN.blit(drag_img, (mx - SQ_SIZE//2, my - SQ_SIZE//2))
        elif dragging and drag_piece and drag_img is None:
            # text fallback
            mx, my = pygame.mouse.get_pos()
            label = FONT.render(drag_piece.name[0].upper() if drag_piece.color=='White' else drag_piece.name[0].lower(), True, TEXT_COLOR)
            WIN.blit(label, (mx - 8, my - 8))

        # HUD: turn
        turn_text = FONT.render(f"Turn: {turn}", True, (0, 0, 0))
        WIN.blit(turn_text, (8, HEIGHT - 22))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
