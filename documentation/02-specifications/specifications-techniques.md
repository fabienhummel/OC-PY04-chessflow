# Spécifications techniques de ChessFlow

## 1. Architecture générale

ChessFlow est une application console Python autonome organisée selon une architecture MVC légère.

```text
Utilisateur
    |
    v
Vues console <-> ApplicationController
    |               |
    v               +--> PlayerController
ConsoleScreen       +--> TournamentController
                    +--> RoundController
                    +--> MatchController
                              |
                              +--> Modèles métier
                              +--> Persistance JSON
```

### Responsabilités

- **Modèles** : représenter les données métier, leurs comportements simples et leur sérialisation.
- **Vues** : afficher les informations et recueillir les saisies utilisateur avec `input()`.
- **ConsoleScreen** : centraliser l’effacement et le rendu cohérent des écrans console, du contexte global et de la zone `OUTPUT`.
- **Contrôleurs métier** : valider les entrées, appliquer les règles applicatives et déclencher les sauvegardes.
- **ApplicationController** : piloter les menus, relier les vues aux contrôleurs spécialisés et fournir le contexte du tournoi/round courant à l’affichage.
- **Persistance** : centraliser les accès aux fichiers et les lectures/écritures JSON via `persistence/json_repository.py`.
- **Point d'entrée** : initialiser l'application et lancer `ApplicationController`.

Les modèles n'appellent ni `input()`, ni les vues, ni les contrôleurs, ni la persistance.

## 2. Interface console

L’interface reste une interface en ligne de commande classique sans framework TUI externe. Elle est rendue comme un écran à deux zones :

- la partie supérieure affiche le chemin de navigation, le contexte courant et le menu actif ;
- la zone `OUTPUT` affiche le résultat, la confirmation ou l’erreur de l’action courante ;
- chaque nouvel affichage remplace l’écran précédent afin d’éviter l’accumulation d’anciens menus dans le terminal ;
- le tournoi chargé est affiché dans l’en-tête dans toute l’application ;
- lorsqu’une ronde est ouverte, son nom est également affiché dans l’en-tête ;
- après clôture de la ronde, son contexte disparaît automatiquement ;
- les sous-menus utilisent `0` pour revenir en arrière.

`views/console_screen.py` ne connaît aucune règle métier. Il reçoit uniquement des lignes de contexte, de menu et de sortie à rendre.

## 3. Environnement

| Élément | Choix retenu |
| --- | --- |
| Langage | Python |
| Version de développement | CPython 3.13.9 |
| Isolation | Environnement virtuel `.venv` |
| Gestion des dépendances | `pip` et `requirements.txt` |
| Interface | Console avec rendu partagé `ConsoleScreen` |
| Persistance | Fichiers JSON locaux |
| Tests | `unittest` |
| Qualité | Flake8 7.3.0, longueur maximale 119 |
| Rapport qualité | flake8-html 0.4.3 |
| Diagrammes | PlantUML et exports SVG |
| Plateformes cibles | macOS, Windows et Linux |

L'application métier utilise uniquement la bibliothèque standard. Les dépendances du fichier `requirements.txt` servent au contrôle qualité et au rapport HTML.

## 4. Arborescence livrée

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

`data/players.json` et les fichiers `data/tournaments/*.json` sont créés localement au besoin et ne font pas partie des données à versionner.

Les fichiers et dossiers générés localement, comme `.venv`, `__pycache__`, les métadonnées d'IDE et les données d'utilisation, sont exclus par `.gitignore`.

## 5. Modèles métier

### `Player`

Attributs :

- `last_name: str` ;
- `first_name: str` ;
- `birth_date: str` ;
- `national_id: str`.

Responsabilités :

- représenter l'identité d'un joueur ;
- fournir `to_dict()` et `from_dict()` pour la sérialisation.

La validation et la normalisation des données joueur sont effectuées par `PlayerController` avant création ou modification.

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

- contenir les informations du tournoi ;
- ajouter un joueur à sa collection ;
- ajouter une ronde et incrémenter `current_round` ;
- fournir `to_dict()` et `from_dict()`.

La validation du nom, du lieu, des dates et du nombre de rondes est effectuée par `TournamentController`.

