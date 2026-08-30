# Spécifications techniques de ChessFlow

## 1. Architecture générale

ChessFlow est une application console Python autonome organisée selon une architecture MVC légère.

```text
Utilisateur
    |
    v
Vues console <-> Contrôleurs -> Modèles métier
                    |
                    +-------> Persistance JSON
```

### Responsabilités

- **Modèles** : représenter les données métier, leurs validations et leur sérialisation.
- **Vues** : afficher les informations et recueillir les saisies utilisateur avec `input()`.
- **Contrôleurs** : orchestrer la navigation, les modèles, les règles de progression, les calculs et la persistance.
- **Persistance** : lire et écrire les fichiers JSON via `utils/json_manager.py`.
- **Point d'entrée** : initialiser l'application et lancer le contrôleur principal.

Les modèles n'appellent ni `input()` ni les vues ou contrôleurs.

## 2. Environnement

| Élément | Choix retenu |
| --- | --- |
| Langage | Python |
| Version de développement | CPython 3.13.9 |
| Isolation | Environnement virtuel `.venv` |
| Gestion des dépendances | `pip` et `requirements.txt` |
| Interface | Console |
| Persistance | Fichiers JSON locaux |
| Tests | `unittest` |
| Qualité | Flake8 7.3.0, longueur maximale 119 |
| Rapport qualité | flake8-html 0.4.3 |
| Diagrammes | PlantUML et exports SVG |
| Plateformes cibles | macOS, Windows et Linux |

L'application métier utilise uniquement la bibliothèque standard. Les dépendances du fichier `requirements.txt` servent au contrôle qualité et au rapport HTML.

## 3. Arborescence livrée

