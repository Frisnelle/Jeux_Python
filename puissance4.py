"""
Jeu de Puissance 4.

Grille 6x7 : chaque joueur dépose un jeton dans une colonne, le jeton
tombe en bas. Le premier à aligner 4 jetons (ligne, colonne, diagonale)
gagne. Mode 2 joueurs humains, ou 1 joueur contre une IA (minimax
avec élagage alpha-bêta et profondeur limitée).
"""

import random

NB_LIGNES = 6
NB_COLONNES = 7
ALIGNEMENT = 4

JOUEUR_1 = "R"
JOUEUR_2 = "J"

# Profondeur de recherche + probabilité de jouer un coup aléatoire
DIFFICULTES_IA = {
    "facile":     {"profondeur": 1, "proba_aleatoire": 0.55},
    "moyen":      {"profondeur": 2, "proba_aleatoire": 0.30},
    "difficile":  {"profondeur": 3, "proba_aleatoire": 0.10},
    "impossible": {"profondeur": 4, "proba_aleatoire": 0.00},
}

DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))


def grille_vide():
    """Retourne une grille 6x7 vide (ligne 0 = haut du plateau)."""
    return [[" " for _ in range(NB_COLONNES)] for _ in range(NB_LIGNES)]


def colonnes_jouables(grille):
    """Colonnes dont la case du haut est encore libre."""
    return [c for c in range(NB_COLONNES) if grille[0][c] == " "]


def jouer_colonne(grille, col, symbole):
    """Place un jeton dans la colonne et retourne la ligne occupée, ou None."""
    for ligne in range(NB_LIGNES - 1, -1, -1):
        if grille[ligne][col] == " ":
            grille[ligne][col] = symbole
            return ligne
    return None


def annuler_colonne(grille, col):
    """Retire le jeton le plus haut d'une colonne (pour l'exploration IA)."""
    for ligne in range(NB_LIGNES):
        if grille[ligne][col] != " ":
            grille[ligne][col] = " "
            return


def grille_pleine(grille):
    return not colonnes_jouables(grille)


def trouver_alignement(grille):
    """Retourne les 4 cases gagnantes [(l, c), ...] ou None."""
    for ligne in range(NB_LIGNES):
        for col in range(NB_COLONNES):
            symbole = grille[ligne][col]
            if symbole == " ":
                continue
            for dl, dc in DIRECTIONS:
                cases = []
                for i in range(ALIGNEMENT):
                    l, c = ligne + i * dl, col + i * dc
                    if not (0 <= l < NB_LIGNES and 0 <= c < NB_COLONNES):
                        break
                    if grille[l][c] != symbole:
                        break
                    cases.append((l, c))
                if len(cases) == ALIGNEMENT:
                    return cases
    return None


def verifier_gagnant(grille):
    """Retourne 'R' ou 'J' s'il y a un gagnant, sinon None."""
    cases = trouver_alignement(grille)
    if cases:
        l, c = cases[0]
        return grille[l][c]
    return None


def _fenetres():
    """Toutes les fenêtres de 4 cases consécutives du plateau."""
    fenetres = []
    for ligne in range(NB_LIGNES):
        for col in range(NB_COLONNES - ALIGNEMENT + 1):
            fenetres.append([(ligne, col + i) for i in range(ALIGNEMENT)])
    for col in range(NB_COLONNES):
        for ligne in range(NB_LIGNES - ALIGNEMENT + 1):
            fenetres.append([(ligne + i, col) for i in range(ALIGNEMENT)])
    for ligne in range(NB_LIGNES - ALIGNEMENT + 1):
        for col in range(NB_COLONNES - ALIGNEMENT + 1):
            fenetres.append([(ligne + i, col + i) for i in range(ALIGNEMENT)])
    for ligne in range(ALIGNEMENT - 1, NB_LIGNES):
        for col in range(NB_COLONNES - ALIGNEMENT + 1):
            fenetres.append([(ligne - i, col + i) for i in range(ALIGNEMENT)])
    return fenetres


FENETRES = _fenetres()


def _score_fenetre(valeurs, joueur_ia, joueur_humain):
    nb_ia = valeurs.count(joueur_ia)
    nb_humain = valeurs.count(joueur_humain)
    nb_vide = valeurs.count(" ")
    if nb_ia == 4:
        return 10000
    if nb_humain == 4:
        return -10000
    if nb_ia == 3 and nb_vide == 1:
        return 50
    if nb_ia == 2 and nb_vide == 2:
        return 8
    if nb_humain == 3 and nb_vide == 1:
        return -80
    if nb_humain == 2 and nb_vide == 2:
        return -8
    return 0


