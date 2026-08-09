"""
Version graphique (Tkinter) du pendu, intégrée au hub à fenêtre unique.
Inclut un bouton Abandonner pendant la partie, un bouton Rejouer une
fois la partie finie, et l'enregistrement du résultat dans le score.
"""

import os
import random
import sys
import tkinter as tk

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from mots import MOTS

from style import (
    COULEUR_FOND, COULEUR_TITRE, COULEUR_SECONDAIRE, COULEUR_SECONDAIRE_SURVOL,
    COULEUR_SUCCES, COULEUR_ERREUR, bouton, bouton_secondaire, bouton_retour,
)
from ecran_choix import FrameChoix
from score import enregistrer_resultat

DIFFICULTES_PENDU = {
    "Facile":    {"essais": 8, "min_longueur": 4,  "max_longueur": 6},
    "Moyen":     {"essais": 6, "min_longueur": 7,  "max_longueur": 9},
    "Difficile": {"essais": 4, "min_longueur": 10, "max_longueur": 99},
}

ALPHABET = "AZERTYUIOPQSDFGHJKLMWXCVBN"  # ordre clavier AZERTY, purement esthétique


def choisir_mot(categorie, min_longueur, max_longueur):
    mots_categorie = MOTS[categorie]
    mots_filtres = [m for m in mots_categorie if min_longueur <= len(m) <= max_longueur]
    if not mots_filtres:
        mots_filtres = mots_categorie
    return random.choice(mots_filtres)


def demarrer_pendu(app):
    options = [(cat.capitalize(), cat) for cat in MOTS.keys()]
    app.afficher_frame(
        FrameChoix, titre="Choisis une catégorie", options=options,
        on_choix=lambda cat: demarrer_difficulte(app, cat), colonnes=2,
    )


def demarrer_difficulte(app, categorie):
    options = [
        (f"{niveau} ({p['essais']} essais)", (niveau, p))
        for niveau, p in DIFFICULTES_PENDU.items()
    ]
    app.afficher_frame(
        FrameChoix, titre="Choisis la difficulté", options=options,
        on_choix=lambda choix: app.afficher_frame(
            FramePenduJeu, categorie=categorie, params=choix[1]
        ),
    )


