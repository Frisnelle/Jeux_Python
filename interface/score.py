"""
Gestion des statistiques de jeu, sauvegardées dans un fichier JSON
(scores.json à la racine du projet) pour qu'elles persistent entre
les lancements de l'application.
"""

import json
import os

CHEMIN_SCORES = os.path.join(os.path.dirname(__file__), "..", "scores.json")

SCORES_PAR_DEFAUT = {
    "anagramme": {"victoires": 0, "defaites": 0},
    "pendu": {"victoires": 0, "defaites": 0},
    "morpion": {"victoires": 0, "defaites": 0, "nuls": 0},
}


def charger_scores():
    """Charge les scores depuis le fichier JSON, ou renvoie des valeurs à zéro si absent/corrompu."""
    if not os.path.exists(CHEMIN_SCORES):
        return {jeu: dict(valeurs) for jeu, valeurs in SCORES_PAR_DEFAUT.items()}
    try:
        with open(CHEMIN_SCORES, "r", encoding="utf-8") as f:
            scores = json.load(f)
        for jeu, valeurs in SCORES_PAR_DEFAUT.items():
            scores.setdefault(jeu, dict(valeurs))
        return scores
    except (json.JSONDecodeError, OSError):
        return {jeu: dict(valeurs) for jeu, valeurs in SCORES_PAR_DEFAUT.items()}


def sauvegarder_scores(scores):
    """Écrit les scores dans le fichier JSON."""
    try:
        with open(CHEMIN_SCORES, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2, ensure_ascii=False)
    except OSError:
        pass  # un souci d'écriture disque ne doit jamais interrompre une partie


def enregistrer_resultat(jeu, resultat):
    """
    Incrémente le compteur correspondant pour le jeu donné et sauvegarde.
    resultat : 'victoires', 'defaites', ou 'nuls' (morpion uniquement).
    """
    scores = charger_scores()
    scores.setdefault(jeu, dict(SCORES_PAR_DEFAUT.get(jeu, {})))
    scores[jeu][resultat] = scores[jeu].get(resultat, 0) + 1
    sauvegarder_scores(scores)
    return scores