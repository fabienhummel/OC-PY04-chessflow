# Règles métier de ChessFlow

## Joueurs

- Un joueur possède un nom, un prénom, une date de naissance et un identifiant national.
- L'identifiant national est fourni par l'organisateur et suit le format `AA12345`.
- L'identifiant national est unique dans le registre, sans distinction de casse.
- Un joueur existe indépendamment des tournois et peut participer à plusieurs tournois.
- Le score n'appartient pas au joueur global : il est propre à chaque tournoi.
- La suppression d'un joueur n'est pas prévue.

## Tournois

- Un tournoi possède un nom, un lieu, des dates, une description et un nombre de rondes.
- Le nombre de rondes vaut 4 par défaut et doit être strictement positif.
- Un joueur ne peut être inscrit qu'une seule fois au même tournoi.
- Les participants commencent chaque tournoi avec un score égal à 0.
- Le tournoi ne démarre qu'avec au moins deux participants et un nombre pair de joueurs.
- Aucun mécanisme de joueur exempt ou de « bye » n'est géré.
- Un tournoi est terminé lorsque toutes les rondes prévues sont clôturées.

## Rondes

- Les rondes sont créées progressivement, et non lors de la création du tournoi.
- Leur nom suit la séquence `Round 1`, `Round 2`, etc.
- La date et l'heure de début sont enregistrées à la création.
- Une seule ronde peut être en cours dans un tournoi.
- Une ronde ne peut être clôturée que lorsque tous ses matchs possèdent un résultat.
- La date et l'heure de fin sont enregistrées automatiquement à la clôture.

## Matchs et scores

- Un match oppose exactement deux participants distincts.
- Les seuls résultats valides sont `1 / 0`, `0 / 1` et `0,5 / 0,5`.
- Le score cumulé d'un participant est la somme de ses résultats dans le tournoi.
- Les coups joués et la couleur des pièces ne sont pas persistés.

## Appariements

- La première ronde mélange les participants puis les associe deux par deux.
- Les rondes suivantes classent les participants par score décroissant.
- Les ex æquo peuvent être départagés aléatoirement.
- Les adversaires proches au classement sont privilégiés.
- Les rencontres déjà jouées sont évitées autant que possible.
- Une ronde complète reste prioritaire sur l'évitement absolu des répétitions.
- Chaque participant apparaît exactement une fois par ronde.

## Persistance

- Le registre des joueurs et les tournois sont persistés en JSON.
- Toute modification significative est sauvegardée après validation.
- Le chargement reconstruit des instances métier et restaure l'état exact du tournoi.
- Les objets en mémoire et les fichiers locaux doivent rester synchronisés.

## Invariants

1. Deux joueurs ne partagent jamais le même identifiant national.
2. Un participant apparaît au maximum une fois dans un tournoi.
3. Un tournoi ne démarre qu'avec un nombre pair de participants.
4. Un tournoi possède au maximum une ronde non clôturée.
5. Une ronde de N participants contient exactement N/2 matchs.
6. Chaque participant apparaît exactement une fois dans une ronde.
7. Les deux joueurs d'un match sont distincts.
8. Un résultat est uniquement `1/0`, `0/1` ou `0,5/0,5`.
9. Le score cumulé correspond à la somme des résultats du tournoi.
10. Un score de tournoi ne modifie jamais le registre général des joueurs.
11. Une ronde clôturée possède une date de fin et des résultats complets.
12. Le nombre de rondes ne dépasse jamais la valeur prévue.

## Modèle métier retenu

| Classe | Responsabilité | Relation principale |
| --- | --- | --- |
| `Player` | Identité stable d'un joueur | Existe indépendamment des tournois |
| `Tournament` | État et avancement d'un tournoi | Agrège des joueurs et compose des rondes |
| `Round` | Étape du tournoi | Appartient à un tournoi et compose des matchs |
| `Match` | Rencontre et résultat | Appartient à une ronde et référence deux joueurs |

Aucun héritage ni aucune classe abstraite ne sont nécessaires dans le périmètre actuel.

