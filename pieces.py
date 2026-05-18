# =============================================================================
# pieces.py — Classes représentant les pièces du jeu
# =============================================================================
# On a une classe abstraite "Piece" dont héritent les 6 types de pièces.
# Chaque pièce sait valider ses propres déplacements via isValidMove().
# =============================================================================

from abc import ABC, abstractmethod
from position import Position


class Piece(ABC):
    """
    Classe abstraite (ABC = Abstract Base Class) représentant une pièce d'échecs.
    # On utilise ABC pour empêcher d'instancier directement "Piece" —
    # il faut toujours passer par une sous-classe concrète (King, Queen, etc.)
    """

    def __init__(self, position: Position, color: int):
        # color : 0 = blanc, 1 = noir
        self._position = position
        self._color = color

    # --- Getters / Setters (encapsulation) ---
    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, new_pos: Position):
        self._position = new_pos

    @property
    def color(self) -> int:
        return self._color

    def color_name(self) -> str:
        return "Blanc" if self._color == 0 else "Noir"

    # --- Méthode abstraite : chaque sous-classe DOIT l'implémenter ---
    @abstractmethod
    def isValidMove(self, newPosition: Position, board) -> bool:
        """
        Vérifie si le déplacement vers newPosition est légal selon les règles
        des échecs pour ce type de pièce.
        # C'est @abstractmethod car chaque pièce a ses propres règles de mouvement.
        """
        pass

    # --- Méthode abstraite : retourne l'identifiant de la pièce (K, Q, B...) ---
    @abstractmethod
    def __str__(self) -> str:
        pass

    # --- Méthode utilitaire commune : y a-t-il une pièce de même couleur à destination ? ---
    def _destination_blocked_by_own_piece(self, newPosition: Position, board) -> bool:
        """
        Retourne True si la case de destination est occupée par une pièce de même couleur.
        # On ne peut pas capturer ses propres pièces !
        """
        target = board.getPiece(newPosition)
        return target is not None and target.color == self._color

    # --- Méthode utilitaire commune : vérifier que le chemin est libre (lignes droites) ---
    def _path_is_clear(self, newPosition: Position, board) -> bool:
        """
        Vérifie qu'il n'y a aucune pièce entre la position actuelle et newPosition
        en ligne droite (horizontale, verticale ou diagonale).
        # Le Cavalier est la seule pièce qui "saute" par-dessus — il n'utilise pas cette méthode.
        """
        col_start = self._position.col_index
        col_end = newPosition.col_index
        row_start = self._position.row
        row_end = newPosition.row

        # Déterminer la direction du mouvement
        # On utilise sign() manuellement : -1, 0 ou +1
        col_step = (col_end - col_start) // max(1, abs(col_end - col_start)) if col_end != col_start else 0
        row_step = (row_end - row_start) // max(1, abs(row_end - row_start)) if row_end != row_start else 0

        col = col_start + col_step
        row = row_start + row_step

        # On parcourt toutes les cases intermédiaires (on s'arrête avant la destination)
        while (col, row) != (col_end, row_end):
            intermediate = Position.from_indices(col, row)
            if board.getPiece(intermediate) is not None:
                return False  # Il y a une pièce sur le chemin !
            col += col_step
            row += row_step

        return True


# =============================================================================
# ROI — King
# =============================================================================
class King(Piece):
    """
    Le Roi se déplace d'une seule case dans n'importe quelle direction.
    """

    def isValidMove(self, newPosition: Position, board) -> bool:
        # Vérification : ne pas capturer ses propres pièces
        if self._destination_blocked_by_own_piece(newPosition, board):
            return False

        col_diff = abs(self._position.col_index - newPosition.col_index)
        row_diff = abs(self._position.row - newPosition.row)

        # Le Roi bouge d'exactement 1 case dans n'importe quelle direction
        # (y compris en diagonale, donc col_diff et row_diff peuvent être 0 ou 1)
        return col_diff <= 1 and row_diff <= 1 and (col_diff + row_diff) > 0

    def __str__(self) -> str:
        return 'K'


