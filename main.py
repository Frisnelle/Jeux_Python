"""
Point d'entrée du hub de jeux.
Affiche un menu pour choisir le jeu auquel jouer.
"""

from anagramme import jouer_anagramme
from pendu import jouer_pendu

JEUX = {
    "1": ("Anagramme chronométré", jouer_anagramme),
    "2": ("Pendu", jouer_pendu),
}


def afficher_menu():
    print("\n=== HUB DE JEUX ===")
    for cle, (nom, _) in JEUX.items():
        print(f"{cle}. {nom}")
    print("0. Quitter")


def main():
    while True:
        afficher_menu()
        choix = input("Choisis un jeu (numéro) : ").strip()

        if choix == "0":
            print("À bientôt !")
            break

        if choix in JEUX:
            _, fonction_jeu = JEUX[choix]
            fonction_jeu()
        else:
            print("Choix invalide, réessaie.")


if __name__ == "__main__":
    main()