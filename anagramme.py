"""
Jeu d'anagramme chronométré.

L'ordinateur choisit un mot dans une catégorie donnée par le joueur,
mélange ses lettres, et le joueur doit retrouver le mot original
avant la fin du temps imparti. Le chrono tourne en temps réel,
pendant que le joueur tape sa réponse.
"""

import random
import sys
import time

import msvcrt  # lecture clavier en temps réel (Windows uniquement)

from mots import MOTS

DIFFICULTES = {
    "facile":    {"duree": 45, "min_longueur": 4,  "max_longueur": 6},
    "moyen":     {"duree": 30, "min_longueur": 7,  "max_longueur": 9},
    "difficile": {"duree": 20, "min_longueur": 10, "max_longueur": 99},
}


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
    niveaux = list(DIFFICULTES.keys())
    print("\nNiveaux de difficulté :")
    for i, niveau in enumerate(niveaux, start=1):
        params = DIFFICULTES[niveau]
        print(f"{i}. {niveau.capitalize()} ({params['duree']}s)")

    while True:
        choix = input("Choisis une difficulté (numéro) : ")
        if choix.isdigit() and 1 <= int(choix) <= len(niveaux):
            return DIFFICULTES[niveaux[int(choix) - 1]]
        print("Choix invalide, réessaie.")


def choisir_mot(categorie, min_longueur, max_longueur):
    """
    Tire un mot au hasard dans la catégorie donnée, dont la longueur
    est comprise entre min_longueur et max_longueur.

    Si aucun mot de la catégorie ne correspond à cette fourchette,
    on se rabat sur l'ensemble des mots de la catégorie plutôt que
    de planter.
    """
    mots_categorie = MOTS[categorie]
    mots_filtres = [
        m for m in mots_categorie if min_longueur <= len(m) <= max_longueur
    ]

    if not mots_filtres:
        mots_filtres = mots_categorie  # repli si la fourchette est trop stricte

    return random.choice(mots_filtres)


def melanger_mot(mot):
    """Mélange les lettres d'un mot jusqu'à obtenir un résultat différent de l'original."""
    lettres = list(mot)
    melange = mot
    while melange == mot:
        random.shuffle(lettres)
        melange = "".join(lettres)
    return melange


def saisie_chronometree(duree):
    """
    Lit la saisie du joueur caractère par caractère, en temps réel,
    en affichant le temps restant en direct sur la même ligne.

    Retourne le texte tapé si le joueur appuie sur Entrée à temps,
    ou None si le temps est écoulé avant validation.
    """
    debut = time.time()
    reponse = ""

    while True:
        temps_restant = duree - (time.time() - debut)
        if temps_restant <= 0:
            print()
            return None

        sys.stdout.write(f"\r⏱  {temps_restant:4.1f}s | Ta réponse : {reponse:<20}")
        sys.stdout.flush()

        if msvcrt.kbhit():
            char = msvcrt.getwch()
            if char == "\r":
                print()
                return reponse
            elif char == "\b":
                reponse = reponse[:-1]
            elif char.isalpha():
                reponse += char.upper()

        time.sleep(0.05)


def jouer_anagramme():
    """Lance une partie complète du jeu d'anagramme."""
    print("=== JEU D'ANAGRAMME ===")
    categorie = choisir_categorie()
    params = choisir_difficulte()

    mot = choisir_mot(categorie, params["min_longueur"], params["max_longueur"])
    melange = melanger_mot(mot)

    print(f"\nCatégorie : {categorie.capitalize()}")
    print(f"Lettres mélangées : {melange}")
    print(f"Tu as {params['duree']} secondes. Tape ta réponse puis Entrée.\n")

    reponse = saisie_chronometree(params["duree"])

    if reponse is None:
        print(f"⏰ Temps écoulé ! Le mot était : {mot}")
    elif reponse.upper() == mot:
        print(f"🎉 Bravo, c'était bien {mot} !")
    else:
        print(f"❌ Raté, tu as répondu {reponse}, le mot était : {mot}")


if __name__ == "__main__":
    jouer_anagramme()