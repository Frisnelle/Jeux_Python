"""
Version graphique (Tkinter) de l'anagramme, intégrée au hub à fenêtre
unique : choix de catégorie -> choix de difficulté -> écran de jeu.
Inclut un bouton Abandonner pendant la partie, un bouton Rejouer une
fois la partie finie, et l'enregistrement du résultat dans le score.
"""

import os
import random
import sys
import time
import tkinter as tk

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from mots import MOTS

from style import (
    COULEUR_FOND, COULEUR_TITRE, COULEUR_SECONDAIRE,
    COULEUR_SUCCES, COULEUR_ERREUR, POLICE_MONO,
    bouton, bouton_secondaire, bouton_retour,
)
from ecran_choix import FrameChoix
from score import enregistrer_resultat

DIFFICULTES = {
    "Facile":    {"duree": 45, "min_longueur": 4,  "max_longueur": 6},
    "Moyen":     {"duree": 30, "min_longueur": 7,  "max_longueur": 9},
    "Difficile": {"duree": 20, "min_longueur": 10, "max_longueur": 99},
}


def choisir_mot(categorie, min_longueur, max_longueur):
    mots_categorie = MOTS[categorie]
    mots_filtres = [m for m in mots_categorie if min_longueur <= len(m) <= max_longueur]
    if not mots_filtres:
        mots_filtres = mots_categorie
    return random.choice(mots_filtres)


def melanger_mot(mot):
    lettres = list(mot)
    melange = mot
    while melange == mot:
        random.shuffle(lettres)
        melange = "".join(lettres)
    return melange


def demarrer_anagramme(app):
    """Point d'entrée depuis le menu : première étape, le choix de la catégorie."""
    options = [(cat.capitalize(), cat) for cat in MOTS.keys()]
    app.afficher_frame(
        FrameChoix, titre="Choisis une catégorie", options=options,
        on_choix=lambda cat: demarrer_difficulte(app, cat), colonnes=2,
    )


def demarrer_difficulte(app, categorie):
    options = [(f"{niveau} ({p['duree']}s)", (niveau, p)) for niveau, p in DIFFICULTES.items()]
    app.afficher_frame(
        FrameChoix, titre="Choisis la difficulté", options=options,
        on_choix=lambda choix: app.afficher_frame(
            FrameAnagrammeJeu, categorie=categorie, params=choix[1]
        ),
    )


class FrameAnagrammeJeu(tk.Frame):
    def __init__(self, parent, app, categorie, params):
        super().__init__(parent, bg=COULEUR_FOND)
        self.app = app
        self.categorie = categorie
        self.params = params
        self.duree = params["duree"]
        self.mot = choisir_mot(categorie, params["min_longueur"], params["max_longueur"])
        self.melange = melanger_mot(self.mot)
        self.temps_debut = time.time()
        self.partie_terminee = False

        tk.Label(
            self, text=f"Catégorie : {categorie.capitalize()}",
            font=("Segoe UI", 16, "bold"), bg=COULEUR_FOND, fg=COULEUR_TITRE,
        ).pack(pady=(40, 5))

        self.label_chrono = tk.Label(
            self, text="", font=("Segoe UI", 15, "bold"),
            bg=COULEUR_FOND, fg=COULEUR_SUCCES,
        )
        self.label_chrono.pack(pady=(0, 15))

        tk.Label(
            self, text=self.melange, font=POLICE_MONO,
            bg=COULEUR_SECONDAIRE, fg=COULEUR_TITRE, width=14, pady=15,
        ).pack(pady=10)

        self.champ_reponse = tk.Entry(self, font=("Segoe UI", 16), justify="center", width=18)
        self.champ_reponse.pack(pady=15)
        self.champ_reponse.bind("<Return>", lambda e: self.valider())
        self.champ_reponse.focus()

        # Boutons actifs pendant la partie : Valider / Abandonner
        self.conteneur_jeu = tk.Frame(self, bg=COULEUR_FOND)
        self.conteneur_jeu.pack(pady=5)
        bouton(self.conteneur_jeu, "Valider", self.valider, largeur=12, hauteur=1).grid(row=0, column=0, padx=5)
        bouton_secondaire(self.conteneur_jeu, "Abandonner", self.abandonner, largeur=12).grid(row=0, column=1, padx=5)

        self.label_resultat = tk.Label(
            self, text="", font=("Segoe UI", 13, "bold"),
            bg=COULEUR_FOND, fg=COULEUR_TITRE,
        )
        self.label_resultat.pack(pady=15)

        # Boutons affichés seulement une fois la partie finie
        self.conteneur_fin = tk.Frame(self, bg=COULEUR_FOND)

        bouton_retour(self, app.afficher_menu).pack(side="bottom", pady=20)

        self.maj_chrono()

    def maj_chrono(self):
        if self.partie_terminee:
            return
        temps_restant = self.duree - (time.time() - self.temps_debut)
        if temps_restant <= 0:
            self.terminer(gagne=False, temps_ecoule=True)
            return
        couleur = COULEUR_ERREUR if temps_restant <= 5 else COULEUR_SUCCES
        self.label_chrono.config(text=f"⏱ {temps_restant:4.1f}s", fg=couleur)
        self.after(100, self.maj_chrono)

    def valider(self):
        if self.partie_terminee:
            return
        reponse = self.champ_reponse.get().strip().upper()
        self.terminer(gagne=(reponse == self.mot), temps_ecoule=False)

    def abandonner(self):
        if self.partie_terminee:
            return
        self.partie_terminee = True
        enregistrer_resultat("anagramme", "defaites")
        self.app.afficher_menu()

    def terminer(self, gagne, temps_ecoule, abandon=False):
        self.partie_terminee = True
        self.champ_reponse.config(state="disabled")
        self.conteneur_jeu.pack_forget()

        if abandon:
            texte, couleur = f"🚩 Partie abandonnée. Le mot était : {self.mot}", COULEUR_ERREUR
        elif temps_ecoule:
            texte, couleur = f"⏰ Temps écoulé ! Le mot était : {self.mot}", COULEUR_ERREUR
        elif gagne:
            texte, couleur = f"🎉 Bravo, c'était {self.mot} !", COULEUR_SUCCES
        else:
            texte, couleur = f"❌ Raté, le mot était : {self.mot}", COULEUR_ERREUR

        self.label_chrono.config(text="")
        self.label_resultat.config(text=texte, fg=couleur)

        enregistrer_resultat("anagramme", "victoires" if gagne else "defaites")

        self.conteneur_fin.pack(pady=5)
        bouton(self.conteneur_fin, "🔁 Rejouer", self.rejouer, largeur=14, hauteur=1).pack()

    def rejouer(self):
        self.app.afficher_frame(FrameAnagrammeJeu, categorie=self.categorie, params=self.params)


if __name__ == "__main__":
    from app import App
    App().mainloop()