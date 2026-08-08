"""
Version graphique (Tkinter) du morpion, intégrée au hub à fenêtre unique.
"""

import random
import tkinter as tk

from style import (
    COULEUR_FOND, COULEUR_TITRE, COULEUR_SECONDAIRE, COULEUR_SECONDAIRE_SURVOL,
    COULEUR_ERREUR, COULEUR_ACCENT, bouton, bouton_retour,
)
from ecran_choix import FrameChoix

COMBINAISONS_GAGNANTES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]

DIFFICULTES_IA = {
    "Facile": 0.6,
    "Moyen": 0.3,
    "Difficile": 0.1,
    "Impossible": 0.0,
}


def verifier_gagnant(grille):
    for a, b, c in COMBINAISONS_GAGNANTES:
        if grille[a] != " " and grille[a] == grille[b] == grille[c]:
            return grille[a]
    return None


def grille_pleine(grille):
    return " " not in grille


def coups_possibles(grille):
    return [i for i, case in enumerate(grille) if case == " "]


def minimax(grille, joueur_courant, joueur_ia, joueur_humain):
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
        prochain = joueur_humain if joueur_courant == joueur_ia else joueur_ia
        scores.append(minimax(grille, prochain, joueur_ia, joueur_humain))
        grille[coup] = " "
    return max(scores) if joueur_courant == joueur_ia else min(scores)


def meilleur_coup_ia(grille, joueur_ia, joueur_humain):
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
    if random.random() < proba_aleatoire:
        return random.choice(coups_possibles(grille))
    return meilleur_coup_ia(grille, joueur_ia, joueur_humain)


def demarrer_morpion(app):
    """Point d'entrée : choix du mode (2 joueurs ou contre l'IA)."""
    options = [("👥 Deux joueurs", False), ("🤖 Contre l'IA", True)]
    app.afficher_frame(
        FrameChoix, titre="Choisis un mode", options=options,
        on_choix=lambda contre_ia: (
            demarrer_difficulte(app) if contre_ia
            else app.afficher_frame(FrameMorpionJeu, contre_ia=False, proba_aleatoire=0.0)
        ),
    )


def demarrer_difficulte(app):
    options = [(niveau, proba) for niveau, proba in DIFFICULTES_IA.items()]
    app.afficher_frame(
        FrameChoix, titre="Choisis la difficulté", options=options,
        on_choix=lambda proba: app.afficher_frame(
            FrameMorpionJeu, contre_ia=True, proba_aleatoire=proba
        ),
    )


class FrameMorpionJeu(tk.Frame):
    def __init__(self, parent, app, contre_ia, proba_aleatoire):
        super().__init__(parent, bg=COULEUR_FOND)
        self.app = app
        self.contre_ia = contre_ia
        self.proba_aleatoire = proba_aleatoire
        self.joueur_ia = "O"
        self.joueur_humain = "X"
        self.joueurs = ["X", "O"]
        self.tour = 0
        self.grille = [" "] * 9
        self.partie_terminee = False
        self.boutons = []

        self.label_tour = tk.Label(
            self, text=self._texte_tour(), font=("Segoe UI", 17, "bold"),
            bg=COULEUR_FOND, fg=COULEUR_TITRE,
        )
        self.label_tour.pack(pady=(40, 15))

        conteneur_grille = tk.Frame(self, bg=COULEUR_FOND)
        conteneur_grille.pack(pady=5)

        for i in range(9):
            b = tk.Button(
                conteneur_grille, text=" ", font=("Segoe UI", 28, "bold"),
                width=4, height=2, bg=COULEUR_SECONDAIRE,
                activebackground=COULEUR_SECONDAIRE_SURVOL, relief="flat", bd=0,
                command=lambda i=i: self.jouer_case(i),
            )
            b.grid(row=i // 3, column=i % 3, padx=4, pady=4)
            self.boutons.append(b)

        bouton(self, "🔁 Nouvelle partie", self.recommencer, largeur=18, hauteur=1).pack(pady=(15, 5))
        bouton_retour(self, app.afficher_menu).pack(side="bottom", pady=15)

    def _texte_tour(self):
        symbole = self.joueurs[self.tour % 2]
        if self.contre_ia and symbole == self.joueur_ia:
            return "Tour de l'IA..."
        return f"Tour de {symbole}"

    def jouer_case(self, index):
        if self.partie_terminee or self.grille[index] != " ":
            return
        symbole = self.joueurs[self.tour % 2]
        if self.contre_ia and symbole == self.joueur_ia:
            return
        self._placer(index, symbole)
        if self._verifier_fin():
            return
        self.tour += 1
        self.label_tour.config(text=self._texte_tour())
        suivant = self.joueurs[self.tour % 2]
        if self.contre_ia and suivant == self.joueur_ia and not self.partie_terminee:
            self.after(400, self.jouer_coup_ia)

    def jouer_coup_ia(self):
        index = choisir_coup_ia(self.grille, self.joueur_ia, self.joueur_humain, self.proba_aleatoire)
        self._placer(index, self.joueur_ia)
        if self._verifier_fin():
            return
        self.tour += 1
        self.label_tour.config(text=self._texte_tour())

    def _placer(self, index, symbole):
        self.grille[index] = symbole
        couleur = COULEUR_ERREUR if symbole == "X" else COULEUR_ACCENT
        self.boutons[index].config(text=symbole, fg=couleur, state="disabled")

    def _verifier_fin(self):
        gagnant = verifier_gagnant(self.grille)
        if gagnant:
            self.partie_terminee = True
            if self.contre_ia and gagnant == self.joueur_ia:
                self.label_tour.config(text="🤖 L'IA a gagné !")
            else:
                self.label_tour.config(text=f"🎉 {gagnant} a gagné !")
            self._desactiver_tout()
            return True
        if grille_pleine(self.grille):
            self.partie_terminee = True
            self.label_tour.config(text="🤝 Match nul !")
            return True
        return False

    def _desactiver_tout(self):
        for b in self.boutons:
            b.config(state="disabled")

    def recommencer(self):
        self.grille = [" "] * 9
        self.tour = 0
        self.partie_terminee = False
        for b in self.boutons:
            b.config(text=" ", state="normal")
        self.label_tour.config(text=self._texte_tour())


if __name__ == "__main__":
    from app import App
    App().mainloop()