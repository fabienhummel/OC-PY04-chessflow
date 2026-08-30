# Règles métier de ChessFlow

## Joueurs

- Un joueur possède un nom, un prénom, une date de naissance et un identifiant national.
- Le nom et le prénom sont obligatoires.
- La date de naissance doit être une date calendaire valide au format ISO `YYYY-MM-DD`.
- L'identifiant national est fourni par l'organisateur et suit le format `AA12345`.
- L'identifiant national est normalisé en majuscules et unique dans le registre.
- Un joueur existe indépendamment des tournois et peut participer à plusieurs tournois.
- Le score n'appartient pas au joueur global : il est calculé dans le contexte d'un tournoi.
- Un joueur peut être recherché, modifié ou supprimé dans le registre général.
- Une modification réutilise les mêmes validations que la création.
- La suppression du registre général ne modifie pas les participants déjà enregistrés dans les fichiers de tournois.

## Tournois

- Un tournoi possède un nom, un lieu, des dates, une description et un nombre de rondes.
- Le nom, le lieu et les dates sont obligatoires.
- La date de fin ne peut pas être antérieure à la date de début.
- Le nombre de rondes vaut 4 par défaut et doit être strictement positif.
- Un joueur ne peut être inscrit qu'une seule fois au même tournoi.
- Les participants peuvent être ajoutés uniquement tant qu'aucune ronde n'a été créée.
- La première ronde ne peut être créée qu'avec au moins deux participants et un nombre pair de joueurs.
- Aucun mécanisme de joueur exempt ou de « bye » n'est géré.
- Le nombre de rondes créées ne peut pas dépasser le nombre prévu.
- Un tournoi n'a pas de statut persisté distinct : son avancement est représenté par `current_round` et ses rondes.
- Lorsque la dernière ronde prévue est clôturée, aucune nouvelle ronde ne peut être créée.

## Rondes

- Les rondes sont créées progressivement, et non lors de la création du tournoi.
- Leur nom suit la séquence `Round 1`, `Round 2`, etc.
- La date et l'heure de début sont enregistrées lors de la création par le contrôleur de tournoi.
- Une seule ronde peut être en cours dans un tournoi.
- Une nouvelle ronde ne peut être créée tant que la précédente n'est pas clôturée.
- Une ronde ne peut être clôturée que lorsque tous ses matchs possèdent un résultat.
- La date et l'heure de fin sont enregistrées automatiquement à la clôture.

## Matchs et scores

- Un match oppose exactement deux participants distincts.
- La représentation interne d'un match est un tuple contenant deux listes mutables : `([joueur1, score1], [joueur2, score2])`.
- Les propriétés `player_one`, `player_two`, `score_one` et `score_two` exposent les éléments de cette structure.
- Les seuls résultats valides sont `1 / 0`, `0 / 1` et `0,5 / 0,5`.
- Un résultat peut être saisi puis modifié.
- Le score cumulé d'un participant est calculé en parcourant les matchs du tournoi.
- Aucun score cumulé n'est stocké dans l'objet `Player` ni dans un dictionnaire séparé du tournoi.
- Les coups joués et la couleur des pièces ne sont pas persistés.

## Appariements

- La première ronde mélange une copie de la liste des participants puis les associe deux par deux.
- Les rondes suivantes utilisent un classement par score décroissant.
- Le tri Python étant stable, les joueurs à égalité conservent leur ordre relatif dans la liste des participants.
- Pour chaque joueur, l'algorithme recherche le premier adversaire disponible qu'il n'a pas encore rencontré.
- Si aucun adversaire inédit n'est disponible, le premier adversaire restant est utilisé.
- Une ronde complète reste prioritaire sur l'évitement absolu des répétitions.
- Chaque participant apparaît exactement une fois dans une ronde générée.

## Persistance

- Le registre des joueurs et les tournois sont persistés en JSON.
- `data/players.json` contient le registre général.
- `data/tournaments/` contient un fichier JSON par tournoi.
- Toute modification significative est sauvegardée après validation.
- Le chargement reconstruit des instances métier à partir des données JSON.
- Les scores ne sont pas restaurés comme une donnée séparée : ils sont recalculés depuis les résultats des matchs.
- Un fichier joueur absent correspond à une collection vide.
- Un fichier JSON vide, invalide ou de structure incorrecte produit une erreur explicite.
- Si le registre des joueurs ne peut pas être chargé, les écritures sur ce registre sont bloquées afin d'éviter d'écraser les données existantes.

## Invariants

1. Deux joueurs ne partagent jamais le même identifiant national dans le registre général.
2. Un participant apparaît au maximum une fois dans un tournoi.
3. Aucun participant ne peut être ajouté après la création de la première ronde.
4. Une ronde ne peut être créée qu'avec un nombre pair de participants et au moins une paire.
5. Un tournoi possède au maximum une ronde non clôturée.
6. Une ronde de N participants contient exactement N/2 matchs.
7. Chaque participant apparaît exactement une fois dans une ronde générée.
8. Les deux joueurs d'un match sont distincts.
9. Un résultat est uniquement `1/0`, `0/1` ou `0,5/0,5`.
10. Le score cumulé correspond à la somme des résultats enregistrés dans le tournoi.
11. Un score de tournoi ne modifie jamais le registre général des joueurs.
12. Une ronde clôturée possède une date de fin et des résultats complets.
13. Le nombre de rondes créées ne dépasse jamais la valeur prévue.

## Modèle métier retenu

| Classe | Responsabilité | Relation principale |
| --- | --- | --- |
| `Player` | Identité et validation d'un joueur | Existe indépendamment des tournois |
| `Tournament` | Informations, participants, rondes et avancement | Agrège des joueurs et contient des rondes |
| `Round` | Étape du tournoi et collection de matchs | Appartient au tournoi |
| `Match` | Paire de joueurs et résultat | Appartient à une ronde et référence deux joueurs |

Le calcul des scores, le classement, les appariements, la sauvegarde et les règles de progression sont orchestrés par les contrôleurs.

Aucun héritage ni aucune classe abstraite ne sont nécessaires dans le périmètre actuel.
