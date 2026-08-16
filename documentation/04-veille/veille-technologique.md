# Veille technologique de ChessFlow

## 1. Objectif et méthode

Cette veille compare les solutions adaptées aux contraintes de ChessFlow : application hors ligne, console Python, architecture MVC, persistance locale, qualité PEP 8 et diagrammes versionnables.

Les choix sont évalués selon cinq critères :

1. conformité au besoin ;
2. simplicité de mise en œuvre ;
3. portabilité ;
4. maintenabilité ;
5. disponibilité d'une documentation officielle.

La préférence est donnée aux technologies standard, maintenues et proportionnées à la taille du projet.

## 2. Langage et environnement Python

Python est retenu pour son support multiplateforme, sa bibliothèque standard et son adéquation à la programmation orientée objet.

### Isolation de l'environnement

| Option | Avantages | Limites | Décision |
| --- | --- | --- | --- |
| `venv` + `pip` | Standard Python, léger, portable, sans outil supplémentaire | Gestion des dépendances moins avancée | Retenu |
| Conda | Gestion complète des environnements et paquets natifs | Plus lourd et inutile pour ce projet | Non retenu |
| Poetry | Résolution et publication modernes | Outil supplémentaire sans besoin de packaging | Non retenu |

La version de développement validée est CPython 3.13.9. Le projet utilise `.venv`, `pip` et `requirements.txt`.

## 3. Architecture applicative

| Option | Avantages | Limites | Décision |
| --- | --- | --- | --- |
| Script monolithique | Démarrage rapide | Responsabilités mélangées, maintenance difficile | Non retenu |
| MVC léger | Séparation des modèles, vues et contrôleurs | Nécessite une organisation initiale | Retenu |
| Architecture hexagonale | Forte indépendance des adaptateurs | Surdimensionnée pour une application console de cette taille | Non retenu |

Le MVC léger répond directement au besoin de séparation des responsabilités sans multiplier les couches.

## 4. Persistance

| Option | Avantages | Limites | Décision |
| --- | --- | --- | --- |
| JSON | Lisible, standard, hors ligne, simple à sauvegarder | Requêtes et concurrence limitées | Retenu |
| SQLite | Transactions et requêtes structurées | Schéma et couche d'accès supplémentaires | Évolution possible |
| Base distante | Accès partagé et centralisé | Réseau requis, complexité et coût | Exclu |

JSON satisfait la portabilité et la simplicité demandées. SQLite pourra être étudié dans une version ultérieure si le volume ou les besoins de recherche augmentent.

## 5. Interface utilisateur

| Option | Avantages | Limites | Décision |
| --- | --- | --- | --- |
| Console standard | Hors ligne, aucune dépendance graphique, portable | Présentation limitée | Retenu |
| Tkinter | Interface graphique incluse avec Python | Développement et tests supplémentaires | Non requis |
| Application web locale | Interface riche | Serveur et navigateur à gérer | Hors périmètre |

L'interface console est suffisante pour les menus, les saisies et les rapports demandés.

## 6. Qualité du code

| Option | Avantages | Limites | Décision |
| --- | --- | --- | --- |
| Flake8 | Contrôle PEP 8 éprouvé, configuration simple | Ne formate pas automatiquement | Retenu |
| Ruff | Très rapide et large couverture | Ne répond pas à l'exigence explicite de rapport Flake8 | Complément éventuel uniquement |
| Pylint | Analyse approfondie | Plus verbeux et configuration plus lourde | Non retenu |

La chaîne retenue utilise Flake8 7.3.0 et flake8-html 0.4.3, avec une longueur maximale de 119 caractères.

## 7. Diagrammes UML

| Option | Avantages | Limites | Décision |
| --- | --- | --- | --- |
| PlantUML | Source texte versionnable, nombreux diagrammes, exports reproductibles | Nécessite un moteur de rendu | Retenu |
| Mermaid | Très bonne intégration Markdown | UML moins complet pour certaines notations | Alternative légère |
| Outil graphique uniquement | Édition visuelle immédiate | Diff Git difficile et risque de source non reproductible | Non retenu comme source principale |

Les sources PlantUML sont conservées avec leurs exports SVG. Les deux formats doivent rester synchronisés.

## 8. Gestion des dates et chemins

- `datetime` et `date` de la bibliothèque standard sont retenus pour les dates et horodatages ;
- ISO 8601 est utilisé dans les fichiers JSON ;
- `pathlib` est préféré aux chemins concaténés manuellement pour assurer la portabilité.

## 9. Architecture technique retenue

| Domaine | Décision |
| --- | --- |
| Exécution | Application console Python locale |
| Python | CPython 3.13.9 pour le développement |
| Isolation | `.venv` standard |
| Métier | Quatre classes principales en POO |
| Structure | MVC léger |
| Persistance | JSON local |
| Dépendances | Bibliothèque standard autant que possible |
| Qualité | Flake8 7.3.0 et limite 119 |
| Rapport | flake8-html 0.4.3 |
| UML | PlantUML et SVG |
| Versionnement | Git et branches de fonctionnalité |

## 10. Points de vigilance

- vérifier les dépendances avant toute montée de version de Python ;
- conserver une version fonctionnelle de flake8-html ;
- sécuriser les écritures JSON et valider les données chargées ;
- empêcher les modèles d'appeler directement la console ;
- éviter les classes et services sans responsabilité concrète ;
- régénérer les SVG après chaque modification PlantUML ;
- ne jamais coder de chemin spécifique à macOS.

## 11. Sources principales

- [Documentation Python 3.13 - environnements virtuels](https://docs.python.org/fr/3.13/library/venv.html)
- [Documentation Python - module JSON](https://docs.python.org/3/library/json.html)
- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Documentation Flake8 7.3.0](https://flake8.pycqa.org/en/7.3.0/)
- [Flake8 sur PyPI](https://pypi.org/project/flake8/)
- [flake8-html sur PyPI](https://pypi.org/project/flake8-html/)
- [PlantUML - diagrammes de classes](https://plantuml.com/fr/class-diagram)
- [Mermaid - diagrammes de classes](https://mermaid.js.org/syntax/classDiagram.html)

