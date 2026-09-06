# ChessFlow

ChessFlow est une application Python hors ligne destinée à la gestion de tournois d’échecs en ligne de commande.

L’application utilise une architecture MVC légère et des fichiers JSON locaux pour conserver les joueurs et les tournois entre deux exécutions.

## Prérequis

- Python 3.13 ou une version compatible ;
- pip, fourni avec Python ;
- Git pour cloner le dépôt.

Vérifier les versions installées :

```bash
git --version
python3 --version
```

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/fabienhummel/OC-PY04-chessflow.git
cd OC-PY04-chessflow
```

### 2. Créer l’environnement virtuel

Sur macOS ou Linux :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Sur Windows avec PowerShell :

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Installer les dépendances

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Exécution

Lancer ChessFlow depuis la racine du projet :

```bash
python main.py
```

L’application permet notamment de :

- créer et consulter le registre des joueurs ;
- créer et reprendre des tournois ;
- sélectionner les participants ;
- ajouter ou retirer un participant tant que la première ronde n’a pas commencé ;
- créer les rondes et les matchs ;
- saisir ou modifier les résultats ;
- consulter les classements et les rapports ;
- retrouver les données après redémarrage grâce à la persistance JSON.

### Interface console

L’interface est organisée comme un écran plutôt que comme un historique de lignes dans le terminal :

- le menu courant reste visible dans la partie supérieure ;
- la zone `OUTPUT` affiche uniquement le résultat ou le message associé à l’action courante ;
- le tournoi chargé est affiché dans l’en-tête dans toute l’application ;
- lorsqu’une ronde est ouverte, son nom est également affiché dans l’en-tête ;
- les erreurs et confirmations sont affichées dans la zone `OUTPUT` au lieu de s’accumuler dans le terminal ;
- `0` permet de revenir au menu précédent dans les sous-menus.

Les données locales sont enregistrées dans :

```text
data/players.json
data/tournaments/
```

## Tests

Exécuter tous les tests depuis la racine du projet :

```bash
python -m unittest discover -v
```

La version actuelle comporte 75 tests automatisés passants.

## Qualité du code

Vérifier le code avec Flake8 :

```bash
flake8 .
```

La configuration du projet fixe la longueur maximale à 119 caractères par ligne.

Générer ou mettre à jour le rapport HTML Flake8 :

```bash
flake8 --format=html --htmldir=flake8_rapport .
```

Le rapport est disponible dans :

```text
flake8_rapport/index.html
```

## Structure du projet

```text
OC-PY04-chessflow/
├── controllers/
│   ├── application_controller.py
│   ├── match_controller.py
│   ├── player_controller.py
│   ├── round_controller.py
│   └── tournament_controller.py
├── data/
│   └── tournaments/
├── documentation/
├── flake8_rapport/
├── models/
├── persistence/
│   └── json_repository.py
├── tests/
├── views/
│   └── console_screen.py
├── .flake8
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

- `models/` contient les objets métier, leurs données, leurs comportements simples et leur sérialisation ;
- `views/` gère l’affichage console et les saisies utilisateur ;
- `views/console_screen.py` centralise le rendu des écrans, de l’en-tête de contexte et de la zone `OUTPUT` ;
- `controllers/` porte les validations, les règles applicatives et la coordination ;
- `persistence/` centralise les lectures et écritures JSON ainsi que les accès aux fichiers de données ;
- `ApplicationController` relie les vues aux contrôleurs spécialisés, pilote les menus et fournit le contexte d’affichage global ;
- `tests/` contient les tests automatisés ;
- `flake8_rapport/` contient le rapport HTML de qualité ;
- `main.py` est le point d’entrée minimal de l’application.

## Désactivation de l’environnement virtuel

```bash
deactivate
```
