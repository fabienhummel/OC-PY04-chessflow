# Spécifications fonctionnelles de ChessFlow

## 1. Objet et acteur

Ce document décrit ce que ChessFlow doit permettre à l'organisateur ou directeur d'un tournoi d'accomplir, indépendamment de l'implémentation technique.

Les joueurs sont bénéficiaires des informations produites, mais n'utilisent pas directement l'application.

## 2. Principes généraux

| ID | Exigence | Vérification attendue |
| --- | --- | --- |
| SF-GEN-01 | Toutes les fonctions métier sont utilisables sans connexion Internet. | Exécuter le parcours avec le réseau désactivé. |
| SF-GEN-02 | La navigation donne accès aux joueurs, tournois, reprises et rapports. | Atteindre chaque domaine depuis le menu. |
| SF-GEN-03 | L'utilisateur peut revenir ou annuler une saisie sans arrêter l'application. | Annuler une opération et retrouver un état cohérent. |
| SF-GEN-04 | Une saisie invalide produit un message clair et peut être corrigée. | Entrer une valeur invalide puis recommencer. |
| SF-GEN-05 | Une action réussie est confirmée. | Valider une création ou modification. |
| SF-GEN-06 | Une erreur ultérieure ne détruit pas les données déjà validées. | Recharger les données après une opération en échec. |

## 3. Gestion des joueurs

| ID | Exigence | Vérification attendue |
| --- | --- | --- |
| SF-JOU-01 | Créer un joueur avec nom, prénom, date de naissance et identifiant national. | Créer puis retrouver le joueur. |
| SF-JOU-02 | Les quatre informations sont obligatoires. | Tester chaque champ vide. |
| SF-JOU-03 | L'identifiant comporte deux lettres suivies de cinq chiffres. | Tester des formats valides et invalides. |
| SF-JOU-04 | L'identifiant est unique sans distinction de casse. | Tenter un doublon. |
| SF-JOU-05 | L'identifiant est saisi et jamais généré. | Vérifier l'absence de génération automatique. |
| SF-JOU-06 | La date de naissance est une date calendaire valide. | Tester une date impossible. |
| SF-JOU-07 | Un joueur validé est immédiatement sélectionnable pour un tournoi. | Créer puis sélectionner le joueur. |
| SF-JOU-08 | Un joueur est conservé entre deux exécutions. | Redémarrer et consulter le registre. |
| SF-JOU-09 | Tous les joueurs peuvent être affichés. | Afficher un registre rempli. |
| SF-JOU-10 | La liste est triée par nom puis prénom. | Utiliser des données volontairement désordonnées. |
| SF-JOU-11 | L'identifiant permet de distinguer les homonymes. | Afficher deux joueurs homonymes. |
| SF-JOU-12 | Un registre vide est signalé sans erreur. | Ouvrir un environnement neuf. |

La suppression de joueurs et l'import historique sont exclus.

## 4. Gestion des tournois

| ID | Exigence | Vérification attendue |
| --- | --- | --- |
| SF-TOU-01 | Créer un tournoi avec nom, lieu, dates, nombre de rondes et description. | Créer puis consulter le tournoi. |
| SF-TOU-02 | Le nom, le lieu et les dates sont obligatoires. | Omettre successivement chaque donnée. |
| SF-TOU-03 | La date de fin n'est pas antérieure à la date de début. | Tester une période inversée. |
| SF-TOU-04 | Le nombre de rondes vaut 4 par défaut. | Valider sans modifier la valeur. |
| SF-TOU-05 | Le nombre de rondes est un entier strictement positif. | Tester zéro, une valeur négative et du texte. |
| SF-TOU-06 | Un tournoi nouvellement créé ne contient aucune ronde commencée. | Consulter son état initial. |
| SF-TOU-07 | Le tournoi est conservé après redémarrage. | Fermer puis recharger. |
| SF-TOU-08 | Les participants sont sélectionnés dans le registre général. | Sélectionner des joueurs existants. |
| SF-TOU-09 | Un joueur ne peut être inscrit deux fois au même tournoi. | Répéter une sélection. |
| SF-TOU-10 | L'inscription ne modifie pas l'identité globale du joueur. | Comparer avant et après. |
| SF-TOU-11 | Le démarrage est refusé avec un nombre impair de participants. | Préparer trois joueurs puis démarrer. |
| SF-TOU-12 | Le refus permet de corriger la sélection. | Ajouter ou retirer un participant. |
| SF-TOU-13 | Tous les participants commencent à 0 point. | Consulter les scores initiaux. |
| SF-TOU-14 | Tous les tournois enregistrés peuvent être affichés. | Afficher plusieurs tournois. |
| SF-TOU-15 | Un tournoi peut être sélectionné pour consultation ou poursuite. | Ouvrir un tournoi existant. |
| SF-TOU-16 | Une liste vide est signalée sans erreur. | Ouvrir un environnement neuf. |
| SF-TOU-17 | Le détail montre identité, dates, nombre de rondes et avancement. | Comparer un tournoi préparé, en cours et terminé. |

