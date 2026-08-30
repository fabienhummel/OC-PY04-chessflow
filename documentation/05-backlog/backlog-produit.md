# Backlog produit de ChessFlow

## 1. Principes

Les user stories sont priorisées selon MoSCoW et estimées avec les points Fibonacci. Les points expriment une complexité relative et non une durée.

Ce backlog conserve la logique de réalisation du projet tout en reflétant les fonctionnalités effectivement livrées dans ChessFlow 1.0.

## 2. User stories

| ID | User story | Critères d'acceptation synthétiques | Priorité | Points | Lot | État |
| --- | --- | --- | --- | --- | --- | --- |
| US-01 | En tant qu'organisateur, je veux naviguer dans des menus clairs afin d'accéder aux fonctions sans interrompre l'application. | Joueurs, tournois et rapports accessibles ; `0` permet de revenir dans les sous-menus ; saisies invalides gérées. | Must | 5 | MVC et navigation | Livré |
| US-02 | En tant qu'organisateur, je veux ajouter un joueur afin de l'inscrire ensuite à un tournoi. | Champs obligatoires ; date valide ; identifiant au format attendu, unique et non généré ; persistance immédiate. | Must | 5 | Joueurs et données | Livré |
| US-03 | En tant qu'organisateur, je veux consulter et rechercher le registre afin de retrouver facilement un joueur. | Tri par nom puis prénom ; identifiant visible ; recherche par identifiant ; registre vide géré. | Must | 3 | Joueurs et données | Livré |
| US-04 | En tant qu'organisateur, je veux modifier ou supprimer un joueur afin de maintenir le registre général. | Modification revalidée ; unicité préservée ; suppression persistée. | Should | 5 | Joueurs et données | Livré |
| US-05 | En tant qu'organisateur, je veux créer un tournoi afin d'enregistrer son cadre et son nombre de rondes. | Informations obligatoires validées ; dates cohérentes ; quatre rondes par défaut ; tournoi restauré après redémarrage. | Must | 5 | Gestion des tournois | Livré |
| US-06 | En tant qu'organisateur, je veux sélectionner les participants depuis le registre afin de constituer un tournoi cohérent. | Aucun doublon ; ajout uniquement avant `Round 1` ; ronde refusée si le nombre est impair ou insuffisant. | Must | 5 | Joueurs et données | Livré |
| US-07 | En tant qu'organisateur, je veux charger un tournoi afin de poursuivre son déroulement exact. | Participants, ronde courante, rondes, matchs et résultats sont restaurés. | Must | 5 | Gestion des tournois | Livré |
| US-08 | En tant qu'organisateur, je veux démarrer la première ronde afin d'obtenir une série complète de matchs aléatoires. | Nom et début automatiques ; joueurs mélangés ; N/2 matchs ; chaque joueur apparaît une fois ; une seule ronde active. | Must | 8 | Appariements | Livré |
| US-09 | En tant qu'organisateur, je veux générer les rondes suivantes selon les scores afin d'obtenir des appariements pertinents. | Classement par score ; ordre stable à égalité ; revanches évitées si possible ; ronde complète. | Must | 8 | Appariements | Livré |
| US-10 | En tant qu'organisateur, je veux saisir ou corriger les résultats afin de calculer les scores du tournoi. | Seuls les trois résultats valides sont acceptés ; sauvegarde immédiate ; modification possible ; score propre au tournoi. | Must | 5 | Gestion des tournois | Livré |
| US-11 | En tant qu'organisateur, je veux clôturer une ronde afin de poursuivre le tournoi. | Tous les matchs renseignés ; fin automatique ; nouvelle ronde autorisée ensuite. | Must | 5 | Gestion des tournois | Livré |
| US-12 | En tant qu'organisateur, je veux que les données soient sauvegardées localement afin de ne perdre aucune action validée. | Persistance JSON ; environnement neuf accepté ; fichiers invalides signalés ; registre protégé après erreur de chargement. | Must | 8 | Joueurs et données | Livré |
| US-13 | En tant qu'organisateur, je veux consulter les tournois afin de suivre leur état. | Liste complète ; détail du tournoi ; avancement visible ; absence de données signalée. | Must | 3 | Rapports | Livré |
| US-14 | En tant qu'organisateur, je veux consulter les participants d'un tournoi afin d'obtenir une liste alphabétique fiable. | Tous les participants sont triés par nom puis prénom. | Must | 2 | Rapports | Livré |
| US-15 | En tant qu'organisateur, je veux consulter les rondes, matchs et classements afin d'obtenir l'historique du tournoi. | Rondes et horodatages ; deux joueurs et résultat par match ; classement avec scores calculés. | Must | 5 | Rapports | Livré |
| US-16 | En tant que mainteneur, je veux une application contrôlée et documentée afin de pouvoir l'installer et la vérifier. | Tests passants ; MVC et POO contrôlés ; Flake8 sans erreur ; rapport HTML ; README et dépendances à jour. | Must | 8 | Finalisation | Livré |

## 3. Plan de réalisation

| Lot | Objectif | User stories principales |
| --- | --- | --- |
| Modèles métier | Construire `Player`, `Match`, `Round` et `Tournament` | Préparation de US-02, US-05 et US-08 |
| Joueurs et données | Sérialiser, persister et gérer le registre | US-02, US-03, US-04, US-06, US-12 |
| Gestion des tournois | Mettre en place MVC et le parcours du tournoi | US-01, US-05, US-07, US-10, US-11 |
| Appariements et rapports | Produire les paires et restituer les informations | US-08, US-09, US-13, US-14, US-15 |
| Finalisation | Tester, corriger et documenter | US-16 et validation globale |

## 4. Éléments exclus

| Élément | Justification |
| --- | --- |
| Nombre impair et joueur exempt | Seuls les nombres pairs sont pris en charge |
| Import historique | Non nécessaire au démarrage |
| Comptes et authentification | Application locale utilisée par un organisateur |
| Synchronisation distante | Fonctionnement hors ligne requis |
| Notation détaillée des coups | Seul le résultat est mémorisé |
| Classement Elo | Donnée externe à ChessFlow |
| Équilibrage avancé des couleurs | Non requis |
| Optimisation exhaustive des appariements | Une solution complète et raisonnable suffit |
| Export PDF ou tableur | Les rapports sont consultés en console |

## 5. Fonctionnalités complémentaires livrées

La recherche, la modification et la suppression des joueurs ne sont pas nécessaires au parcours minimal d'un tournoi, mais elles sont présentes dans la version finale afin de rendre le registre plus utilisable.

La modification d'un résultat déjà saisi est également disponible.

## 6. Definition of Ready

Une story peut être développée lorsque :

- sa valeur pour l'utilisateur est explicite ;
- ses critères d'acceptation sont testables ;
- les règles métier et dépendances sont connues ;
- aucune décision fonctionnelle bloquante ne reste ouverte.

## 7. Definition of Done

Une story est terminée lorsque :

- les critères d'acceptation sont vérifiés ;
- les erreurs utilisateur prévues sont gérées ;
- les données validées sont sauvegardées lorsque nécessaire ;
- le code respecte l'architecture MVC et la POO ;
- les tests concernés passent ;
- Flake8 ne signale aucune erreur ;
- la documentation associée est à jour.
