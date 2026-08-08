"""
Point d'entrée graphique du hub de jeux.

Une seule fenêtre reste ouverte du début à la fin : son contenu
change d'écran en écran (menu -> choix -> jeu) via des Frames qui
se remplacent, plutôt que d'ouvrir une nouvelle fenêtre à chaque étape.
"""

import tkinter as tk

from style import COULEUR_FOND, COULEUR_TITRE, COULEUR_SOUS_TITRE, POLICE_TITRE, POLICE_SOUS_TITRE, bouton


class App(tk.Tk):
    """Fenêtre unique du hub. Gère le passage d'un écran à l'autre."""

    def __init__(self):
        super().__init__()
        self.title("Hub de jeux")
        self.geometry("520x620")
        self.configure(bg=COULEUR_FOND)
        self.resizable(False, False)

        self.conteneur = tk.Frame(self, bg=COULEUR_FOND)
        self.conteneur.pack(fill="both", expand=True)

        self.frame_actuelle = None
        self.afficher_menu()

    def afficher_frame(self, classe_frame, **kwargs):
        """Détruit l'écran actuel (s'il existe) et affiche le nouveau à la place."""
        if self.frame_actuelle is not None:
            self.frame_actuelle.destroy()
        self.frame_actuelle = classe_frame(self.conteneur, self, **kwargs)
        self.frame_actuelle.pack(fill="both", expand=True)

    def afficher_menu(self):
        self.afficher_frame(FrameMenu)


class FrameMenu(tk.Frame):
    """Écran d'accueil : un bouton par jeu."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COULEUR_FOND)

        tk.Label(
            self, text="🎮 Hub de jeux", font=POLICE_TITRE,
            bg=COULEUR_FOND, fg=COULEUR_TITRE,
        ).pack(pady=(50, 5))

        tk.Label(
            self, text="Choisis un jeu pour commencer",
            font=POLICE_SOUS_TITRE, bg=COULEUR_FOND, fg=COULEUR_SOUS_TITRE,
        ).pack(pady=(0, 40))

        conteneur_boutons = tk.Frame(self, bg=COULEUR_FOND)
        conteneur_boutons.pack(expand=True)

        # Imports locaux pour éviter les imports circulaires
        # (les jeux importent FrameChoix qui ne dépend pas de app.py,
        # mais app.py a besoin des jeux pour construire ce menu).
        from anagramme_gui import demarrer_anagramme
        from pendu_gui import demarrer_pendu
        from morpion_gui import demarrer_morpion

        bouton(conteneur_boutons, "🔤  Anagramme", lambda: demarrer_anagramme(app)).pack(pady=8)
        bouton(conteneur_boutons, "🪢  Pendu", lambda: demarrer_pendu(app)).pack(pady=8)
        bouton(conteneur_boutons, "❌⭕  Morpion", lambda: demarrer_morpion(app)).pack(pady=8)

        tk.Button(
            self, text="Quitter", command=app.destroy,
            font=("Segoe UI", 10), bg=COULEUR_FOND, fg=COULEUR_SOUS_TITRE,
            relief="flat", cursor="hand2", bd=0,
        ).pack(pady=(30, 20), side="bottom")


if __name__ == "__main__":
    app = App()
    app.mainloop()