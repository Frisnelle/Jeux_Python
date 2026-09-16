# 🎮 Jeux Python

Un hub de mini-jeux développés en Python, avec deux versions jouables : une en console, une avec interface graphique (Tkinter).

Projet personnel réalisé pour pratiquer la programmation orientée objet, les algorithmes de jeu (dont le **minimax**), et la construction d'une interface graphique cohérente à partir de zéro.

## 🕹️ Jeux disponibles

- **Anagramme chronométré** — un mot mélangé à retrouver avant la fin du temps imparti, avec catégories et niveaux de difficulté.
- **Pendu** — devine le mot secret lettre par lettre avant d'épuiser tes essais.
- **Morpion** — 2 joueurs en local, ou contre une IA (algorithme **minimax**) avec 4 niveaux de difficulté (Facile, Moyen, Difficile, Impossible).
- **Puissance 4** — grille 6×7, 2 joueurs en local ou contre une IA (**minimax** + élagage alpha-bêta, profondeur limitée) avec 4 niveaux de difficulté.

Les 9 catégories de mots disponibles (ville, pays, animal, fruit, métier, sport, couleur, objet, instrument) sont partagées entre l'anagramme et le pendu.

## 🖥️ Deux versions

### Version console

```bash
python main.py
```

Menu textuel classique, jeux jouables directement dans le terminal.

### Version graphique (Tkinter)

```bash
python interface/app.py
```

Une seule fenêtre, avec navigation par écrans (menu → choix de catégorie/difficulté → jeu). Comprend :
- un thème sombre cohérent sur tout le hub,
- un chrono en temps réel pour l'anagramme,
- un pendu qui se dessine progressivement sur un `Canvas`,
- une grille de morpion cliquable avec IA,
- un plateau de Puissance 4 cliquable avec IA,
- un suivi des scores (victoires/défaites) sauvegardé entre les lancements.

## 📁 Structure du projet

```
jeux-python/
├── main.py                 # Point d'entrée version console
├── mots.py                 # Banque de mots partagée (9 catégories)
├── anagramme.py             # Logique du jeu d'anagramme (console)
├── pendu.py                 # Logique du jeu du pendu (console)
├── morpion.py                # Logique du morpion + IA minimax (console)
├── puissance4.py             # Logique du Puissance 4 + IA minimax (console)
├── scores.json               # Scores sauvegardés (généré automatiquement, non versionné)
└── interface/
    ├── app.py                # Point d'entrée version graphique
    ├── style.py               # Couleurs, polices, boutons réutilisables
    ├── ecran_choix.py          # Écran générique de sélection (catégorie/difficulté/mode)
    ├── score.py                # Sauvegarde et lecture des statistiques (JSON)
    ├── anagramme_gui.py         # Anagramme version graphique
    ├── pendu_gui.py              # Pendu version graphique
    ├── morpion_gui.py            # Morpion version graphique
    └── puissance4_gui.py         # Puissance 4 version graphique
```

## 🧠 Ce que ce projet met en pratique

- Séparation des données (`mots.py`), de la logique de jeu, et de l'interface
- Algorithme **minimax** (morpion) et **minimax + alpha-bêta** (Puissance 4) pour des IA configurables
- Interface Tkinter à fenêtre unique avec navigation par `Frame` (pas de popups multiples)
- Persistance de données simple via JSON (scores)
- Réutilisation de composants d'interface entre plusieurs jeux (`ecran_choix.py`)

## 🚀 Pistes d'évolution

- Version web avec Flask
- Historique de parties détaillé (pas seulement des compteurs)
- Nouveaux jeux (quiz, memory...)

## 🛠️ Prérequis

- Python 3.8+ (aucune dépendance externe, Tkinter est inclus avec Python)