## 5. Déroulement et rondes

| ID | Exigence | Vérification attendue |
| --- | --- | --- |
| SF-DER-01 | Un tournoi conforme avec un nombre pair de participants peut démarrer. | Démarrer un tournoi valide. |
| SF-DER-02 | Le démarrage est refusé si aucune paire ne peut être formée. | Tester zéro ou un participant. |
| SF-DER-03 | L'ouverture restaure l'état exact du tournoi. | Quitter en cours de tournoi puis rouvrir. |
| SF-DER-04 | Participants, scores, ronde courante, rondes et matchs sont restaurés. | Comparer avant et après redémarrage. |
| SF-DER-05 | Un tournoi terminé reste consultable sans nouvelle ronde possible. | Tenter de poursuivre un tournoi terminé. |
| SF-RON-01 | Les rondes sont créées une par une. | Vérifier qu'une seule nouvelle ronde apparaît. |
| SF-RON-02 | Leur nom est séquentiel : `Round 1`, `Round 2`, etc. | Créer plusieurs rondes. |
| SF-RON-03 | Le début est horodaté automatiquement. | Créer puis consulter une ronde. |
| SF-RON-04 | Une nouvelle ronde exige la clôture de la précédente. | Tenter deux rondes simultanées. |
| SF-RON-05 | Le nombre de rondes créées ne dépasse pas la valeur prévue. | Tenter une ronde supplémentaire. |
| SF-RON-06 | Une ronde ne se clôture qu'avec tous ses résultats. | Laisser un match incomplet. |
| SF-RON-07 | La fin est horodatée automatiquement. | Clôturer puis consulter. |
| SF-RON-08 | La clôture actualise les scores cumulés. | Comparer les scores avant et après. |
| SF-RON-09 | Une ronde clôturée reste consultable. | Ouvrir une ronde terminée. |
| SF-RON-10 | Le tournoi se termine après la dernière ronde prévue. | Clôturer la ronde finale. |

## 6. Appariements

| ID | Exigence | Vérification attendue |
| --- | --- | --- |
| SF-APP-01 | La première ronde mélange aléatoirement les participants. | Comparer plusieurs créations équivalentes. |
| SF-APP-02 | Les joueurs sont associés deux par deux sans oubli ni doublon. | Contrôler toutes les occurrences. |
| SF-APP-03 | Le nombre de matchs vaut la moitié du nombre de participants. | Tester 4, 6 et 8 joueurs. |
| SF-APP-04 | Les rondes suivantes utilisent les scores décroissants. | Préparer des scores connus. |
| SF-APP-05 | Les ex æquo peuvent être départagés aléatoirement. | Tester plusieurs égalités. |
| SF-APP-06 | Les adversaires proches au classement sont privilégiés. | Contrôler des paires attendues. |
| SF-APP-07 | Les rencontres déjà jouées sont évitées autant que possible. | Simuler plusieurs rondes. |
| SF-APP-08 | Un cas contraint produit tout de même une ronde complète. | Tester un historique limitant les choix. |
| SF-APP-09 | Chaque participant apparaît exactement une fois par ronde. | Contrôler les paires produites. |

L'optimisation parfaite et l'équilibrage des couleurs ne sont pas requis.

## 7. Matchs et résultats