def evaluer(grille, joueur_ia, joueur_humain):
    """Score heuristique d'une position du point de vue de l'IA."""
    gagnant = verifier_gagnant(grille)
    if gagnant == joueur_ia:
        return 10000
    if gagnant == joueur_humain:
        return -10000

    score = 0
    for ligne in range(NB_LIGNES):
        if grille[ligne][NB_COLONNES // 2] == joueur_ia:
            score += 3
        elif grille[ligne][NB_COLONNES // 2] == joueur_humain:
            score -= 3

    for cases in FENETRES:
        valeurs = [grille[l][c] for l, c in cases]
        score += _score_fenetre(valeurs, joueur_ia, joueur_humain)
    return score


def minimax(grille, profondeur, alpha, beta, maximise, joueur_ia, joueur_humain):
    jouables = colonnes_jouables(grille)
    gagnant = verifier_gagnant(grille)
    if profondeur == 0 or gagnant or not jouables:
        return evaluer(grille, joueur_ia, joueur_humain)

    if maximise:
        meilleur = float("-inf")
        for col in jouables:
            jouer_colonne(grille, col, joueur_ia)
            score = minimax(grille, profondeur - 1, alpha, beta, False, joueur_ia, joueur_humain)
            annuler_colonne(grille, col)
            meilleur = max(meilleur, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return meilleur

    meilleur = float("inf")
    for col in jouables:
        jouer_colonne(grille, col, joueur_humain)
        score = minimax(grille, profondeur - 1, alpha, beta, True, joueur_ia, joueur_humain)
        annuler_colonne(grille, col)
        meilleur = min(meilleur, score)
        beta = min(beta, score)
        if beta <= alpha:
            break
    return meilleur


def colonne_gagnante(grille, symbole):
    """Retourne une colonne qui fait gagner immédiatement, ou None."""
    for col in colonnes_jouables(grille):
        jouer_colonne(grille, col, symbole)
        gagne = verifier_gagnant(grille) == symbole
        annuler_colonne(grille, col)
        if gagne:
            return col
    return None


def meilleur_coup_ia(grille, joueur_ia, joueur_humain, profondeur):
    """Retourne la colonne du meilleur coup selon minimax."""
    coup_gagnant = colonne_gagnante(grille, joueur_ia)
    if coup_gagnant is not None:
        return coup_gagnant
    coup_bloquant = colonne_gagnante(grille, joueur_humain)
    if coup_bloquant is not None:
        return coup_bloquant

    meilleur_score = float("-inf")
    meilleurs_coups = []
    # On explore le centre en premier : ça accélère l'élagage.
    ordre = sorted(colonnes_jouables(grille), key=lambda c: abs(c - NB_COLONNES // 2))

    for col in ordre:
        jouer_colonne(grille, col, joueur_ia)
        score = minimax(
            grille, profondeur - 1, float("-inf"), float("inf"),
            False, joueur_ia, joueur_humain,
        )
        annuler_colonne(grille, col)
        if score > meilleur_score:
            meilleur_score = score
            meilleurs_coups = [col]
        elif score == meilleur_score:
            meilleurs_coups.append(col)

    return random.choice(meilleurs_coups) if meilleurs_coups else random.choice(colonnes_jouables(grille))


def choisir_coup_ia(grille, joueur_ia, joueur_humain, params):
    """Coup de l'IA : aléatoire avec une certaine proba, sinon minimax."""
    jouables = colonnes_jouables(grille)
    if random.random() < params["proba_aleatoire"]:
        return random.choice(jouables)
    return meilleur_coup_ia(grille, joueur_ia, joueur_humain, params["profondeur"])


def afficher_grille(grille):
    print()
    print("  " + "   ".join(str(c + 1) for c in range(NB_COLONNES)))
    print("+" + "---+" * NB_COLONNES)
    for ligne in grille:
        print("| " + " | ".join(c if c != " " else " " for c in ligne) + " |")
        print("+" + "---+" * NB_COLONNES)
    print()


def choisir_mode():
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
    niveaux = list(DIFFICULTES_IA.keys())
    print("\nNiveaux de difficulté de l'IA :")
    for i, niveau in enumerate(niveaux, start=1):
        print(f"{i}. {niveau.capitalize()}")

    while True:
        choix = input("Choisis une difficulté (numéro) : ")
        if choix.isdigit() and 1 <= int(choix) <= len(niveaux):
            return DIFFICULTES_IA[niveaux[int(choix) - 1]]
        print("Choix invalide, réessaie.")


def demander_colonne(grille):
    while True:
        choix = input(f"Choisis une colonne (1-{NB_COLONNES}) : ")
        if choix.isdigit() and 1 <= int(choix) <= NB_COLONNES:
            col = int(choix) - 1
            if col in colonnes_jouables(grille):
                return col
            print("Cette colonne est pleine.")
        else:
            print(f"Entrée invalide, choisis un numéro entre 1 et {NB_COLONNES}.")


def jouer_puissance4():
    """Lance une partie complète de Puissance 4."""
    print("=== PUISSANCE 4 ===")
    contre_ia = choisir_mode()
    params_ia = choisir_difficulte_ia() if contre_ia else None

    grille = grille_vide()
    joueurs = [JOUEUR_1, JOUEUR_2]
    tour = 0
    joueur_ia = JOUEUR_2
    joueur_humain = JOUEUR_1

    print(f"\n{JOUEUR_1} = jeton rouge, {JOUEUR_2} = jeton jaune.")
    afficher_grille(grille)

    while True:
        symbole = joueurs[tour % 2]

        if contre_ia and symbole == joueur_ia:
            print("L'IA réfléchit...")
            col = choisir_coup_ia(grille, joueur_ia, joueur_humain, params_ia)
        else:
            print(f"Tour de {symbole}")
            col = demander_colonne(grille)

        jouer_colonne(grille, col, symbole)
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
    jouer_puissance4()
