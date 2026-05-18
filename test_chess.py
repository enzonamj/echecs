# =============================================================================
# test_chess.py — Tests unitaires avec le framework unittest
# =============================================================================
# On teste chaque classe de façon isolée pour vérifier que le code fonctionne.
# # unittest est le framework de test standard de Python.
# Pour lancer les tests : python -m pytest test_chess.py -v
#                     ou : python test_chess.py
# =============================================================================

import unittest
from position import Position
from pieces import King, Queen, Bishop, Knight, Rook, Pawn
from board import Board


# =============================================================================
# Tests de la classe Position
# =============================================================================
class TestPosition(unittest.TestCase):

    def test_creation_valide(self):
        """Vérifie qu'on peut créer une position correcte."""
        pos = Position('e', 4)
        self.assertEqual(pos.column, 'e')
        self.assertEqual(pos.row, 4)

    def test_str(self):
        """Vérifie que __str__ retourne bien le format 'e4'."""
        pos = Position('e', 4)
        self.assertEqual(str(pos), 'e4')

    def test_from_string(self):
        """Vérifie qu'on peut créer une Position depuis une chaîne."""
        pos = Position.from_string('a1')
        self.assertEqual(pos.column, 'a')
        self.assertEqual(pos.row, 1)

    def test_egalite(self):
        """Deux positions identiques doivent être égales."""
        p1 = Position('d', 5)
        p2 = Position('d', 5)
        self.assertEqual(p1, p2)

    def test_inegalite(self):
        """Deux positions différentes ne doivent pas être égales."""
        p1 = Position('a', 1)
        p2 = Position('h', 8)
        self.assertNotEqual(p1, p2)

    def test_colonne_invalide(self):
        """Une colonne invalide doit lever une ValueError."""
        with self.assertRaises(ValueError):
            Position('z', 4)

    def test_rangee_invalide(self):
        """Une rangée invalide doit lever une ValueError."""
        with self.assertRaises(ValueError):
            Position('a', 9)

    def test_col_index(self):
        """Vérifie la conversion colonne → index numérique."""
        self.assertEqual(Position('a', 1).col_index, 0)
        self.assertEqual(Position('h', 1).col_index, 7)
        self.assertEqual(Position('e', 1).col_index, 4)


# =============================================================================
# Tests du Cavalier (Knight)
# =============================================================================
class TestKnight(unittest.TestCase):

    def setUp(self):
        """
        Prépare un plateau vide pour les tests.
        # setUp() est appelé avant chaque test — pratique pour réinitialiser l'état.
        """
        self.board = Board()
        # On enlève toutes les pièces pour tester en isolation
        self.board._squares = {}

    def _place(self, piece):
        self.board._squares[piece.position] = piece

    def test_mouvement_valide_en_L(self):
        """Le Cavalier doit pouvoir bouger en L."""
        knight = Knight(Position('b', 1), 0)
        self._place(knight)
        # b1 → c3 : +1 col, +2 row → valide
        self.assertTrue(knight.isValidMove(Position('c', 3), self.board))
        # b1 → a3 : -1 col, +2 row → valide
        self.assertTrue(knight.isValidMove(Position('a', 3), self.board))

    def test_mouvement_invalide_en_ligne(self):
        """Le Cavalier ne peut pas bouger en ligne droite."""
        knight = Knight(Position('b', 1), 0)
        self._place(knight)
        self.assertFalse(knight.isValidMove(Position('b', 3), self.board))

    def test_capture_piece_adverse(self):
        """Le Cavalier peut capturer une pièce adverse."""
        knight = Knight(Position('b', 1), 0)
        enemy = Pawn(Position('c', 3), 1)
        self._place(knight)
        self._place(enemy)
        self.assertTrue(knight.isValidMove(Position('c', 3), self.board))

    def test_ne_capture_pas_allie(self):
        """Le Cavalier ne peut pas capturer un allié."""
        knight = Knight(Position('b', 1), 0)
        ally = Pawn(Position('c', 3), 0)
        self._place(knight)
        self._place(ally)
        self.assertFalse(knight.isValidMove(Position('c', 3), self.board))


