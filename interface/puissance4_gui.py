"""
Version graphique (Tkinter) du Puissance 4, intégrée au hub à fenêtre unique.
Le plateau est dessiné sur un Canvas : un clic dans une colonne y dépose
un jeton. Inclut un highlight de l'alignement gagnant, un bouton
Abandonner, et l'enregistrement du score en mode contre l'IA.
"""

import os
import sys
import tkinter as tk

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from puissance4 import (
    NB_LIGNES, NB_COLONNES, JOUEUR_1, JOUEUR_2, DIFFICULTES_IA,
    grille_vide, colonnes_jouables, jouer_colonne, trouver_alignement,
    verifier_gagnant, grille_pleine, choisir_coup_ia,
)

from style import (
    COULEUR_FOND, COULEUR_TITRE, COULEUR_SECONDAIRE,
    COULEUR_ERREUR, COULEUR_ACCENT, COULEUR_GAGNANT,
    bouton, bouton_secondaire, bouton_retour,
)
from ecran_choix import FrameChoix
from score import enregistrer_resultat

COULEUR_PLATEAU = "#313244"
COULEUR_TROU = "#1e1e2e"
COULEUR_SURVOL = "#45475a"
TAILLE_CASE = 52
MARGE = 12
RAYON = 20


def demarrer_puissance4(app):
    options = [("👥 Deux joueurs", False), ("🤖 Contre l'IA", True)]
    app.afficher_frame(
        FrameChoix, titre="Choisis un mode", options=options,
        on_choix=lambda contre_ia: (
            demarrer_difficulte(app) if contre_ia
            else app.afficher_frame(FramePuissance4Jeu, contre_ia=False, params_ia=None)
        ),
    )


def demarrer_difficulte(app):
    options = [(niveau.capitalize(), params) for niveau, params in DIFFICULTES_IA.items()]
    app.afficher_frame(
        FrameChoix, titre="Choisis la difficulté", options=options,
        on_choix=lambda params: app.afficher_frame(
            FramePuissance4Jeu, contre_ia=True, params_ia=params
        ),
    )


