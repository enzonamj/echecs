# Jeu d'Échecs — Projet I1 2025/2026

Implémentation d'un jeu d'échecs en Python avec interface en mode texte, orientée objet.

## Structure des fichiers

| Fichier | Contenu |
|---|---|
| `position.py` | Classe `Position` (coordonnées sur l'échiquier) |
| `pieces.py` | Classes `Piece`, `King`, `Queen`, `Bishop`, `Knight`, `Rook`, `Pawn` |
| `board.py` | Classe `Board` (plateau de jeu) |
| `player.py` | Classes `Player` et `AIPlayer` |
| `chess_game.py` | Classe `Chess` (gestion de la partie) |
| `main.py` | Point d'entrée du programme |
| `test_chess.py` | Tests unitaires (unittest) |

## Lancer le jeu

```bash
python main.py
```

## Lancer les tests unitaires

```bash
python -m pytest test_chess.py -v
# ou
python test_chess.py
```

## Format des coups

Un coup se saisit sous la forme : `<Pièce><case_départ> <case_arrivée>`

Exemples :
- `Nb1 c3` — Cavalier de b1 vers c3
- `Pe2 e4` — Pion de e2 vers e4
- `Ke1 d1` — Roi de e1 vers d1

Identifiants des pièces : `K`=Roi, `Q`=Reine, `B`=Fou, `N`=Cavalier, `R`=Tour, `P`=Pion

## Commandes pendant la partie

- `save` — Sauvegarder la partie en cours
- `load` — Charger une partie sauvegardée
- `quit` — Quitter le jeu

## Jouer contre l'IA

Entrez `AI` comme nom de joueur pour jouer contre l'ordinateur.

## Fonctionnalités implémentées

- Tous les déplacements des 6 types de pièces
- Détection de l'échec et du mat
- Détection du pat
- Sauvegarde/restauration en JSON
- IA aléatoire (AIPlayer)
- Tests unitaires avec unittest