```text
OC-PY04-chessflow/
├── controllers/
├── data/
│   └── tournaments/
├── documentation/
├── flake8_rapport/
├── models/
├── tests/
├── utils/
├── views/
├── .flake8
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

`data/players.json` et les fichiers `data/tournaments/*.json` sont créés localement au besoin et ne font pas partie des données à versionner.

Les fichiers et dossiers générés localement, comme `.venv`, `__pycache__`, les métadonnées d'IDE et les données d'utilisation, sont exclus par `.gitignore`.

## 4. Modèles métier

### `Player`

Attributs :

- `last_name: str` ;
- `first_name: str` ;
- `birth_date: str` au format `YYYY-MM-DD` ;
- `national_id: str` normalisé en majuscules.

Responsabilités :

- valider et normaliser les textes obligatoires ;
- valider la date de naissance avec `date.fromisoformat()` ;
- valider l'identifiant avec l'expression régulière `[A-Z]{2}[0-9]{5}` ;
- fournir `to_dict()` et `from_dict()` pour la persistance.

L'unicité de l'identifiant dans le registre est contrôlée par `PlayerController`.

### `Tournament`

Attributs :

- `name: str` ;
- `location: str` ;
- `start_date: str` ;
- `end_date: str` ;
- `description: str` ;
- `number_of_rounds: int` ;
- `current_round: int` ;
- `players: list[Player]` ;
- `rounds: list[Round]`.

Responsabilités :

- valider le nom, le lieu, les dates et le nombre de rondes ;
- empêcher une date de fin antérieure à la date de début ;
- ajouter un joueur à sa collection ;
- ajouter une ronde et incrémenter `current_round` ;
- fournir `to_dict()` et `from_dict()`.

Le modèle `Tournament` ne stocke ni score cumulé, ni classement, ni statut distinct. Ces informations sont déduites des rondes et matchs par le contrôleur.

### `Round`

Attributs :

- `name: str` ;
- `matches: list[Match]` ;
- `start_datetime: datetime | None` ;
- `end_datetime: datetime | None`.

Responsabilités :

- contenir les matchs de la ronde ;
- enregistrer l'heure de fin avec `close()` ;
- fournir `to_dict()` et `from_dict()`.

Le contrôleur renseigne l'heure de début lors de la création et vérifie la complétude des résultats avant d'appeler `close()`.

### `Match`

Représentation interne :

```python
pair = (
    [player_one, score_one],
    [player_two, score_two],
)
```

`pair` est un tuple de deux listes mutables afin de conserver une structure de paire tout en permettant la saisie ultérieure des scores.

Propriétés exposées :

- `player_one` ;
- `player_two` ;
- `score_one` ;
- `score_two`.

Responsabilités :

- refuser deux joueurs ayant le même identifiant national ;
- accepter uniquement `(1, 0)`, `(0, 1)` et `(0.5, 0.5)` ;
- modifier les scores dans les deux listes internes ;
- fournir `to_dict()` et `from_dict()`.

## 5. Contrôleurs

### `PlayerController`

Responsabilités principales :

- charger le registre des joueurs au démarrage ;
- créer, lister, rechercher, modifier et supprimer les joueurs ;
- contrôler l'unicité de l'identifiant national ;
- trier les listes par nom puis prénom ;
- bloquer les écritures si le registre n'a pas pu être chargé correctement ;
- déclencher les sauvegardes après modification.

### `TournamentController`

Responsabilités principales :

- créer, lister et charger les tournois ;
- ajouter les participants avant le démarrage de la première ronde ;
- créer les rondes et leurs matchs ;
- contrôler qu'une ronde précédente est clôturée ;
- calculer le score d'un joueur en parcourant tous les matchs ;
- produire le classement par score décroissant ;
- détecter les rencontres déjà jouées ;
- enregistrer les résultats et clôturer les rondes ;
- déclencher les sauvegardes.

### `ApplicationController`

Responsabilités principales :

- piloter les menus et sous-menus ;
- relier les vues aux contrôleurs métier ;
- gérer le tournoi actuellement chargé ;
- appliquer les conditions de navigation et de progression ;
- présenter les erreurs métier à l'utilisateur.

## 6. Relations UML

| Relation | Type | Cardinalité |
| --- | --- | --- |
| `Tournament` - `Player` | Agrégation | Un tournoi agrège 0..* joueurs ; un joueur peut apparaître dans 0..* tournois |
| `Tournament` - `Round` | Composition métier | Un tournoi contient 0..* rondes |
| `Round` - `Match` | Composition métier | Une ronde contient 0..* matchs |
| `Match` - `Player` | Association | Un match référence exactement deux joueurs |

Aucune classe abstraite ni hiérarchie d'héritage ne sont utilisées.

## 7. Persistance JSON

### Chemins

Les chemins sont ancrés sur la racine du projet avec `pathlib` :

```text
PROJECT_ROOT
└── data/
    ├── players.json
    └── tournaments/
```

### Principes

- `load_players()` retourne une liste vide si `players.json` n'existe pas ;
- un fichier joueur vide, un JSON invalide ou une structure autre qu'une liste produit une `ValueError` explicite ;
- les données de chaque joueur sont revalidées par `Player.from_dict()` ;
- `save_players()` crée le dossier parent si nécessaire et écrit en UTF-8 ;
- `load_tournament()` vérifie l'existence, la taille, la syntaxe JSON et la structure dictionnaire ;
- les données du tournoi sont revalidées lors de `Tournament.from_dict()` ;
- `save_tournament()` crée `data/tournaments/` si nécessaire et écrit en UTF-8 ;
- les objets métier sont sérialisés avec leurs méthodes `to_dict()`.

Les écritures utilisent directement les fichiers cibles. Il n'y a pas de mécanisme de remplacement atomique dans la version 1.0.

## 8. Algorithme d'appariement

### Première ronde

1. copier `tournament.players` ;
2. mélanger la copie avec `random.shuffle()` ;
3. extraire les joueurs deux par deux ;
4. créer un objet `Match` pour chaque paire.

### Rondes suivantes

1. produire le classement avec `get_ranking()` ;
2. trier les joueurs par score décroissant ;
3. conserver l'ordre relatif des joueurs à égalité, car `sorted()` est stable ;
4. prendre le premier joueur disponible ;
5. rechercher le premier adversaire restant qui n'a pas déjà été rencontré ;
6. si aucun adversaire inédit n'existe, utiliser le premier adversaire restant ;
7. répéter jusqu'à épuisement de la liste.

L'objectif est un algorithme simple et explicable qui évite les revanches autant que possible, sans recherche exhaustive du système suisse.

## 9. Calcul des scores et classement

Les scores ne sont pas stockés comme attributs de `Player` ou `Tournament`.

`TournamentController.get_player_score()` parcourt toutes les rondes et tous les matchs du tournoi. Il additionne les scores non nuls associés à l'identifiant national du joueur.

`get_ranking()` trie ensuite `tournament.players` par score décroissant.

Cette approche garantit qu'après rechargement d'un tournoi, les scores sont reconstruits automatiquement depuis les résultats persistés.

## 10. Validation des entrées

### Modèles

- nom et prénom : texte non vide après `strip()` ;
- identifiant national : normalisation en majuscules puis expression régulière `[A-Z]{2}[0-9]{5}` ;
- date de naissance et dates du tournoi : parsing avec `date.fromisoformat()` ;
- date de fin supérieure ou égale à la date de début ;
- nombre de rondes converti en entier strictement positif ;
- résultat limité aux trois couples autorisés.

### Contrôleurs et vues

- unicité de l'identifiant joueur contrôlée lors de la création et de la modification ;
- doublon de participant refusé dans un tournoi ;
- ajout de participant interdit après la première ronde ;
- création d'une ronde refusée sans participant ou avec un nombre impair ;
- nouvelle ronde interdite tant qu'une ronde précédente est ouverte ;
- nouvelle ronde interdite lorsque le nombre prévu est atteint ;
- clôture refusée tant qu'un résultat manque ;
- saisie des scores répétée tant que le couple n'est pas valide.

## 11. Qualité et vérification

La configuration Flake8 utilise une longueur maximale de 119 caractères.

Contrôle standard :

```bash
flake8 .
```

Génération du rapport HTML :

```bash
flake8 --format=html --htmldir=flake8_rapport .
```

Le rapport final indique zéro erreur Flake8 sur 28 fichiers analysés.

Les tests automatisés sont exécutés avec :

```bash
python -m unittest discover -v
```

La version consolidée comporte 70 tests passants.

Les vérifications couvrent notamment :

- validation des modèles ;
- représentation interne du match ;
- sérialisation et désérialisation ;
- persistance JSON et erreurs de chargement ;
- unicité et tri des joueurs ;
- appariements et historique des rencontres ;
- saisie des résultats et calcul des scores ;
- règles de progression des rondes ;
- indépendance des modèles vis-à-vis des vues et contrôleurs.

## 12. Sécurité et robustesse

- aucune donnée sensible ni aucun secret n'est nécessaire ;
- aucune communication réseau n'est effectuée pendant l'usage métier ;
- les chemins sont construits avec `pathlib` ;
- les données chargées sont validées avant reconstruction des objets ;
- les erreurs JSON sont remontées avec des messages explicites ;
- le registre joueur n'est pas réécrit si son chargement a échoué ;
- les données locales d'utilisation sont séparées du code source et ne sont pas versionnées.