class FramePenduJeu(tk.Frame):
    def __init__(self, parent, app, categorie, params):
        super().__init__(parent, bg=COULEUR_FOND)
        self.app = app
        self.categorie = categorie
        self.params = params
        self.mot = choisir_mot(categorie, params["min_longueur"], params["max_longueur"])
        self.max_essais = params["essais"]
        self.nb_erreurs = 0
        self.lettres_trouvees = set()
        self.lettres_tentees = set()
        self.partie_terminee = False
        self.boutons_lettres = {}

        tk.Label(
            self, text=f"{categorie.capitalize()} — {len(self.mot)} lettres",
            font=("Segoe UI", 15, "bold"), bg=COULEUR_FOND, fg=COULEUR_TITRE,
        ).pack(pady=(20, 5))

        self.canvas = tk.Canvas(self, width=200, height=190, bg=COULEUR_SECONDAIRE, highlightthickness=0)
        self.canvas.pack(pady=6)
        self._dessiner_potence()

        self.label_essais = tk.Label(
            self, text=self._texte_essais(), font=("Segoe UI", 12, "bold"),
            bg=COULEUR_FOND, fg=COULEUR_SUCCES,
        )
        self.label_essais.pack(pady=(0, 6))

        self.label_mot = tk.Label(
            self, text=self._mot_masque(), font=("Consolas", 20, "bold"),
            bg=COULEUR_FOND, fg=COULEUR_TITRE,
        )
        self.label_mot.pack(pady=6)

        self.conteneur_clavier = tk.Frame(self, bg=COULEUR_FOND)
        self.conteneur_clavier.pack(pady=(5, 8))

        for i, lettre in enumerate(ALPHABET):
            b = tk.Button(
                self.conteneur_clavier, text=lettre, font=("Segoe UI", 10, "bold"),
                bg=COULEUR_SECONDAIRE, fg=COULEUR_TITRE, relief="flat",
                width=3, cursor="hand2", bd=0,
                command=lambda l=lettre: self.proposer_lettre(l),
            )
            b.grid(row=i // 9, column=i % 9, padx=2, pady=2)
            self.boutons_lettres[lettre] = b

        bouton_secondaire(self, "Abandonner", self.abandonner, largeur=14).pack(pady=(0, 5))

        # Bouton affiché seulement une fois la partie finie
        self.conteneur_fin = tk.Frame(self, bg=COULEUR_FOND)

        bouton_retour(self, app.afficher_menu).pack(side="bottom", pady=12)

    def _texte_essais(self):
        return f"Essais restants : {self.max_essais - self.nb_erreurs}"

    def _mot_masque(self):
        return " ".join(l if l in self.lettres_trouvees else "_" for l in self.mot)

    def proposer_lettre(self, lettre):
        if self.partie_terminee or lettre in self.lettres_tentees:
            return
        self.lettres_tentees.add(lettre)
        self.boutons_lettres[lettre].config(state="disabled", bg=COULEUR_SECONDAIRE_SURVOL)

        if lettre in self.mot:
            self.lettres_trouvees.add(lettre)
            self.label_mot.config(text=self._mot_masque())
            if all(l in self.lettres_trouvees for l in self.mot):
                self._terminer(gagne=True)
        else:
            self.nb_erreurs += 1
            self.label_essais.config(text=self._texte_essais())
            self._dessiner_etape(self.nb_erreurs)
            if self.nb_erreurs >= self.max_essais:
                self._terminer(gagne=False)

    def abandonner(self):
        if self.partie_terminee:
            return
        self._terminer(gagne=False, abandon=True)

    def _terminer(self, gagne, abandon=False):
        self.partie_terminee = True
        for b in self.boutons_lettres.values():
            b.config(state="disabled")

        if abandon:
            self.label_essais.config(text=f"🚩 Partie abandonnée. C'était {self.mot}", fg=COULEUR_ERREUR)
            self.label_mot.config(text=self.mot)
        elif gagne:
            self.label_essais.config(text=f"🎉 Gagné ! C'était {self.mot}", fg=COULEUR_SUCCES)
        else:
            self.label_essais.config(text=f"💀 Perdu ! C'était {self.mot}", fg=COULEUR_ERREUR)
            self.label_mot.config(text=self.mot)

        enregistrer_resultat("pendu", "victoires" if gagne else "defaites")

        self.conteneur_fin.pack(pady=8)
        bouton(self.conteneur_fin, "🔁 Rejouer", self.rejouer, largeur=14, hauteur=1).pack()

    def rejouer(self):
        self.app.afficher_frame(FramePenduJeu, categorie=self.categorie, params=self.params)

    def _dessiner_potence(self):
        c = self.canvas
        c.create_line(15, 175, 100, 175, fill=COULEUR_TITRE, width=3)
        c.create_line(40, 175, 40, 15, fill=COULEUR_TITRE, width=3)
        c.create_line(40, 15, 120, 15, fill=COULEUR_TITRE, width=3)
        c.create_line(120, 15, 120, 38, fill=COULEUR_TITRE, width=3)

    def _dessiner_etape(self, nb_erreurs):
        """
        Ajoute une partie du corps selon le nombre d'erreurs, réparti
        proportionnellement sur les 6 parties du corps selon le max_essais
        du niveau choisi. On redessine tout jusqu'à l'étape courante pour
        éviter les trous si le pas saute plusieurs parties d'un coup.
        """
        parties = [self._tete, self._corps, self._bras_g, self._bras_d, self._jambe_g, self._jambe_d]
        index = round(nb_erreurs / self.max_essais * len(parties)) - 1
        index = max(0, min(index, len(parties) - 1))
        self.canvas.delete("corps")
        for i in range(index + 1):
            parties[i]()

    def _tete(self):
        self.canvas.create_oval(100, 38, 138, 76, outline=COULEUR_ERREUR, width=3, tags="corps")

    def _corps(self):
        self.canvas.create_line(120, 76, 120, 128, fill=COULEUR_ERREUR, width=3, tags="corps")

    def _bras_g(self):
        self.canvas.create_line(120, 86, 98, 110, fill=COULEUR_ERREUR, width=3, tags="corps")

    def _bras_d(self):
        self.canvas.create_line(120, 86, 142, 110, fill=COULEUR_ERREUR, width=3, tags="corps")

    def _jambe_g(self):
        self.canvas.create_line(120, 128, 100, 160, fill=COULEUR_ERREUR, width=3, tags="corps")

    def _jambe_d(self):
        self.canvas.create_line(120, 128, 140, 160, fill=COULEUR_ERREUR, width=3, tags="corps")


if __name__ == "__main__":
    from app import App
    App().mainloop()