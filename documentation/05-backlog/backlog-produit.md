# Backlog produit de ChessFlow

## 1. Principes

Les user stories sont priorisées selon MoSCoW et estimées avec les points Fibonacci. Les points expriment une complexité relative et non une durée.

Toutes les stories ci-dessous sont indispensables à la première version. Les améliorations facultatives sont volontairement exclues afin de préserver le périmètre.

## 2. User stories

| ID | User story | Critères d'acceptation synthétiques | Priorité | Points | Lot |
| --- | --- | --- | --- | --- | --- |
| US-01 | En tant qu'organisateur, je veux naviguer dans des menus clairs afin d'accéder aux fonctions sans interrompre l'application. | Joueurs, tournois, reprise et rapports accessibles ; retour et annulation possibles ; saisies invalides corrigibles ; actions confirmées. | Must | 5 | MVC et navigation |
| US-02 | En tant qu'organisateur, je veux ajouter un joueur afin de l'inscrire ensuite à un tournoi. | Quatre champs obligatoires ; date valide ; identifiant au format attendu, unique et non généré ; persistance immédiate. | Must | 5 | Joueurs et données |
| US-03 | En tant qu'organisateur, je veux consulter le registre trié afin de retrouver facilement un joueur. | Tri par nom puis prénom ; identifiant visible ; registre vide géré proprement. | Must | 3 | Joueurs et données |
| US-04 | En tant qu'organisateur, je veux créer un tournoi afin d'enregistrer son cadre et son nombre de rondes. | Informations obligatoires validées ; dates cohérentes ; quatre rondes par défaut ; tournoi restauré après redémarrage. | Must | 5 | Gestion des tournois |
| US-05 | En tant qu'organisateur, je veux sélectionner les participants depuis le registre afin de constituer un tournoi cohérent. | Aucun doublon ; identité inchangée ; score initial nul ; démarrage refusé si le nombre est impair ou inférieur à deux. | Must | 5 | Joueurs et données |
| US-06 | En tant qu'organisateur, je veux démarrer ou reprendre un tournoi afin de poursuivre son déroulement exact. | L'état restauré contient participants, scores, ronde courante, rondes et matchs ; un tournoi terminé reste en lecture seule. | Must | 5 | Gestion des tournois |
| US-07 | En tant qu'organisateur, je veux démarrer la première ronde afin d'obtenir une série complète de matchs aléatoires. | Nom et début automatiques ; joueurs mélangés ; N/2 matchs ; chaque joueur apparaît une fois ; une seule ronde active. | Must | 8 | Appariements |
| US-08 | En tant qu'organisateur, je veux générer les rondes suivantes selon les scores afin d'obtenir des appariements pertinents. | Classement par score ; égalités aléatoires ; adversaires proches ; revanches évitées si possible ; ronde complète. | Must | 8 | Appariements |
| US-09 | En tant qu'organisateur, je veux saisir les résultats afin de calculer les scores du tournoi. | Seuls les trois résultats valides sont acceptés ; sauvegarde immédiate ; score propre au tournoi. | Must | 5 | Gestion des tournois |
| US-10 | En tant qu'organisateur, je veux clôturer une ronde puis le tournoi afin de figer les résultats et l'avancement. | Tous les matchs renseignés ; fin automatique ; scores recalculés ; tournoi terminé après la dernière ronde. | Must | 5 | Gestion des tournois |
| US-11 | En tant qu'organisateur, je veux que les données soient sauvegardées localement afin de ne perdre aucune action validée. | Persistance JSON complète ; environnement neuf accepté ; fichier illisible signalé ; données valides préservées. | Must | 8 | Joueurs et données |
| US-12 | En tant qu'organisateur, je veux consulter les tournois afin de suivre leur état. | Liste complète ; détail du tournoi ; avancement visible ; absence de données signalée. | Must | 3 | Rapports |
| US-13 | En tant qu'organisateur, je veux consulter les participants d'un tournoi afin d'obtenir une liste alphabétique fiable. | Tous les participants sont triés par nom puis prénom sans modifier leur identité globale. | Must | 2 | Rapports |
| US-14 | En tant qu'organisateur, je veux consulter les rondes et matchs afin d'obtenir l'historique complet du tournoi. | Rondes chronologiques ; horodatages ; deux joueurs et résultat par match ; absence de données gérée. | Must | 3 | Rapports |
| US-15 | En tant que mainteneur, je veux une application contrôlée et documentée afin de pouvoir l'installer et la vérifier. | Parcours fonctionnel vérifié ; MVC et POO contrôlés ; Flake8 sans erreur ; README et dépendances à jour. | Must | 8 | Finalisation |

**Total indicatif : 78 points.**

## 3. Plan de réalisation

| Lot | Objectif | User stories principales |
| --- | --- | --- |
| Modèles métier | Construire `Player`, `Match`, `Round` et `Tournament` | Préparation de US-02, US-04 et US-07 |
| Joueurs et données | Sérialiser, persister et gérer le registre | US-02, US-03, US-05, US-11 |
| Gestion des tournois | Mettre en place MVC et le parcours du tournoi | US-01, US-04, US-06, US-09, US-10 |
| Appariements et rapports | Produire les paires et restituer les informations | US-07, US-08, US-12, US-13, US-14 |
| Finalisation | Tester, corriger et documenter | US-15 et validation globale |

## 4. Éléments exclus

| Élément | Justification |
| --- | --- |
| Nombre impair et joueur exempt | Seuls les nombres pairs sont pris en charge |
| Suppression de joueurs | Hors périmètre de la première version |
| Import historique | Non nécessaire au démarrage |
| Comptes et authentification | Application locale utilisée par un organisateur |
| Synchronisation distante | Fonctionnement hors ligne requis |
| Notation détaillée des coups | Seul le résultat est mémorisé |
| Classement Elo | Donnée externe à ChessFlow |
| Équilibrage avancé des couleurs | Non requis |
| Optimisation parfaite des appariements | Une solution complète et raisonnable suffit |
| Export PDF ou tableur | Les rapports sont consultés en console |

## 5. Definition of Ready

Une story peut être développée lorsque :

- sa valeur pour l'utilisateur est explicite ;
- ses critères d'acceptation sont testables ;
- les règles métier et dépendances sont connues ;
- aucune décision fonctionnelle bloquante ne reste ouverte.

## 6. Definition of Done

Une story est terminée lorsque :

- les critères d'acceptation sont vérifiés ;
- les erreurs utilisateur prévues sont gérées ;
- les données validées sont sauvegardées lorsque nécessaire ;
- le code respecte l'architecture MVC et la POO ;
- Flake8 ne signale aucune erreur ;
- la documentation associée est à jour.

