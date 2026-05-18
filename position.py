# =============================================================================
# position.py — Classe Position
# =============================================================================
# Une position sur l'échiquier est représentée par une colonne (lettre a-h)
# et une rangée (chiffre 1-8). Par exemple "e1" ou "a8".
# =============================================================================

class Position:
    """
    Représente une case de l'échiquier avec une colonne (a-h) et une rangée (1-8).
    """

    # On définit les colonnes valides dans un attribut de classe (c'est pratique
    # pour vérifier qu'une position est bien sur l'échiquier)
    COLUMNS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    def __init__(self, column: str, row: int):
        # On vérifie que la colonne et la rangée sont valides avant de les stocker
        if column not in self.COLUMNS:
            raise ValueError(f"Colonne invalide : '{column}'. Doit être parmi {self.COLUMNS}")
        if not (1 <= row <= 8):
            raise ValueError(f"Rangée invalide : {row}. Doit être entre 1 et 8")

        # Encapsulation : les attributs sont "privés" (convention _ en Python)
        self._column = column
        self._row = row

    # --- Getters ---
    @property
    def column(self) -> str:
        return self._column

    @property
    def row(self) -> int:
        return self._row

    # --- Index numériques utiles pour les calculs de déplacement ---
    @property
    def col_index(self) -> int:
        """Retourne l'index numérique de la colonne (a=0, b=1, ..., h=7)."""
        return self.COLUMNS.index(self._column)

    # --- Représentation en chaîne de caractères ---
    def __str__(self) -> str:
        # Par exemple : "e1", "a8"
        return f"{self._column}{self._row}"

    def __repr__(self) -> str:
        return f"Position('{self._column}', {self._row})"

    # --- Comparaison (utile pour tester si deux positions sont identiques) ---
    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return False
        return self._column == other._column and self._row == other._row

    def __hash__(self):
        # Nécessaire pour pouvoir utiliser des Position comme clés de dictionnaire
        return hash((self._column, self._row))

    # --- Méthode utilitaire : créer une Position à partir d'une chaîne ---
    @staticmethod
    def from_string(s: str) -> 'Position':
        """
        Crée une Position depuis une chaîne comme "e1" ou "a8".
        # On utilise une méthode statique car elle ne dépend d'aucune instance.
        """
        if len(s) != 2:
            raise ValueError(f"Format invalide : '{s}'. Attendu : lettre + chiffre (ex: 'e4')")
        column = s[0].lower()
        try:
            row = int(s[1])
        except ValueError:
            raise ValueError(f"Format invalide : '{s}'. Le deuxième caractère doit être un chiffre")
        return Position(column, row)

    # --- Méthode utilitaire : vérifier si une position (col_idx, row) est dans le plateau ---
    @staticmethod
    def is_valid_indices(col_idx: int, row: int) -> bool:
        """Vérifie si des indices numériques correspondent à une case valide."""
        return 0 <= col_idx <= 7 and 1 <= row <= 8

    @staticmethod
    def from_indices(col_idx: int, row: int) -> 'Position':
        """Crée une Position depuis des indices numériques (col 0-7, row 1-8)."""
        return Position(Position.COLUMNS[col_idx], row)