Le modèle `Tournament` ne stocke ni score cumulé, ni classement, ni statut distinct. Ces informations sont déduites des rondes et matchs par les contrôleurs.

### `Round`

Attributs :

- `name: str` ;
- `matches: list[Match]` ;
- `start_datetime: datetime | None` ;
- `end_datetime: datetime | None`.

Responsabilités :

- contenir les matchs de la ronde ;
- ajouter un match ;
- enregistrer l'heure de fin avec `close()` ;
- fournir `to_dict()` et `from_dict()`.

`RoundController` renseigne l'heure de début lors de la création et vérifie les règles de progression avant d'appeler `close()`.

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

- représenter la paire de joueurs et leurs scores ;
- modifier les scores avec `set_result()` ;
- fournir `to_dict()` et `from_dict()`.

La validation des résultats autorisés est effectuée par `MatchController`.

## 6. Contrôleurs

### `PlayerController`

Responsabilités principales :

- charger le registre des joueurs au démarrage ;
- valider et normaliser le nom, le prénom, la date de naissance et l'identifiant national ;
- créer, lister, rechercher, modifier et supprimer les joueurs ;
- contrôler l'unicité de l'identifiant national ;
- trier les listes par nom puis prénom ;
- bloquer les écritures si le registre n'a pas pu être chargé correctement ;
- déclencher les sauvegardes après modification.

### `TournamentController`

Responsabilités principales :

- valider les informations nécessaires à la création d'un tournoi ;
- créer, lister et charger les tournois ;
- ajouter ou retirer les participants avant le démarrage de la première ronde ;
- empêcher les doublons de participants ;
- refuser la modification de la liste des participants une fois le tournoi commencé ;
- déclencher les sauvegardes liées aux informations du tournoi.

### `RoundController`

Responsabilités principales :

- contrôler la création et la clôture des rondes ;
- vérifier le nombre pair de participants et le nombre maximal de rondes ;
- générer les appariements ;
- éviter les rencontres déjà jouées autant que possible ;
- calculer le score cumulé d'un participant ;
- produire le classement et le classement avec scores ;
- déclencher les sauvegardes liées aux rondes et aux appariements.

### `MatchController`

Responsabilités principales :

- convertir les saisies de score en valeurs numériques ;
- accepter uniquement les résultats `1-0`, `0-1` et `0.5-0.5` ;
- enregistrer ou modifier le résultat d'un match ;
- déclencher la sauvegarde du tournoi après modification d'un résultat.

### `ApplicationController`

Responsabilités principales :

- piloter les menus et sous-menus ;
- relier les vues aux contrôleurs métier ;
- gérer le tournoi actuellement chargé ;
- déterminer la ronde ouverte pour le contexte d’affichage ;
- transmettre les erreurs et confirmations à la vue active.

`ApplicationController` ne porte pas les règles métier des joueurs, tournois, rondes ou résultats.

## 7. Relations UML

| Relation | Type | Cardinalité |
| --- | --- | --- |
| `Tournament` - `Player` | Agrégation | Un tournoi agrège 0..* joueurs ; un joueur peut apparaître dans 0..* tournois |
| `Tournament` - `Round` | Composition métier | Un tournoi contient 0..* rondes |
| `Round` - `Match` | Composition métier | Une ronde contient 0..* matchs |
| `Match` - `Player` | Association | Un match référence exactement deux joueurs |

Aucune classe abstraite ni hiérarchie d'héritage ne sont utilisées.

## 8. Persistance JSON

### Chemins

Les chemins sont ancrés sur la racine du projet avec `pathlib` :

```text
PROJECT_ROOT
└── data/
    ├── players.json
    └── tournaments/
```

### Principes

- `list_tournament_files()` centralise la lecture du dossier des tournois ;
- `load_players()` retourne une liste vide si `players.json` n'existe pas ;
- un fichier joueur vide, un JSON invalide ou une structure autre qu'une liste produit une `ValueError` explicite ;
- `save_players()` crée le dossier parent si nécessaire et écrit en UTF-8 ;
- `load_tournament()` vérifie l'existence, la taille, la syntaxe JSON et la structure dictionnaire ;
- `save_tournament()` crée `data/tournaments/` si nécessaire et écrit en UTF-8 ;
- les objets métier sont reconstruits avec leurs méthodes `from_dict()` et sérialisés avec `to_dict()`.