class FramePuissance4Jeu(tk.Frame):
    def __init__(self, parent, app, contre_ia, params_ia):
        super().__init__(parent, bg=COULEUR_FOND)
        self.app = app
        self.contre_ia = contre_ia
        self.params_ia = params_ia
        self.joueur_ia = JOUEUR_2
        self.joueur_humain = JOUEUR_1
        self.joueurs = [JOUEUR_1, JOUEUR_2]
        self.tour = 0
        self.grille = grille_vide()
        self.partie_terminee = False
        self.colonne_survolee = None
        self.cases_gagnantes = set()

        self.label_tour = tk.Label(
            self, text=self._texte_tour(), font=("Segoe UI", 17, "bold"),
            bg=COULEUR_FOND, fg=COULEUR_TITRE,
        )
        self.label_tour.pack(pady=(18, 8))

        largeur = MARGE * 2 + TAILLE_CASE * NB_COLONNES
        hauteur = MARGE * 2 + TAILLE_CASE * NB_LIGNES
        self.canvas = tk.Canvas(
            self, width=largeur, height=hauteur,
            bg=COULEUR_PLATEAU, highlightthickness=0,
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._clic)
        self.canvas.bind("<Motion>", self._survol)
        self.canvas.bind("<Leave>", self._quitter_survol)

        self.conteneur_actions = tk.Frame(self, bg=COULEUR_FOND)
        self.conteneur_actions.pack(pady=(12, 4))
        bouton(self.conteneur_actions, "🔁 Nouvelle partie", self.recommencer, largeur=16, hauteur=1).grid(row=0, column=0, padx=4)
        bouton_secondaire(self.conteneur_actions, "Abandonner", self.abandonner, largeur=12).grid(row=0, column=1, padx=4)

        bouton_retour(self, app.afficher_menu).pack(side="bottom", pady=12)

        self._dessiner()

    def _texte_tour(self):
        symbole = self.joueurs[self.tour % 2]
        if self.contre_ia and symbole == self.joueur_ia:
            return "Tour de l'IA..."
        nom = "Rouge" if symbole == JOUEUR_1 else "Jaune"
        return f"Tour de {nom}"

    def _couleur_jeton(self, symbole, gagnant=False):
        if gagnant:
            return COULEUR_GAGNANT
        if symbole == JOUEUR_1:
            return COULEUR_ERREUR
        if symbole == JOUEUR_2:
            return COULEUR_ACCENT
        return COULEUR_TROU

    def _dessiner(self):
        self.canvas.delete("all")
        for ligne in range(NB_LIGNES):
            for col in range(NB_COLONNES):
                cx = MARGE + col * TAILLE_CASE + TAILLE_CASE // 2
                cy = MARGE + ligne * TAILLE_CASE + TAILLE_CASE // 2
                fond = COULEUR_SURVOL if col == self.colonne_survolee and not self.partie_terminee else COULEUR_PLATEAU
                self.canvas.create_rectangle(
                    MARGE + col * TAILLE_CASE,
                    MARGE + ligne * TAILLE_CASE,
                    MARGE + (col + 1) * TAILLE_CASE,
                    MARGE + (ligne + 1) * TAILLE_CASE,
                    fill=fond, outline=fond,
                )
                symbole = self.grille[ligne][col]
                gagnant = (ligne, col) in self.cases_gagnantes
                couleur = self._couleur_jeton(symbole, gagnant=gagnant) if symbole != " " else COULEUR_TROU
                self.canvas.create_oval(
                    cx - RAYON, cy - RAYON, cx + RAYON, cy + RAYON,
                    fill=couleur, outline=couleur,
                )

    def _colonne_depuis_x(self, x):
        col = (x - MARGE) // TAILLE_CASE
        if 0 <= col < NB_COLONNES:
            return int(col)
        return None

    def _survol(self, event):
        if self.partie_terminee:
            return
        col = self._colonne_depuis_x(event.x)
        if col != self.colonne_survolee:
            self.colonne_survolee = col
            self._dessiner()

    def _quitter_survol(self, _event):
        self.colonne_survolee = None
        self._dessiner()

    def _clic(self, event):
        if self.partie_terminee:
            return
        symbole = self.joueurs[self.tour % 2]
        if self.contre_ia and symbole == self.joueur_ia:
            return
        col = self._colonne_depuis_x(event.x)
        if col is None or col not in colonnes_jouables(self.grille):
            return
        self._jouer(col)

    def _jouer(self, col):
        symbole = self.joueurs[self.tour % 2]
        jouer_colonne(self.grille, col, symbole)
        self._dessiner()
        if self._verifier_fin():
            return
        self.tour += 1
        self.label_tour.config(text=self._texte_tour())
        suivant = self.joueurs[self.tour % 2]
        if self.contre_ia and suivant == self.joueur_ia and not self.partie_terminee:
            self.after(350, self.jouer_coup_ia)

    def jouer_coup_ia(self):
        if self.partie_terminee or not self.winfo_exists():
            return
        col = choisir_coup_ia(self.grille, self.joueur_ia, self.joueur_humain, self.params_ia)
        self._jouer(col)

    def abandonner(self):
        if self.partie_terminee:
            return
        self.partie_terminee = True
        if self.contre_ia:
            enregistrer_resultat("puissance4", "defaites")
        self.app.afficher_menu()

    def _verifier_fin(self):
        alignement = trouver_alignement(self.grille)
        if alignement:
            self.partie_terminee = True
            self.cases_gagnantes = set(alignement)
            gagnant = verifier_gagnant(self.grille)
            if self.contre_ia and gagnant == self.joueur_ia:
                self.label_tour.config(text="🤖 L'IA a gagné !")
                enregistrer_resultat("puissance4", "defaites")
            else:
                nom = "Rouge" if gagnant == JOUEUR_1 else "Jaune"
                self.label_tour.config(text=f"🎉 {nom} a gagné !")
                if self.contre_ia:
                    enregistrer_resultat("puissance4", "victoires")
            self._dessiner()
            return True

        if grille_pleine(self.grille):
            self.partie_terminee = True
            self.label_tour.config(text="🤝 Match nul !")
            if self.contre_ia:
                enregistrer_resultat("puissance4", "nuls")
            return True

        return False

    def recommencer(self):
        self.grille = grille_vide()
        self.tour = 0
        self.partie_terminee = False
        self.cases_gagnantes = set()
        self.label_tour.config(text=self._texte_tour())
        self._dessiner()


if __name__ == "__main__":
    from app import App
    App().mainloop()
