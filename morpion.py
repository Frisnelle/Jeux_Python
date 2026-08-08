"""
Jeu du morpion (Tic-Tac-Toe).

Grille 3x3, deux joueurs (X et O) jouent chacun leur tour.
Le premier à aligner 3 symboles (ligne, colonne, diagonale) gagne.
Mode 2 joueurs humains, ou 1 joueur contre une IA (algorithme minimax),
avec un niveau de difficulté qui contrôle la fiabilité de l'IA.
"""

import random

COMBINAISONS_GAGNANTES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # lignes
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # colonnes
    (0, 4, 8), (2, 4, 6),             # diagonales
]

# Probabilité que l'IA joue un coup aléatoire au lieu du meilleur coup (minimax)
DIFFICULTES_IA = {
    "facile": 0.6,       # 60% de coups aléatoires -> facile à battre
    "moyen": 0.3,        # 30% -> jouable, quelques ouvertures
    "difficile": 0.1,    # 10% -> rare erreur, mais possible de gagner
    "impossible": 0.0,   # 0% -> IA parfaite (minimax pur, invincible)
}


def grille_vide():
    """Retourne une grille de 9 cases vides."""
    return [" "] * 9


def afficher_grille(grille):
    """Affiche la grille 3x3 avec les indices des cases vides pour aider le joueur."""
    print()
    for ligne in range(3):
        cases = []
        for col in range(3):
            i = ligne * 3 + col
            cases.append(grille[i] if grille[i] != " " else str(i + 1))
        print(f" {cases[0]} | {cases[1]} | {cases[2]} ")
        if ligne < 2:
            print("---+---+---")
    print()


def verifier_gagnant(grille):
    """Retourne 'X' ou 'O' si l'un des deux a gagné, sinon None."""
    for a, b, c in COMBINAISONS_GAGNANTES:
        if grille[a] != " " and grille[a] == grille[b] == grille[c]:
            return grille[a]
    return None


def grille_pleine(grille):
    """True si toutes les cases sont occupées."""
    return " " not in grille


def coups_possibles(grille):
    """Retourne la liste des indices de cases vides."""
    return [i for i, case in enumerate(grille) if case == " "]


def choisir_mode():
    """Demande au joueur le mode de jeu et retourne True si IA activée."""
    print("\nModes disponibles :")
    print("1. Deux joueurs (humain vs humain)")
    print("2. Un joueur contre l'IA")

    while True:
        choix = input("Choisis un mode (numéro) : ")
        if choix == "1":
            return False
        if choix == "2":
            return True
        print("Choix invalide, réessaie.")


def choisir_difficulte_ia():
    """Affiche les niveaux de difficulté et retourne la probabilité de coup aléatoire."""
    niveaux = list(DIFFICULTES_IA.keys())
    print("\nNiveaux de difficulté de l'IA :")
    for i, niveau in enumerate(niveaux, start=1):
        print(f"{i}. {niveau.capitalize()}")

    while True:
        choix = input("Choisis une difficulté (numéro) : ")
        if choix.isdigit() and 1 <= int(choix) <= len(niveaux):
            return DIFFICULTES_IA[niveaux[int(choix) - 1]]
        print("Choix invalide, réessaie.")


def demander_coup(grille):
    """Demande au joueur humain un numéro de case (1-9) et retourne son indice (0-8)."""
    while True:
        choix = input("Choisis une case (1-9) : ")
        if choix.isdigit() and 1 <= int(choix) <= 9:
            index = int(choix) - 1
            if grille[index] == " ":
                return index
            print("Cette case est déjà occupée.")
        else:
            print("Entrée invalide, choisis un numéro entre 1 et 9.")


def minimax(grille, joueur_courant, joueur_ia, joueur_humain):
    """
    Explore récursivement tous les coups possibles et retourne le score
    de la position pour l'IA : +1 si l'IA gagne, -1 si elle perd, 0 si nul.
    Suppose que chaque joueur joue le meilleur coup possible.
    """
    gagnant = verifier_gagnant(grille)
    if gagnant == joueur_ia:
        return 1
    if gagnant == joueur_humain:
        return -1
    if grille_pleine(grille):
        return 0

    scores = []
    for coup in coups_possibles(grille):
        grille[coup] = joueur_courant
        prochain_joueur = joueur_humain if joueur_courant == joueur_ia else joueur_ia
        scores.append(minimax(grille, prochain_joueur, joueur_ia, joueur_humain))
        grille[coup] = " "  # on annule le coup après l'avoir exploré

    return max(scores) if joueur_courant == joueur_ia else min(scores)


def meilleur_coup_ia(grille, joueur_ia, joueur_humain):
    """Retourne l'indice du meilleur coup pour l'IA, selon minimax."""
    meilleur_score = float("-inf")
    meilleur_coup = None

    for coup in coups_possibles(grille):
        grille[coup] = joueur_ia
        score = minimax(grille, joueur_humain, joueur_ia, joueur_humain)
        grille[coup] = " "

        if score > meilleur_score:
            meilleur_score = score
            meilleur_coup = coup

    return meilleur_coup


def choisir_coup_ia(grille, joueur_ia, joueur_humain, proba_aleatoire):
    """
    Retourne le coup joué par l'IA : soit aléatoire (avec probabilité
    proba_aleatoire), soit le meilleur coup calculé par minimax sinon.
    """
    if random.random() < proba_aleatoire:
        return random.choice(coups_possibles(grille))
    return meilleur_coup_ia(grille, joueur_ia, joueur_humain)


def jouer_morpion():
    """Lance une partie complète de morpion."""
    print("=== MORPION ===")
    contre_ia = choisir_mode()
    proba_aleatoire = choisir_difficulte_ia() if contre_ia else 0.0

    grille = grille_vide()
    joueurs = ["X", "O"]
    tour = 0

    # En mode IA, le joueur humain est toujours X, l'IA est O.
    joueur_ia = "O"
    joueur_humain = "X"

    afficher_grille(grille)

    while True:
        symbole = joueurs[tour % 2]

        if contre_ia and symbole == joueur_ia:
            print("L'IA réfléchit...")
            index = choisir_coup_ia(grille, joueur_ia, joueur_humain, proba_aleatoire)
        else:
            print(f"Tour de {symbole}")
            index = demander_coup(grille)

        grille[index] = symbole
        afficher_grille(grille)

        gagnant = verifier_gagnant(grille)
        if gagnant:
            if contre_ia and gagnant == joueur_ia:
                print("🤖 L'IA a gagné !")
            else:
                print(f"🎉 {gagnant} a gagné !")
            return

        if grille_pleine(grille):
            print("🤝 Match nul !")
            return

        tour += 1


if __name__ == "__main__":
    jouer_morpion()