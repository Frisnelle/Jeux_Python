"""
Point d'entrée graphique du hub de jeux.

Une seule fenêtre reste ouverte du début à la fin : son contenu
change d'écran en écran (menu -> choix -> jeu) via des Frames qui
se remplacent, plutôt que d'ouvrir une nouvelle fenêtre à chaque étape.
"""

import tkinter as tk

from style import COULEUR_FOND, COULEUR_TITRE, COULEUR_SOUS_TITRE, POLICE_TITRE, POLICE_SOUS_TITRE, bouton
from score import charger_scores


class App(tk.Tk):
    """Fenêtre unique du hub. Gère le passage d'un écran à l'autre."""

    def __init__(self):
        super().__init__()
        self.title("Hub de jeux")
        self.configure(bg=COULEUR_FOND)
        self.resizable(False, False)
        self._centrer(520, 680)

        self.conteneur = tk.Frame(self, bg=COULEUR_FOND)
        self.conteneur.pack(fill="both", expand=True)

        self.frame_actuelle = None
        self.afficher_menu()

    def _centrer(self, largeur, hauteur):
        """Positionne la fenêtre au centre de l'écran de l'utilisateur au démarrage."""
        self.update_idletasks()
        x = (self.winfo_screenwidth() - largeur) // 2
        y = (self.winfo_screenheight() - hauteur) // 2
        self.geometry(f"{largeur}x{hauteur}+{x}+{y}")

    def afficher_frame(self, classe_frame, **kwargs):
        """Détruit l'écran actuel (s'il existe) et affiche le nouveau à la place."""
        if self.frame_actuelle is not None:
            self.frame_actuelle.destroy()
        self.frame_actuelle = classe_frame(self.conteneur, self, **kwargs)
        self.frame_actuelle.pack(fill="both", expand=True)

    def afficher_menu(self):
        self.afficher_frame(FrameMenu)


class FrameMenu(tk.Frame):
    """Écran d'accueil : un bouton par jeu, plus un résumé des scores."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COULEUR_FOND)

        tk.Label(
            self, text="🎮 Hub de jeux", font=POLICE_TITRE,
            bg=COULEUR_FOND, fg=COULEUR_TITRE,
        ).pack(pady=(45, 5))

        tk.Label(
            self, text="Choisis un jeu pour commencer",
            font=POLICE_SOUS_TITRE, bg=COULEUR_FOND, fg=COULEUR_SOUS_TITRE,
        ).pack(pady=(0, 25))

        conteneur_boutons = tk.Frame(self, bg=COULEUR_FOND)
        conteneur_boutons.pack(expand=True)

        # Imports locaux pour éviter les imports circulaires
        # (les jeux importent FrameChoix qui ne dépend pas de app.py,
        # mais app.py a besoin des jeux pour construire ce menu).
        from anagramme_gui import demarrer_anagramme
        from pendu_gui import demarrer_pendu
        from morpion_gui import demarrer_morpion
        from puissance4_gui import demarrer_puissance4

        bouton(conteneur_boutons, "🔤  Anagramme", lambda: demarrer_anagramme(app)).pack(pady=6)
        bouton(conteneur_boutons, "🪢  Pendu", lambda: demarrer_pendu(app)).pack(pady=6)
        bouton(conteneur_boutons, "❌⭕  Morpion", lambda: demarrer_morpion(app)).pack(pady=6)
        bouton(conteneur_boutons, "🔴🟡  Puissance 4", lambda: demarrer_puissance4(app)).pack(pady=6)

        self._afficher_stats()

        tk.Button(
            self, text="Quitter", command=app.destroy,
            font=("Segoe UI", 10), bg=COULEUR_FOND, fg=COULEUR_SOUS_TITRE,
            relief="flat", cursor="hand2", bd=0,
        ).pack(pady=(15, 20), side="bottom")

    def _afficher_stats(self):
        """Affiche un petit résumé des scores cumulés, sous les boutons de jeu."""
        scores = charger_scores()

        conteneur = tk.Frame(self, bg=COULEUR_FOND)
        conteneur.pack(pady=(20, 0))

        lignes = [
            ("🔤 Anagramme", f"{scores['anagramme']['victoires']} gagnées / {scores['anagramme']['defaites']} ratées"),
            ("🪢 Pendu", f"{scores['pendu']['victoires']} gagnées / {scores['pendu']['defaites']} ratées"),
            ("❌⭕ Morpion", f"{scores['morpion']['victoires']}V / {scores['morpion']['defaites']}D / {scores['morpion']['nuls']}N"),
            ("🔴🟡 Puissance 4", f"{scores['puissance4']['victoires']}V / {scores['puissance4']['defaites']}D / {scores['puissance4']['nuls']}N"),
        ]

        for nom, texte in lignes:
            ligne = tk.Frame(conteneur, bg=COULEUR_FOND)
            ligne.pack(fill="x", pady=1)
            tk.Label(
                ligne, text=nom, font=("Segoe UI", 9), bg=COULEUR_FOND, fg=COULEUR_SOUS_TITRE, width=16, anchor="w",
            ).pack(side="left")
            tk.Label(
                ligne, text=texte, font=("Segoe UI", 9), bg=COULEUR_FOND, fg=COULEUR_SOUS_TITRE, anchor="w",
            ).pack(side="left")


if __name__ == "__main__":
    app = App()
    app.mainloop()
    