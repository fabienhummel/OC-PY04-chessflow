# Spécifications techniques de ChessFlow

## 1. Architecture générale

ChessFlow est une application console Python autonome organisée selon une architecture MVC légère.

```text
Utilisateur
    |
    v
Vues console <-> Contrôleurs -> Modèles métier
                    |                |
                    +-------> Persistance JSON
```

### Responsabilités

- **Modèles** : représenter les données et règles métier.
- **Vues** : afficher les informations et recueillir les saisies.
- **Contrôleurs** : orchestrer la navigation, les validations, les modèles et la persistance.
- **Point d'entrée** : initialiser l'application et lancer le contrôleur principal.

Les modèles ne doivent ni appeler `input()` ni afficher directement des informations.

## 2. Environnement

| Élément | Choix retenu |
| --- | --- |
| Langage | Python |
| Version de développement | CPython 3.13.9 |
| Isolation | Environnement virtuel `.venv` |
| Gestion des dépendances | `pip` et `requirements.txt` |
| Interface | Console |
| Persistance | Fichiers JSON locaux |
| Qualité | Flake8 7.3.0, longueur maximale 119 |
| Rapport qualité | flake8-html 0.4.3 |
| Diagrammes | PlantUML et exports SVG |
| Plateformes cibles | macOS, Windows et Linux |

L'application privilégie la bibliothèque standard. Les dépendances de développement sont déclarées explicitement.

## 3. Arborescence cible

```text
OC-PY04-chessflow/
├── controllers/
├── models/
├── views/
├── data/
│   ├── players.json
│   └── tournaments/
├── documentation/
├── flake8_rapport/
├── main.py
├── requirements.txt
├── .flake8
└── README.md
```

Les fichiers et dossiers générés localement, comme `.venv`, `__pycache__`, les métadonnées d'IDE et les caches, sont exclus par `.gitignore`.

## 4. Modèles métier

### `Player`

Attributs essentiels : nom, prénom, date de naissance et identifiant national.

Responsabilités :

- valider son identité et le format de son identifiant ;
- fournir une représentation sérialisable ;
- être reconstruit depuis des données JSON.

### `Tournament`

Attributs essentiels : nom, lieu, dates, description, nombre de rondes, ronde courante, participants, scores et rondes.

Responsabilités :

- inscrire des joueurs sans doublon ;
- vérifier les conditions de démarrage ;
- conserver les scores propres au tournoi ;
- gérer l'avancement et la création des rondes ;
- fournir les données nécessaires aux appariements.

### `Round`

Attributs essentiels : nom, début, fin et matchs.

Responsabilités :

- contenir les matchs de la ronde ;
- vérifier que tous les résultats sont renseignés ;
- enregistrer automatiquement l'heure de fin à la clôture.

### `Match`

Attributs essentiels : deux références de joueurs et leurs scores.

Responsabilités :

- garantir deux joueurs distincts ;
- accepter uniquement les trois résultats valides ;
- exposer une structure sérialisable compatible JSON.

## 5. Relations UML

| Relation | Type | Cardinalité |
| --- | --- | --- |
| `Tournament` - `Player` | Agrégation | Un tournoi agrège 2..* joueurs ; un joueur participe à 0..* tournois |
| `Tournament` - `Round` | Composition | Un tournoi compose 0..* rondes ; une ronde appartient à un tournoi |
| `Round` - `Match` | Composition | Une ronde compose 1..* matchs ; un match appartient à une ronde |
| `Match` - `Player` | Association | Un match référence exactement deux joueurs |

Aucune classe abstraite ni hiérarchie d'héritage ne sont justifiées.

## 6. Persistance JSON

### Organisation

- `data/players.json` : registre général des joueurs ;
- `data/tournaments/` : un ou plusieurs fichiers de tournois.

### Principes

- les écritures utilisent `pathlib` et l'encodage UTF-8 ;
- les dossiers manquants sont créés proprement ;
- toute modification validée déclenche une sauvegarde ;
- les dates et heures utilisent un format ISO 8601 ;
- les chargements reconstruisent les objets métier ;
- un fichier absent correspond à une collection vide ;
- un JSON illisible déclenche une erreur explicite sans écraser les données existantes.

Une écriture temporaire suivie d'un remplacement atomique est recommandée pour limiter le risque de fichier partiellement écrit.

## 7. Algorithme d'appariement

### Première ronde

1. copier la liste des participants ;
2. la mélanger aléatoirement ;
3. associer les joueurs consécutifs ;
4. vérifier que chaque joueur apparaît exactement une fois.

### Rondes suivantes

1. classer les participants par score décroissant ;
2. mélanger les joueurs à égalité ;
3. sélectionner pour chaque joueur disponible l'adversaire disponible le plus proche ;
4. préférer un adversaire jamais rencontré ;
5. autoriser une répétition uniquement si elle est nécessaire pour produire une ronde complète.

L'objectif est un algorithme lisible et explicable, pas une optimisation exhaustive du système suisse.

## 8. Validation des entrées

- identifiant national : expression régulière `^[A-Za-z]{2}\d{5}$` puis normalisation en majuscules ;
- date de naissance et dates de tournoi : parsing contrôlé ;
- fin du tournoi supérieure ou égale au début ;
- nombre de rondes entier strictement positif ;
- nombre de participants pair et supérieur ou égal à deux ;
- résultat limité aux couples autorisés.

Les erreurs utilisateur sont affichées par les vues et permettent une nouvelle saisie.

## 9. Qualité et vérification

La configuration Flake8 utilise une longueur maximale de 119 caractères. Le contrôle standard est :

```bash
flake8 .
```

Le rapport HTML est généré dans `flake8_rapport` avec :

```bash
flake8 --format=html --htmldir=flake8_rapport .
```

Les vérifications doivent couvrir au minimum :

- création et validation des quatre modèles ;
- sérialisation et désérialisation ;
- calcul des trois résultats possibles ;
- appariements avec et sans historique ;
- interruption et reprise d'un tournoi ;
- respect des invariants métier ;
- parcours console nominal.

## 10. Sécurité et robustesse

- aucune donnée sensible ni aucun secret n'est nécessaire ;
- aucune communication réseau n'est effectuée pendant l'usage métier ;
- les chemins sont construits avec `pathlib` ;
- les données chargées sont validées avant reconstruction des objets ;
- les fichiers valides ne sont pas écrasés après une erreur de lecture ou de validation.

