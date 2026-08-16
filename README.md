# ChessFlow

ChessFlow est une application Python hors ligne destinée à la gestion de tournois d’échecs.

Le projet repose sur une architecture MVC et utilise des fichiers JSON pour assurer la persistance des données.

## Prérequis

Avant d’installer le projet, vérifier la présence des outils suivants :

- Git ;
- Python 3.13 ou une version compatible ;
- pip, fourni avec Python.

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

### 2. Configurer l’identité Git locale

Cette configuration s’applique uniquement au dépôt ChessFlow :

```bash
git config --local user.name "Votre nom"
git config --local user.email "votre-adresse-github@example.com"
```

Il est recommandé d’utiliser l’adresse privée `noreply` associée au compte GitHub.

### 3. Créer l’environnement virtuel

Sur macOS ou Linux :

```bash
python3 -m venv .venv
```

Sur Windows :

```powershell
python -m venv .venv
```

### 4. Activer l’environnement virtuel

Sur macOS ou Linux :

```bash
source .venv/bin/activate
```

Sur Windows avec PowerShell :

```powershell
.venv\Scripts\Activate.ps1
```

Une fois l’environnement activé, l’invite de commande doit commencer par `(.venv)`.

### 5. Installer les dépendances

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 6. Vérifier l’installation

```bash
python --version
flake8 --version
```

## Exécution

Lancer l’application depuis la racine du projet :

```bash
python main.py
```

## Qualité du code

Vérifier la conformité du code avec Flake8 :

```bash
flake8 .
```

Le projet applique une longueur maximale de 119 caractères par ligne.

Générer le rapport HTML demandé dans le cahier des charges :

```bash
flake8 . --format=html --htmldir=flake8_rapport
```

Le rapport est ensuite disponible dans :

```text
flake8_rapport/index.html
```

## Structure du projet

```text
OC-PY04-chessflow/
├── controllers/
│   └── __init__.py
├── models/
│   └── __init__.py
├── views/
│   └── __init__.py
├── .flake8
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

- `models` contient les données et la logique métier ;
- `views` gère les affichages et les interactions avec l’utilisateur ;
- `controllers` coordonne les modèles et les vues ;
- `main.py` constitue le point d’entrée de l’application.

## Désactivation de l’environnement virtuel

```bash
deactivate
```

## État du projet

Le projet est en cours de développement. Les fonctionnalités et les instructions d’utilisation seront complétées progressivement.