| ID | Exigence | Vérification attendue |
| --- | --- | --- |
| SF-MAT-01 | Un match oppose exactement deux participants distincts. | Consulter tous les matchs. |
| SF-MAT-02 | L'organisateur choisit victoire du premier, victoire du second ou nul. | Tester les trois résultats. |
| SF-MAT-03 | Une victoire attribue 1 point au gagnant et 0 au perdant. | Enregistrer puis contrôler. |
| SF-MAT-04 | Un nul attribue 0,5 point à chaque joueur. | Enregistrer puis contrôler. |
| SF-MAT-05 | Toute autre combinaison est refusée. | Tester valeurs négatives, 2 points et texte libre. |
| SF-MAT-06 | Un résultat validé est sauvegardé immédiatement. | Quitter après une saisie puis rouvrir. |
| SF-MAT-07 | Les points restent propres au tournoi. | Comparer le même joueur dans deux tournois. |
| SF-MAT-08 | Les coups joués ne sont jamais demandés. | Parcourir la saisie complète. |

## 8. Sauvegarde et reprise

| ID | Exigence | Vérification attendue |
| --- | --- | --- |
| SF-PER-01 | Toute création ou modification validée d'un joueur est sauvegardée. | Redémarrer immédiatement après création. |
| SF-PER-02 | Toute création ou modification validée d'un tournoi est sauvegardée. | Redémarrer immédiatement après création. |
| SF-PER-03 | La sélection des participants est sauvegardée. | Quitter après inscription puis reprendre. |
| SF-PER-04 | La création et la clôture d'une ronde sont sauvegardées. | Quitter après chaque étape. |
| SF-PER-05 | Chaque résultat est sauvegardé sans attendre la fin du tournoi. | Quitter après un seul match. |
| SF-PER-06 | Sans fichier existant, l'application démarre avec des collections vides. | Utiliser un environnement neuf. |
| SF-PER-07 | Un fichier illisible produit une erreur compréhensible. | Présenter un JSON invalide. |
| SF-PER-08 | La reprise continue depuis la dernière action validée. | Interrompre entre deux étapes. |

## 9. Rapports

| ID | Exigence | Vérification attendue |
| --- | --- | --- |
| SF-RAP-01 | Afficher tous les joueurs par nom puis prénom. | Comparer à un jeu désordonné. |
| SF-RAP-02 | Afficher tous les tournois. | Créer plusieurs tournois. |
| SF-RAP-03 | Afficher le nom et les dates d'un tournoi. | Comparer avec la création. |
| SF-RAP-04 | Afficher les participants d'un tournoi par ordre alphabétique. | Inscrire dans un ordre différent. |
| SF-RAP-05 | Afficher toutes les rondes dans leur ordre chronologique. | Consulter un tournoi multi-rondes. |
| SF-RAP-06 | Afficher le nom, les horodatages et les matchs de chaque ronde. | Comparer aux données enregistrées. |
| SF-RAP-07 | Afficher les deux joueurs et le résultat de chaque match. | Comparer ronde en cours et terminée. |
| SF-RAP-08 | Tous les rapports sont consultables dans la console. | Générer sans fichier externe. |
| SF-RAP-09 | L'absence de données produit un message explicite. | Demander un rapport vide. |

## 10. Cohérence globale

| ID | Exigence | Vérification attendue |
| --- | --- | --- |
| SF-COH-01 | Un joueur conserve la même identité dans tous les tournois. | Comparer plusieurs participations. |
| SF-COH-02 | Le score affiché égale la somme des résultats du tournoi. | Recalculer manuellement. |
| SF-COH-03 | Une ronde clôturée contient un résultat par match. | Contrôler les rondes terminées. |
| SF-COH-04 | Le numéro courant correspond à l'avancement réel. | Comparer avant et après clôture. |
| SF-COH-05 | Le tournoi ne se termine qu'après toutes les rondes prévues. | Tester un tournoi multi-rondes. |
| SF-COH-06 | Avec N participants, chaque ronde contient N/2 matchs complets. | Contrôler plusieurs tailles paires. |

## 11. Parcours nominal

1. L'organisateur démarre ChessFlow.
2. Il crée ou consulte les joueurs.
3. Il crée un tournoi et renseigne ses informations.
4. Il sélectionne un nombre pair de participants.
5. Il démarre le tournoi.
6. ChessFlow crée la première ronde avec des appariements aléatoires.
7. L'organisateur saisit les résultats et clôture la ronde.
8. ChessFlow actualise les scores.
9. Les rondes suivantes sont générées selon les scores et l'historique.
10. Le tournoi passe à l'état terminé après la dernière ronde.
11. L'organisateur consulte les rapports.
12. Chaque action validée reste disponible après redémarrage.

