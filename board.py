# =============================================================================
# board.py — Classe Board (le plateau de jeu)
# =============================================================================
# Le plateau contient toutes les pièces et permet de retrouver une pièce
# à une position donnée, ou de retrouver la position d'une pièce.
#
# On utilise un DICTIONNAIRE pour stocker les pièces :
#   clé   → Position (ex: Position('e', 1))
#   valeur → Piece (ex: King(blanc))
#
# Ce dictionnaire est très pratique car on peut retrouver instantanément
# quelle pièce est sur une case, sans parcourir tout le plateau !
# =============================================================================

from position import Position
from pieces import King, Queen, Bishop, Knight, Rook, Pawn, Piece


class Board:
    """
    Représente l'état complet de l'échiquier à un instant donné.
    Stocke toutes les pièces dans un dictionnaire {Position: Piece}.
    """

    def __init__(self):
        # Le dictionnaire principal : position → pièce
        # # C'est notre DICTIONNAIRE obligatoire du cahier des charges !
        self._squares = {}

        # On initialise le plateau avec toutes les pièces à leur place de départ
        self._setup_initial_position()

    def _setup_initial_position(self):
        """
        Place toutes les pièces dans leur position initiale.
        # L'ordre des pièces sur la première rangée est standard aux échecs :
        # Tour, Cavalier, Fou, Reine, Roi, Fou, Cavalier, Tour
        """
        # Rangée 1 (blancs) et rangée 8 (noirs) — pièces principales
        back_rank = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        piece_classes = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for col, PieceClass in zip(back_rank, piece_classes):
            # Pièces blanches en rangée 1
            self._place(PieceClass(Position(col, 1), 0))
            # Pièces noires en rangée 8
            self._place(PieceClass(Position(col, 8), 1))

        # Rangée 2 (pions blancs) et rangée 7 (pions noirs)
        for col in back_rank:
            self._place(Pawn(Position(col, 2), 0))
            self._place(Pawn(Position(col, 7), 1))

    def _place(self, piece: Piece):
        """Place une pièce sur l'échiquier (ajoute au dictionnaire)."""
        self._squares[piece.position] = piece

    def getPiece(self, position: Position):
        """
        Retourne la pièce sur la case 'position', ou None si la case est vide.
        # dict.get() retourne None par défaut si la clé n'existe pas — parfait !
        """
        return self._squares.get(position, None)

    def getPosition(self, piece: Piece):
        """
        Retourne la position d'une pièce, ou None si elle a été capturée.
        # On cherche dans les valeurs du dictionnaire quelle position correspond.
        """
        for pos, p in self._squares.items():
            if p is piece:
                return pos
        return None  # La pièce a été capturée et n'est plus sur le plateau

    def movePiece(self, fromPos: Position, toPos: Position):
        """
        Déplace la pièce de fromPos vers toPos.
        Si une pièce adverse est sur toPos, elle est capturée (supprimée du dict).
        """
        piece = self._squares.pop(fromPos)  # On retire la pièce de sa case actuelle
        piece.position = toPos              # On met à jour sa position interne
        self._squares[toPos] = piece        # On la place sur la nouvelle case

    def get_all_pieces(self, color: int = None):
        """
        Retourne la liste de toutes les pièces (ou celles d'une couleur donnée).
        # On utilise une LISTE pour stocker les résultats — liste obligatoire du cahier des charges !
        """
        result = []
        for piece in self._squares.values():
            if color is None or piece.color == color:
                result.append(piece)
        return result

    def is_in_check(self, color: int) -> bool:
        """
        Vérifie si le roi de la couleur 'color' est en échec.
        Un roi est en échec si une pièce adverse peut le capturer.
        """
        # Trouver la position du roi
        king_pos = None
        for pos, piece in self._squares.items():
            if piece.color == color and str(piece) == 'K':
                king_pos = pos
                break

        if king_pos is None:
            return False  # Le roi n'existe plus (ne devrait pas arriver)

        # Vérifier si une pièce adverse peut atteindre le roi
        enemy_color = 1 - color
        for piece in self.get_all_pieces(enemy_color):
            if piece.isValidMove(king_pos, self):
                return True

        return False

    def copy(self):
        """
        Crée une copie du plateau (utile pour simuler des coups sans modifier l'original).
        """
        import copy
        new_board = Board.__new__(Board)
        new_board._squares = {}
        for pos, piece in self._squares.items():
            new_pos = Position(pos.column, pos.row)
            new_piece = copy.copy(piece)
            new_piece._position = new_pos
            new_board._squares[new_pos] = new_piece
        return new_board

    def to_dict(self) -> dict:
        """
        Sérialise le plateau en dictionnaire Python (pour la sauvegarde).
        # On sauvegarde chaque pièce avec sa position, son type et sa couleur.
        """
        data = []
        for pos, piece in self._squares.items():
            data.append({
                'type': str(piece),
                'color': piece.color,
                'position': str(pos)
            })
        return {'pieces': data}

    def from_dict(self, data: dict):
        """
        Restaure le plateau depuis un dictionnaire (pour le chargement d'une sauvegarde).
        """
        from pieces import King, Queen, Bishop, Knight, Rook, Pawn
        TYPE_MAP = {'K': King, 'Q': Queen, 'B': Bishop, 'N': Knight, 'R': Rook, 'P': Pawn}

        self._squares = {}
        for piece_data in data['pieces']:
            PieceClass = TYPE_MAP[piece_data['type']]
            pos = Position.from_string(piece_data['position'])
            piece = PieceClass(pos, piece_data['color'])
            self._squares[pos] = piece
