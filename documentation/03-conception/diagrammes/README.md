# Diagrammes de ChessFlow

Ce dossier contient les diagrammes de conception alignés sur ChessFlow 1.0.

## Organisation

- `sources/` : sources PlantUML faisant foi ;
- `exports/` : rendus SVG correspondant aux sources.

## Diagrammes

- `cas-utilisation-chessflow` : fonctions réellement accessibles à l'organisateur dans l'application console ;
- `classes-metier-chessflow` : modèle objet livré `Player`, `Tournament`, `Round` et `Match`.

Le diagramme de cas d'utilisation a été revérifié après la simplification architecturale : les fonctionnalités utilisateur n'ont pas changé.

Le diagramme de classes métier a été mis à jour le 6 septembre 2026 pour refléter les modèles simplifiés. Les validations et règles applicatives sont désormais portées par `PlayerController`, `TournamentController`, `RoundController` et `MatchController`.

Toute modification fonctionnelle ou structurelle doit d'abord être reportée dans le fichier `.puml`, puis dans l'export SVG correspondant.