# =============================================================================
# Tests de la Tour (Rook)
# =============================================================================
class TestRook(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.board._squares = {}

    def _place(self, piece):
        self.board._squares[piece.position] = piece

    def test_mouvement_horizontal(self):
        """La Tour peut bouger horizontalement."""
        rook = Rook(Position('a', 1), 0)
        self._place(rook)
        self.assertTrue(rook.isValidMove(Position('h', 1), self.board))

    def test_mouvement_vertical(self):
        """La Tour peut bouger verticalement."""
        rook = Rook(Position('a', 1), 0)
        self._place(rook)
        self.assertTrue(rook.isValidMove(Position('a', 8), self.board))

    def test_mouvement_diagonal_invalide(self):
        """La Tour ne peut pas bouger en diagonale."""
        rook = Rook(Position('a', 1), 0)
        self._place(rook)
        self.assertFalse(rook.isValidMove(Position('b', 2), self.board))

    def test_bloque_par_piece(self):
        """La Tour est bloquée si une pièce est sur son chemin."""
        rook = Rook(Position('a', 1), 0)
        blocker = Pawn(Position('a', 4), 0)
        self._place(rook)
        self._place(blocker)
        self.assertFalse(rook.isValidMove(Position('a', 7), self.board))


# =============================================================================
# Tests du Pion (Pawn)
# =============================================================================
class TestPawn(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.board._squares = {}

    def _place(self, piece):
        self.board._squares[piece.position] = piece

    def test_avance_une_case(self):
        """Le pion blanc peut avancer d'une case."""
        pawn = Pawn(Position('e', 4), 0)
        self._place(pawn)
        self.assertTrue(pawn.isValidMove(Position('e', 5), self.board))

    def test_double_avance_depuis_depart(self):
        """Le pion peut avancer de 2 cases depuis sa rangée de départ."""
        pawn = Pawn(Position('e', 2), 0)
        self._place(pawn)
        self.assertTrue(pawn.isValidMove(Position('e', 4), self.board))

    def test_pas_de_double_avance_hors_depart(self):
        """Le pion ne peut pas avancer de 2 cases s'il a déjà bougé."""
        pawn = Pawn(Position('e', 3), 0)
        self._place(pawn)
        self.assertFalse(pawn.isValidMove(Position('e', 5), self.board))

    def test_capture_diagonale(self):
        """Le pion capture en diagonale."""
        pawn = Pawn(Position('e', 4), 0)
        enemy = Pawn(Position('f', 5), 1)
        self._place(pawn)
        self._place(enemy)
        self.assertTrue(pawn.isValidMove(Position('f', 5), self.board))

    def test_pas_de_capture_devant(self):
        """Le pion ne peut pas avancer si une pièce bloque."""
        pawn = Pawn(Position('e', 4), 0)
        blocker = Pawn(Position('e', 5), 1)
        self._place(pawn)
        self._place(blocker)
        self.assertFalse(pawn.isValidMove(Position('e', 5), self.board))

    def test_pion_noir_avance_vers_bas(self):
        """Le pion noir avance vers les rangées décroissantes."""
        pawn = Pawn(Position('e', 7), 1)
        self._place(pawn)
        self.assertTrue(pawn.isValidMove(Position('e', 6), self.board))
        self.assertFalse(pawn.isValidMove(Position('e', 8), self.board))


# =============================================================================
# Tests du Fou (Bishop)
# =============================================================================
class TestBishop(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.board._squares = {}

    def _place(self, piece):
        self.board._squares[piece.position] = piece

    def test_mouvement_diagonal(self):
        """Le Fou se déplace en diagonale."""
        bishop = Bishop(Position('c', 1), 0)
        self._place(bishop)
        self.assertTrue(bishop.isValidMove(Position('h', 6), self.board))

    def test_mouvement_non_diagonal_invalide(self):
        """Le Fou ne peut pas se déplacer en ligne droite."""
        bishop = Bishop(Position('c', 1), 0)
        self._place(bishop)
        self.assertFalse(bishop.isValidMove(Position('c', 5), self.board))


# =============================================================================
# Tests du plateau (Board)
# =============================================================================
class TestBoard(unittest.TestCase):

    def test_initialisation(self):
        """Le plateau doit avoir 32 pièces au départ."""
        board = Board()
        all_pieces = board.get_all_pieces()
        self.assertEqual(len(all_pieces), 32)

    def test_getPiece_case_vide(self):
        """Une case vide retourne None."""
        board = Board()
        self.assertIsNone(board.getPiece(Position('e', 4)))

    def test_getPiece_avec_piece(self):
        """La case e1 doit contenir le Roi blanc au départ."""
        board = Board()
        piece = board.getPiece(Position('e', 1))
        self.assertIsNotNone(piece)
        self.assertEqual(str(piece), 'K')
        self.assertEqual(piece.color, 0)

    def test_movePiece(self):
        """Déplacer une pièce doit mettre à jour le plateau."""
        board = Board()
        board.movePiece(Position('e', 2), Position('e', 4))
        self.assertIsNone(board.getPiece(Position('e', 2)))
        piece = board.getPiece(Position('e', 4))
        self.assertIsNotNone(piece)
        self.assertEqual(str(piece), 'P')

    def test_sauvegarde_restauration(self):
        """La sauvegarde et la restauration doivent donner le même plateau."""
        board = Board()
        board.movePiece(Position('e', 2), Position('e', 4))
        data = board.to_dict()

        board2 = Board()
        board2.from_dict(data)

        self.assertIsNone(board2.getPiece(Position('e', 2)))
        piece = board2.getPiece(Position('e', 4))
        self.assertIsNotNone(piece)
        self.assertEqual(str(piece), 'P')


# =============================================================================
# Lancement des tests
# =============================================================================
if __name__ == '__main__':
    unittest.main(verbosity=2)
