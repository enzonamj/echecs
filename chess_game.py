# =============================================================================
# chess_game.py — Classe Chess (chef d'orchestre du jeu)
# =============================================================================
# Cette classe gère la partie dans son ensemble : les joueurs, le plateau,
# la boucle de jeu, la validation des coups et la sauvegarde/restauration.
# =============================================================================

import json
import os
from board import Board
from position import Position
from player import Player, AIPlayer


class Chess:
    """
    Classe principale qui orchestre une partie d'échecs complète.
    Elle contient le plateau (Board) et les deux joueurs (Player ou AIPlayer).
    """

    def __init__(self):
        # Le plateau de jeu
        self.board = Board()

        # La liste des joueurs — C'est notre LISTE obligatoire du cahier des charges !
        # # On utilise une liste car l'ordre compte (index 0 = blanc, index 1 = noir)
        self.players = []

        # Le joueur dont c'est le tour
        self.currentPlayer = None

        # Historique des coups (pour l'affichage et la sauvegarde)
        self.move_history = []

    # =========================================================================
    # Initialisation des joueurs
    # =========================================================================
    def initPlayers(self):
        """
        Demande le nom de chaque joueur et crée les objets Player ou AIPlayer.
        Si le nom est "AI", c'est une IA qui joue à la place du joueur humain.
        """
        print("\n" + "="*50)
        print("     BIENVENUE AU JEU D'ÉCHECS !")
        print("="*50)
        print("(Tapez 'AI' pour jouer contre l'ordinateur)\n")

        names = []
        for color, color_name in [(0, "Blancs"), (1, "Noirs")]:
            name = input(f"Nom du joueur {color_name} : ").strip()
            if not name:
                name = f"Joueur {color_name}"
            names.append((name, color))

        # Créer les objets Player ou AIPlayer selon le nom saisi
        for name, color in names:
            if name.upper() == "AI":
                self.players.append(AIPlayer("Ordinateur", color))
            else:
                self.players.append(Player(name, color))

        # Les blancs commencent toujours aux échecs
        self.currentPlayer = self.players[0]
        print(f"\nC'est {self.players[0]} qui commence !")

    # =========================================================================
    # Affichage du plateau
    # =========================================================================
    def displayBoard(self):
        """
        Affiche l'échiquier dans le terminal avec les coordonnées.
        Les pièces blanches sont en majuscules, les noires en minuscules.
        """
        print("\n    a  b  c  d  e  f  g  h")
        print("  +" + "---" * 8 + "+")

        for row in range(8, 0, -1):  # De la rangée 8 (haut) à 1 (bas)
            print(f"{row} |", end="")
            for col in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                pos = Position(col, row)
                piece = self.board.getPiece(pos)
                if piece is None:
                    # Case vide : on alterne les symboles pour simuler les couleurs
                    if (ord(col) + row) % 2 == 0:
                        print(" . ", end="")
                    else:
                        print("   ", end="")
                else:
                    # Pièce blanche en MAJUSCULE, noire en minuscule
                    symbol = str(piece) if piece.color == 0 else str(piece).lower()
                    print(f" {symbol} ", end="")
            print(f"| {row}")

        print("  +" + "---" * 8 + "+")
        print("    a  b  c  d  e  f  g  h\n")

    # =========================================================================
    # Validation et exécution des coups
    # =========================================================================
    def parseMove(self, move: str):
        """
        Analyse la chaîne de coup et retourne (piece, fromPos, toPos) ou None si invalide.
        Format attendu : "Nb1 c3" → pièce N sur b1, destination c3
        """
        try:
            parts = move.strip().split()
            if len(parts) != 2:
                return None

            origin_str = parts[0]  # Ex: "Nb1"
            dest_str = parts[1]    # Ex: "c3"

            piece_id = origin_str[0].upper()
            from_pos = Position.from_string(origin_str[1:])
            to_pos = Position.from_string(dest_str)

            # Récupérer la pièce sur la case de départ
            piece = self.board.getPiece(from_pos)

            if piece is None:
                print(f"  Aucune pièce en {from_pos} !")
                return None

            if str(piece).upper() != piece_id:
                print(f"  La pièce en {from_pos} est un(e) '{piece}', pas un(e) '{piece_id}' !")
                return None

            if piece.color != self.currentPlayer.color:
                print(f"  Cette pièce ne vous appartient pas !")
                return None

            return piece, from_pos, to_pos

        except (ValueError, IndexError):
            return None

    def isValidMove(self, move: str) -> bool:
        """
        Vérifie qu'un coup est valide selon les règles des échecs.
        Retourne True si le coup peut être joué.
        """
        parsed = self.parseMove(move)
        if parsed is None:
            return False

        piece, from_pos, to_pos = parsed

        # Vérifier les règles de déplacement de la pièce
        if not piece.isValidMove(to_pos, self.board):
            print(f"  Mouvement invalide pour {piece} !")
            return False

        # Vérifier que ce coup ne met pas notre propre roi en échec
        # # On simule le coup sur une copie du plateau pour vérifier
        board_copy = self.board.copy()
        board_copy.movePiece(from_pos, to_pos)
        if board_copy.is_in_check(self.currentPlayer.color):
            print("  Ce coup laisse votre roi en échec !")
            return False

        return True

    def updateBoard(self, move: str):
        """
        Applique le coup sur le plateau (après validation).
        """
        parsed = self.parseMove(move)
        if parsed is None:
            return

        piece, from_pos, to_pos = parsed
        self.board.movePiece(from_pos, to_pos)
        self.move_history.append(move)
        print(f"  ✓ {self.currentPlayer.name} joue : {move}")

    # =========================================================================
    # Gestion du tour et fin de partie
    # =========================================================================
    def switchPlayer(self):
        """
        Passe la main à l'autre joueur.
        # On utilise l'index dans la liste : si currentPlayer est players[0],
        # on passe à players[1], et vice versa.
        """
        if self.currentPlayer is self.players[0]:
            self.currentPlayer = self.players[1]
        else:
            self.currentPlayer = self.players[0]

    def isCheckMate(self) -> bool:
        """
        Vérifie si le joueur courant est en échec et mat.
        C'est le cas si :
        1. Le roi est en échec
        2. Aucun coup possible ne peut retirer l'échec
        """
        color = self.currentPlayer.color

        # Si le roi n'est pas en échec, ce n'est pas mat (peut être pat)
        if not self.board.is_in_check(color):
            return False

        # Chercher si au moins un coup peut sauver le roi
        pieces = self.board.get_all_pieces(color)
        columns = Position.COLUMNS

        for piece in pieces:
            for col in columns:
                for row in range(1, 9):
                    dest = Position(col, row)
                    if piece.isValidMove(dest, self.board):
                        board_copy = self.board.copy()
                        board_copy.movePiece(piece.position, dest)
                        if not board_copy.is_in_check(color):
                            return False  # Il existe un coup qui sauve le roi !

        return True  # Aucun coup possible → échec et mat !

    def isStalemate(self) -> bool:
        """
        Vérifie le pat : le joueur courant n'est pas en échec mais n'a aucun coup légal.
        """
        color = self.currentPlayer.color

        if self.board.is_in_check(color):
            return False  # C'est un échec, pas un pat

        pieces = self.board.get_all_pieces(color)
        columns = Position.COLUMNS

        for piece in pieces:
            for col in columns:
                for row in range(1, 9):
                    dest = Position(col, row)
                    if piece.isValidMove(dest, self.board):
                        board_copy = self.board.copy()
                        board_copy.movePiece(piece.position, dest)
                        if not board_copy.is_in_check(color):
                            return False  # Il existe un coup légal

        return True  # Aucun coup légal → pat

    # =========================================================================
    # Sauvegarde et restauration
    # =========================================================================
    def save(self, filename: str = "sauvegarde.json"):
        """
        Sauvegarde la partie en cours dans un fichier JSON.
        # On utilise JSON car c'est lisible et facile à charger.
        """
        data = {
            'board': self.board.to_dict(),
            'current_player_color': self.currentPlayer.color,
            'move_history': self.move_history,
            'players': [
                {'name': p.name, 'color': p.color, 'is_ai': isinstance(p, AIPlayer)}
                for p in self.players
            ]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  💾 Partie sauvegardée dans '{filename}'")

    def load(self, filename: str = "sauvegarde.json"):
        """
        Restaure une partie depuis un fichier JSON.
        """
        if not os.path.exists(filename):
            print(f"  Fichier '{filename}' introuvable !")
            return False

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.board.from_dict(data['board'])
        self.move_history = data['move_history']

        # Recréer les joueurs
        self.players = []
        for p_data in data['players']:
            if p_data['is_ai']:
                self.players.append(AIPlayer(p_data['name'], p_data['color']))
            else:
                self.players.append(Player(p_data['name'], p_data['color']))

        # Restaurer le joueur courant
        current_color = data['current_player_color']
        self.currentPlayer = next(p for p in self.players if p.color == current_color)

        print(f"  📂 Partie restaurée depuis '{filename}'")
        return True

    # =========================================================================
    # Boucle principale du jeu
    # =========================================================================
    def play(self):
        """
        Démarre et gère la partie d'échecs complète.
        Suit le pseudo-code du cahier des charges :
          - Initialiser les joueurs
          - Tant qu'il n'y a pas d'échec et mat :
              - Afficher le plateau
              - Demander un coup valide
              - Mettre à jour le plateau
              - Changer de joueur
        """
        self.initPlayers()

        while True:
            # Afficher le plateau
            self.displayBoard()

            # Vérifier la fin de partie
            if self.isCheckMate():
                self.switchPlayer()  # Le joueur qui vient de jouer a gagné
                print(f"\n🏆 ÉCHEC ET MAT ! {self.currentPlayer.name} ({self.currentPlayer.color_name()}) a gagné !\n")
                break

            if self.isStalemate():
                print(f"\n🤝 PAT ! La partie est nulle !\n")
                break

            # Indiquer si le roi est en échec
            if self.board.is_in_check(self.currentPlayer.color):
                print(f"  ⚠️  {self.currentPlayer.name}, votre roi est EN ÉCHEC !")

            # Obtenir et valider le coup
            move = None

            if isinstance(self.currentPlayer, AIPlayer):
                # L'IA cherche un coup valide directement
                print(f"\n[{self.currentPlayer.color_name()}] {self.currentPlayer.name} (IA) réfléchit...")
                import time
                time.sleep(0.5)
                move = self.currentPlayer.get_random_valid_move(self.board)
                if move is None:
                    print(f"  L'IA n'a plus de coup possible !")
                    break
            else:
                # Joueur humain : boucler jusqu'à un coup valide
                print(f"Commandes : 'save' pour sauvegarder, 'load' pour charger, 'quit' pour quitter")
                while True:
                    raw = input(f"[{self.currentPlayer.color_name()}] {self.currentPlayer.name} → ").strip()

                    if raw.lower() == 'save':
                        self.save()
                        continue
                    elif raw.lower() == 'load':
                        self.load()
                        self.displayBoard()
                        continue
                    elif raw.lower() in ('quit', 'exit'):
                        print("À bientôt !")
                        return

                    if self.isValidMove(raw):
                        move = raw
                        break
                    else:
                        print("  Coup invalide, réessayez.")

            # Appliquer le coup
            self.updateBoard(move)

            # Passer à l'autre joueur
            self.switchPlayer()
