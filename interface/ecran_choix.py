"""
Écran générique de sélection (catégorie, difficulté, mode de jeu...).
Affiche un titre et une grille de boutons ; cliquer sur une option
appelle le callback fourni avec la valeur associée à ce bouton.

Réutilisé par les jeux pour éviter de dupliquer ce code partout.
"""

import tkinter as tk

from style import COULEUR_FOND, COULEUR_TITRE, POLICE_TITRE, bouton_secondaire, bouton_retour


class FrameChoix(tk.Frame):
    """
    options : liste de tuples (texte_affiché, valeur)
    on_choix : fonction appelée avec la valeur du bouton cliqué
    colonnes : nombre de boutons par ligne dans la grille
    """

    def __init__(self, parent, app, titre, options, on_choix, colonnes=1):
        super().__init__(parent, bg=COULEUR_FOND)
        self.app = app

        tk.Label(
            self, text=titre, font=POLICE_TITRE,
            bg=COULEUR_FOND, fg=COULEUR_TITRE,
        ).pack(pady=(60, 30))

        grille = tk.Frame(self, bg=COULEUR_FOND)
        grille.pack()

        for i, (texte, valeur) in enumerate(options):
            b = bouton_secondaire(grille, texte, lambda v=valeur: on_choix(v))
            b.grid(row=i // colonnes, column=i % colonnes, padx=6, pady=6)

        bouton_retour(self, app.afficher_menu).pack(side="bottom", pady=20)