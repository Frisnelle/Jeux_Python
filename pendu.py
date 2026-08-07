"""
Jeu du pendu.

Un mot secret est choisi dans une catégorie donnée par le joueur.
Le joueur propose des lettres une par une. Chaque lettre absente
du mot fait perdre un essai. Le joueur gagne s'il découvre toutes
les lettres avant d'épuiser ses essais.
"""

import random

from mots import MOTS

DIFFICULTES_PENDU = {
    "facile":    {"essais": 8, "min_longueur": 4,  "max_longueur": 6},
    "moyen":     {"essais": 6, "min_longueur": 7,  "max_longueur": 9},
    "difficile": {"essais": 4, "min_longueur": 10, "max_longueur": 99},
}

# Dessins ASCII du pendu, du moins avancé (0 erreur) au plus avancé (pendu complet)
DESSINS_PENDU = [
    """
       ------
       |    |
       |
       |
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |    |
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   /
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |  (X)
    ---------
    """,
]


def choisir_categorie():
    """Affiche les catégories disponibles et retourne le choix du joueur."""
    categories = list(MOTS.keys())
    print("\nCatégories disponibles :")
    for i, cat in enumerate(categories, start=1):
        print(f"{i}. {cat.capitalize()}")

    while True:
        choix = input("Choisis une catégorie (numéro) : ")
        if choix.isdigit() and 1 <= int(choix) <= len(categories):
            return categories[int(choix) - 1]
        print("Choix invalide, réessaie.")


def choisir_difficulte():
    """Affiche les niveaux de difficulté et retourne les paramètres associés."""
    niveaux = list(DIFFICULTES_PENDU.keys())
    print("\nNiveaux de difficulté :")
    for i, niveau in enumerate(niveaux, start=1):
        params = DIFFICULTES_PENDU[niveau]
        print(f"{i}. {niveau.capitalize()} ({params['essais']} essais)")

    while True:
        choix = input("Choisis une difficulté (numéro) : ")
        if choix.isdigit() and 1 <= int(choix) <= len(niveaux):
            return DIFFICULTES_PENDU[niveaux[int(choix) - 1]]
        print("Choix invalide, réessaie.")


def choisir_mot(categorie, min_longueur, max_longueur):
    """Tire un mot au hasard dans la catégorie, filtré par longueur (avec repli si vide)."""
    mots_categorie = MOTS[categorie]
    mots_filtres = [
        m for m in mots_categorie if min_longueur <= len(m) <= max_longueur
    ]
    if not mots_filtres:
        mots_filtres = mots_categorie
    return random.choice(mots_filtres)


def afficher_mot_masque(mot, lettres_trouvees):
    """Retourne le mot avec les lettres non trouvées remplacées par des underscores."""
    return " ".join(l if l in lettres_trouvees else "_" for l in mot)


def afficher_pendu(nb_erreurs, max_erreurs):
    """Affiche le dessin ASCII correspondant au nombre d'erreurs actuel."""
    index = min(nb_erreurs, len(DESSINS_PENDU) - 1)
    print(DESSINS_PENDU[index])


def jouer_pendu():
    """Lance une partie complète du jeu du pendu."""
    print("=== JEU DU PENDU ===")
    categorie = choisir_categorie()
    params = choisir_difficulte()

    mot = choisir_mot(categorie, params["min_longueur"], params["max_longueur"])
    max_essais = params["essais"]

    # On calibre le nombre de dessins disponibles sur le nombre d'essais du niveau,
    # pour que le dessin final coïncide avec la dernière erreur autorisée.
    pas_dessin = (len(DESSINS_PENDU) - 1) / max_essais

    lettres_trouvees = set()
    lettres_tentees = set()
    nb_erreurs = 0

    print(f"\nCatégorie : {categorie.capitalize()}")
    print(f"Le mot fait {len(mot)} lettres. Tu as {max_essais} essais.\n")

    while nb_erreurs < max_essais:
        index_dessin = round(nb_erreurs * pas_dessin)
        print(DESSINS_PENDU[min(index_dessin, len(DESSINS_PENDU) - 1)])
        print(f"Mot : {afficher_mot_masque(mot, lettres_trouvees)}")
        print(f"Lettres essayées : {', '.join(sorted(lettres_tentees)) or '(aucune)'}")
        print(f"Essais restants : {max_essais - nb_erreurs}")

        lettre = input("Propose une lettre : ").upper().strip()

        if len(lettre) != 1 or not lettre.isalpha():
            print("⚠️  Entre une seule lettre valide.\n")
            continue

        if lettre in lettres_tentees:
            print("Tu as déjà essayé cette lettre.\n")
            continue

        lettres_tentees.add(lettre)

        if lettre in mot:
            lettres_trouvees.add(lettre)
            print(f"✅ Bien joué, {lettre} est dans le mot !\n")
            if all(l in lettres_trouvees for l in mot):
                print(f"🎉 Gagné ! Le mot était : {mot}")
                return
        else:
            nb_erreurs += 1
            print(f"❌ Raté, {lettre} n'est pas dans le mot.\n")

    print(DESSINS_PENDU[-1])
    print(f"💀 Perdu ! Le mot était : {mot}")


if __name__ == "__main__":
    jouer_pendu()