# =============================================================================
# REINE — Queen
# =============================================================================
class Queen(Piece):
    """
    La Reine se déplace en ligne droite (comme la Tour) ou en diagonale (comme le Fou),
    sur autant de cases qu'elle veut.
    """

    def isValidMove(self, newPosition: Position, board) -> bool:
        if self._destination_blocked_by_own_piece(newPosition, board):
            return False

        col_diff = abs(self._position.col_index - newPosition.col_index)
        row_diff = abs(self._position.row - newPosition.row)

        # Mouvement valide si en ligne droite OU en diagonale parfaite
        is_straight = (col_diff == 0 or row_diff == 0)
        is_diagonal = (col_diff == row_diff)

        if not (is_straight or is_diagonal):
            return False

        # Vérifier qu'il n'y a rien sur le chemin
        return self._path_is_clear(newPosition, board)

    def __str__(self) -> str:
        return 'Q'


# =============================================================================
# FOU — Bishop
# =============================================================================
class Bishop(Piece):
    """
    Le Fou se déplace uniquement en diagonale, sur autant de cases qu'il veut.
    Il reste toujours sur la même couleur de case.
    """

    def isValidMove(self, newPosition: Position, board) -> bool:
        if self._destination_blocked_by_own_piece(newPosition, board):
            return False

        col_diff = abs(self._position.col_index - newPosition.col_index)
        row_diff = abs(self._position.row - newPosition.row)

        # Mouvement diagonal : col_diff doit égaler row_diff (et être > 0)
        if col_diff != row_diff or col_diff == 0:
            return False

        return self._path_is_clear(newPosition, board)

    def __str__(self) -> str:
        return 'B'


# =============================================================================
# CAVALIER — Knight
# =============================================================================
class Knight(Piece):
    """
    Le Cavalier se déplace en "L" : 2 cases dans une direction + 1 case perpendiculaire.
    C'est la seule pièce qui peut "sauter" par-dessus les autres !
    """

    def isValidMove(self, newPosition: Position, board) -> bool:
        if self._destination_blocked_by_own_piece(newPosition, board):
            return False

        col_diff = abs(self._position.col_index - newPosition.col_index)
        row_diff = abs(self._position.row - newPosition.row)

        # Le "L" : (2,1) ou (1,2) — le Cavalier saute donc pas besoin de vérifier le chemin
        return (col_diff == 2 and row_diff == 1) or (col_diff == 1 and row_diff == 2)

    def __str__(self) -> str:
        return 'N'


# =============================================================================
# TOUR — Rook
# =============================================================================
class Rook(Piece):
    """
    La Tour se déplace en ligne droite (horizontale ou verticale),
    sur autant de cases qu'elle veut.
    """

    def isValidMove(self, newPosition: Position, board) -> bool:
        if self._destination_blocked_by_own_piece(newPosition, board):
            return False

        col_diff = abs(self._position.col_index - newPosition.col_index)
        row_diff = abs(self._position.row - newPosition.row)

        # Mouvement valide uniquement en ligne droite (colonne OU rangée, pas les deux)
        if not (col_diff == 0 or row_diff == 0) or (col_diff == 0 and row_diff == 0):
            return False

        return self._path_is_clear(newPosition, board)

    def __str__(self) -> str:
        return 'R'


# =============================================================================
# PION — Pawn
# =============================================================================
class Pawn(Piece):
    """
    Le Pion avance d'une case vers l'avant (2 cases depuis la rangée de départ).
    Il capture en diagonale d'une case.
    Les blancs avancent vers les rangées croissantes (1→8), les noirs vers les décroissantes (8→1).
    """

    def isValidMove(self, newPosition: Position, board) -> bool:
        col_diff = newPosition.col_index - self._position.col_index
        row_diff = newPosition.row - self._position.row

        # Direction selon la couleur :
        # Blanc (color=0) avance vers row croissante (+1), Noir (color=1) vers row décroissante (-1)
        direction = 1 if self._color == 0 else -1

        # Rangée de départ (pour le double pas initial)
        start_row = 2 if self._color == 0 else 7

        # --- Avance d'une case tout droit ---
        if col_diff == 0 and row_diff == direction:
            # La case doit être vide (le pion ne capture pas tout droit)
            return board.getPiece(newPosition) is None

        # --- Double avance depuis la rangée de départ ---
        if col_diff == 0 and row_diff == 2 * direction and self._position.row == start_row:
            # Les deux cases devant doivent être vides
            intermediate = Position.from_indices(
                self._position.col_index,
                self._position.row + direction
            )
            return board.getPiece(intermediate) is None and board.getPiece(newPosition) is None

        # --- Capture en diagonale ---
        if abs(col_diff) == 1 and row_diff == direction:
            target = board.getPiece(newPosition)
            # Il doit y avoir une pièce ennemie à capturer
            return target is not None and target.color != self._color

        return False

    def __str__(self) -> str:
        return 'P'
