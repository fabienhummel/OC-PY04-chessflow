# Documentation de ChessFlow

Ce dossier regroupe les documents de cadrage, de conception, de spécification, de veille et de planification de ChessFlow.

Les documents décrivent l'application telle qu'elle est livrée dans la branche `main`.

## Organisation

| Dossier | Contenu |
| --- | --- |
| [`01-cadrage`](01-cadrage/cahier-des-charges.md) | Contexte, objectifs, périmètre et cahier des charges |
| [`02-specifications`](02-specifications/specifications-fonctionnelles.md) | Spécifications fonctionnelles, techniques et règles métier |
| [`03-conception`](03-conception/diagrammes/README.md) | Diagrammes UML, sources PlantUML et exports SVG |
| [`04-veille`](04-veille/veille-technologique.md) | Comparaison des solutions et justification des choix techniques |
| [`05-backlog`](05-backlog/backlog-produit.md) | User stories, priorités, estimations et plan de réalisation |

## Références de version

- Version documentaire : 1.0 finale
- Date de consolidation : 30 août 2026
- Application cible : ChessFlow 1.0
- Environnement de développement validé : CPython 3.13.9
- Qualité : Flake8 7.3.0 et flake8-html 0.4.3
- Vérification automatisée : 70 tests `unittest`

Les documents sont maintenus en Markdown pour rester lisibles, versionnables et faciles à mettre à jour.
Les diagrammes sont maintenus en PlantUML avec leurs exports SVG correspondants.
