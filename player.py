# =============================================================================
# player.py — Classes Player et AIPlayer
# =============================================================================
# Player représente un joueur humain qui saisit ses coups au clavier.
# AIPlayer hérite de Player et génère ses coups automatiquement (aléatoire).
# =============================================================================

import random
from position import Position


class Player:
    """
    Représente un joueur humain.
    Il saisit ses coups via askMove() en tapant par exemple "Nb1 c3".
    """

    def __init__(self, name: str, color: int):
        # name : nom du joueur
        # color : 0 = blanc, 1 = noir
        self._name = name
        self._color = color

    # --- Getters ---
    @property
    def name(self) -> str:
        return self._name

    @property
    def color(self) -> int:
        return self._color

    def color_name(self) -> str:
        return "Blanc" if self._color == 0 else "Noir"

    def askMove(self) -> str:
        """
        Demande au joueur de saisir son coup.
        Format attendu : "Xe1 e3" où X est l'identifiant de la pièce,
        e1 est la position de départ et e3 la destination.
        # On boucle jusqu'à ce que le format soit correct (mais pas forcément valide aux règles).
        """
        while True:
            move = input(f"\n[{self.color_name()}] {self._name}, entrez votre coup (ex: Nb1 c3) : ").strip()
            if self._validate_format(move):
                return move
            print("  Format invalide ! Exemple valide : 'Nb1 c3' (pièce + case départ + case arrivée)")

    @staticmethod
    def _validate_format(move: str) -> bool:
        """
        Vérifie que la chaîne de coup a le bon format.
        Format : "Xab cd" où X=lettre pièce, ab=position départ, cd=position arrivée.
        Exemples valides : "Nb1 c3", "Pe2 e4", "Ke1 d1"
        """
        parts = move.split()
        if len(parts) != 2:
            return False

        origin_str = parts[0]
        dest_str = parts[1]

        # L'origine : 1 lettre pièce + 2 caractères de position
        if len(origin_str) != 3:
            return False
        piece_id = origin_str[0].upper()
        if piece_id not in ['K', 'Q', 'B', 'N', 'R', 'P']:
            return False

        try:
            Position.from_string(origin_str[1:])  # Vérifie "b1" par exemple
            Position.from_string(dest_str)         # Vérifie "c3" par exemple
        except ValueError:
            return False

        return True

    def __str__(self) -> str:
        return f"{self._name} ({self.color_name()})"


class AIPlayer(Player):
    """
    Joueur IA qui génère automatiquement un coup aléatoire valide.
    # AIPlayer hérite de Player (sous-classe) et redéfinit askMove().
    # Grâce au polymorphisme, le reste du programme n'a pas besoin de savoir
    # si le joueur est humain ou IA — il appelle juste askMove() dans les deux cas !
    """

    def __init__(self, name: str, color: int):
        super().__init__(name, color)  # On appelle le constructeur de Player

    def askMove(self) -> str:
        """
        Génère un coup aléatoire parmi tous les coups valides de l'IA.
        Si aucun coup n'est trouvé, retourne un coup factice (ne devrait pas arriver).
        """
        import time
        print(f"\n[{self.color_name()}] {self._name} (IA) réfléchit...")
        time.sleep(0.5)  # Petite pause pour simuler la "réflexion" de l'IA

        # On retourne None ici et on laisse Chess gérer la recherche de coup valide
        # (pour éviter d'importer Board ici et créer une dépendance circulaire)
        return "__AI__"

    def get_random_valid_move(self, board) -> str:
        """
        Cherche un coup valide aléatoire parmi toutes les pièces de l'IA.
        Retourne une chaîne de coup ou None si aucun coup n'est possible.
        """
        pieces = board.get_all_pieces(self._color)
        random.shuffle(pieces)  # On mélange pour que l'IA joue de façon aléatoire

        columns = Position.COLUMNS

        for piece in pieces:
            # On essaie toutes les cases du plateau comme destination
            all_positions = []
            for col in columns:
                for row in range(1, 9):
                    all_positions.append(Position(col, row))

            random.shuffle(all_positions)

            for dest in all_positions:
                if piece.isValidMove(dest, board):
                    # On vérifie aussi que ce coup ne met pas notre propre roi en échec
                    board_copy = board.copy()
                    board_copy.movePiece(piece.position, dest)
                    if not board_copy.is_in_check(self._color):
                        # Coup valide trouvé !
                        move_str = f"{str(piece)}{piece.position} {dest}"
                        return move_str

        return None  # Aucun coup possible → probablement mat ou pat
