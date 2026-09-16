"""
Style partagé (couleurs, polices, boutons) pour tout le hub de jeux,
afin que le menu et les jeux aient un rendu visuel cohérent.
"""

import tkinter as tk

COULEUR_FOND = "#1e1e2e"
COULEUR_CARTE = "#282838"
COULEUR_TITRE = "#f5f5f5"
COULEUR_SOUS_TITRE = "#a6adc8"
COULEUR_ACCENT = "#89b4fa"
COULEUR_ACCENT_SURVOL = "#74a8f9"
COULEUR_SECONDAIRE = "#313244"
COULEUR_SECONDAIRE_SURVOL = "#45475a"
COULEUR_SUCCES = "#a6e3a1"
COULEUR_ERREUR = "#f38ba8"
COULEUR_GAGNANT = "#f9e2af"
COULEUR_TEXTE_BOUTON = "#1e1e2e"

POLICE_TITRE = ("Segoe UI", 26, "bold")
POLICE_SOUS_TITRE = ("Segoe UI", 12)
POLICE_BOUTON = ("Segoe UI", 13, "bold")
POLICE_MONO = ("Consolas", 30, "bold")


def bouton(parent, texte, commande, largeur=22, hauteur=2,
           couleur=COULEUR_ACCENT, couleur_survol=COULEUR_ACCENT_SURVOL,
           couleur_texte=COULEUR_TEXTE_BOUTON, police=POLICE_BOUTON):
    """Bouton stylisé avec effet de survol (la couleur change au passage de la souris)."""
    b = tk.Button(
        parent, text=texte, command=commande, font=police,
        bg=couleur, fg=couleur_texte, activebackground=couleur_survol,
        relief="flat", width=largeur, height=hauteur, cursor="hand2", bd=0,
    )
    b.bind("<Enter>", lambda e: b.config(bg=couleur_survol))
    b.bind("<Leave>", lambda e: b.config(bg=couleur))
    return b


def bouton_secondaire(parent, texte, commande, largeur=18):
    """Variante plus discrète, utilisée pour les écrans de choix (catégorie, difficulté...)."""
    return bouton(
        parent, texte, commande, largeur=largeur, hauteur=1,
        couleur=COULEUR_SECONDAIRE, couleur_survol=COULEUR_SECONDAIRE_SURVOL,
        couleur_texte=COULEUR_TITRE,
    )


def bouton_retour(parent, commande):
    """Petit lien discret pour revenir au menu principal depuis n'importe quel écran."""
    b = tk.Button(
        parent, text="← Retour au menu", command=commande,
        font=("Segoe UI", 10), bg=COULEUR_FOND, fg=COULEUR_SOUS_TITRE,
        relief="flat", cursor="hand2", bd=0, activebackground=COULEUR_FOND,
    )
    b.bind("<Enter>", lambda e: b.config(fg=COULEUR_TITRE))
    b.bind("<Leave>", lambda e: b.config(fg=COULEUR_SOUS_TITRE))
    return b