La couche de persistance contrôle la syntaxe JSON, le type général des structures et la présence des clés nécessaires à la reconstruction. Les validations métier des nouvelles saisies utilisateur restent dans les contrôleurs.

Les écritures utilisent directement les fichiers cibles. Il n'y a pas de mécanisme de remplacement atomique dans la version 1.0.

## 9. Algorithme d'appariement

L'algorithme est géré par `RoundController`.

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

## 10. Calcul des scores et classement

Les scores ne sont pas stockés comme attributs de `Player` ou `Tournament`.

`RoundController.get_player_score()` parcourt toutes les rondes et tous les matchs du tournoi. Il additionne les scores non nuls associés à l'identifiant national du joueur.

`get_ranking()` trie ensuite `tournament.players` par score décroissant. `get_ranking_with_scores()` fournit directement les couples joueur-score nécessaires à l'affichage.

Cette approche garantit qu'après rechargement d'un tournoi, les scores sont reconstruits automatiquement depuis les résultats persistés.

## 11. Validation des entrées

### `PlayerController`

- nom et prénom : texte non vide après `strip()` ;
- identifiant national : normalisation en majuscules puis expression régulière `[A-Z]{2}[0-9]{5}` ;
- date de naissance : parsing avec `date.fromisoformat()` ;
- unicité de l'identifiant contrôlée lors de la création et de la modification.

### `TournamentController`

- nom, lieu et dates obligatoires ;
- dates validées avec `date.fromisoformat()` ;
- date de fin supérieure ou égale à la date de début ;
- nombre de rondes converti en entier strictement positif, avec valeur 4 par défaut ;
- doublon de participant refusé ;
- ajout et retrait d’un participant interdits après la création de la première ronde ;
- retrait d’un participant inconnu refusé.

### `RoundController`

- création d'une ronde refusée sans participant ou avec un nombre impair ;
- nouvelle ronde interdite tant qu'une ronde précédente est ouverte ;
- nouvelle ronde interdite lorsque le nombre prévu est atteint ;
- clôture refusée tant qu'un résultat manque.

### `MatchController`

- conversion des scores saisis sous forme de chaînes ;
- virgule décimale acceptée puis normalisée ;
- résultat limité aux trois couples autorisés.

Les vues restent responsables de la saisie et de l'affichage, sans appliquer ces validations métier.

## 12. Qualité et vérification

La configuration Flake8 utilise une longueur maximale de 119 caractères.

Contrôle standard :

```bash
flake8 .
```

La vérification directe de la version actuelle ne remonte aucune erreur.

Génération du rapport HTML :

```bash
flake8 --format=html --htmldir=flake8_rapport .
```

Les tests automatisés sont exécutés avec :

```bash
python -m unittest discover -v
```

La version actuelle comporte 75 tests passants.

Les vérifications couvrent notamment :

- validation dans les contrôleurs ;
- représentation interne des modèles ;
- sérialisation et désérialisation ;
- persistance JSON et erreurs de chargement ;
- unicité et tri des joueurs ;
- ajout et retrait des participants avant démarrage ;
- appariements et historique des rencontres ;
- saisie des résultats et calcul des scores ;
- règles de progression des rondes ;
- indépendance des modèles vis-à-vis des vues et contrôleurs.

## 13. Sécurité et robustesse

- aucune donnée sensible ni aucun secret n'est nécessaire ;
- aucune communication réseau n'est effectuée pendant l'usage métier ;
- les chemins sont construits avec `pathlib` ;
- les erreurs JSON sont remontées avec des messages explicites ;
- le registre joueur n'est pas réécrit si son chargement a échoué ;
- les données locales d'utilisation sont séparées du code source et ne sont pas versionnées.

## 14. Validation finale

La simplification de l’architecture a été fusionnée via la **PR GitHub #19 —** `refactor: simplify MVC architecture`.

L’ergonomie console, le contexte global, la gestion homogène de la zone `OUTPUT` et la possibilité de retirer un participant avant le démarrage ont ensuite été fusionnés via la **PR GitHub #20 —** `feat: improve console layout and tournament workflow`.
