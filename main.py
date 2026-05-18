# =============================================================================
# main.py — Point d'entrée du programme
# =============================================================================
# C'est ici qu'on lance le jeu ! On crée une instance de Chess et on appelle play().
# Toutes les classes sont dans des fichiers séparés et importées ici.
# (Pas de copier-coller de code — utilisation des imports comme demandé !)
# =============================================================================

from chess_game import Chess


def main():
    """
    Fonction principale : crée une partie d'échecs et la lance.
    """
    game = Chess()
    game.play()


# Ce bloc garantit que main() n'est appelé que si on exécute ce fichier directement
# (et non si on l'importe depuis un autre module)
if __name__ == "__main__":
    main()
