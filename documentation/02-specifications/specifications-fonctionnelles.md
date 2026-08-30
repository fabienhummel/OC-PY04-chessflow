# Spécifications fonctionnelles de ChessFlow

## 1. Objet et acteur

Ce document décrit les fonctions effectivement disponibles dans ChessFlow 1.0 pour l'organisateur ou directeur d'un tournoi.

Les joueurs sont bénéficiaires des informations produites, mais n'utilisent pas directement l'application.

## 2. Principes généraux

| ID | Fonction livrée | Vérification attendue |
| --- | --- | --- |
| SF-GEN-01 | Toutes les fonctions métier sont utilisables sans connexion Internet. | Exécuter le parcours avec le réseau désactivé. |
| SF-GEN-02 | Le menu principal donne accès aux joueurs, tournois et rapports. | Atteindre chaque domaine depuis le menu. |
| SF-GEN-03 | Tous les sous-menus utilisent `0` pour revenir au menu précédent. | Parcourir les menus puis revenir avec `0`. |
| SF-GEN-04 | Une saisie métier invalide produit un message clair et n'est pas enregistrée. | Entrer une valeur invalide puis vérifier les données. |
| SF-GEN-05 | Une erreur de chargement JSON est signalée explicitement. | Présenter un fichier vide ou invalide. |
| SF-GEN-06 | Une erreur de lecture du registre joueur bloque les écritures sur ce registre. | Provoquer une erreur de chargement puis tenter une modification. |

## 3. Gestion des joueurs

| ID | Fonction livrée | Vérification attendue |
| --- | --- | --- |
| SF-JOU-01 | Créer un joueur avec nom, prénom, date de naissance et identifiant national. | Créer puis retrouver le joueur. |
| SF-JOU-02 | Le nom et le prénom sont obligatoires. | Tester chaque champ vide. |
| SF-JOU-03 | La date de naissance doit être une date calendaire valide au format `YYYY-MM-DD`. | Tester une date impossible. |
| SF-JOU-04 | L'identifiant comporte deux lettres suivies de cinq chiffres. | Tester des formats valides et invalides. |
| SF-JOU-05 | L'identifiant est normalisé en majuscules et unique. | Créer `ab12345` puis tenter `AB12345`. |
| SF-JOU-06 | L'identifiant est saisi et jamais généré. | Vérifier l'absence de génération automatique. |
| SF-JOU-07 | Un joueur validé est immédiatement sélectionnable pour un tournoi. | Créer puis sélectionner le joueur. |
| SF-JOU-08 | Un joueur est conservé entre deux exécutions. | Redémarrer et consulter le registre. |
| SF-JOU-09 | Tous les joueurs peuvent être affichés. | Afficher un registre rempli. |
| SF-JOU-10 | La liste est triée par nom puis prénom sans modifier l'ordre de stockage. | Utiliser des données volontairement désordonnées. |
| SF-JOU-11 | Un joueur peut être recherché par identifiant national. | Rechercher un identifiant existant puis absent. |
| SF-JOU-12 | Un joueur peut être modifié. Un champ laissé vide conserve sa valeur actuelle. | Modifier un champ et conserver les autres. |
| SF-JOU-13 | Les validations de création s'appliquent aussi à la modification. | Tester date ou identifiant invalide lors d'une modification. |
| SF-JOU-14 | Un joueur peut être supprimé du registre général. | Supprimer puis vérifier la liste. |
| SF-JOU-15 | Un registre vide est signalé sans erreur. | Ouvrir un environnement neuf. |

La suppression d'un joueur du registre général ne réécrit pas les tournois déjà sauvegardés.

## 4. Gestion des tournois

| ID | Fonction livrée | Vérification attendue |
| --- | --- | --- |
| SF-TOU-01 | Créer un tournoi avec nom, lieu, dates, nombre de rondes et description. | Créer puis consulter le tournoi. |
| SF-TOU-02 | Le nom, le lieu et les dates sont obligatoires. | Omettre successivement chaque donnée. |
| SF-TOU-03 | La date de fin n'est pas antérieure à la date de début. | Tester une période inversée. |
| SF-TOU-04 | Le nombre de rondes vaut 4 par défaut. | Valider sans saisir de valeur. |
| SF-TOU-05 | Le nombre de rondes est un entier strictement positif. | Tester zéro, une valeur négative et du texte. |
| SF-TOU-06 | Un tournoi nouvellement créé ne contient aucune ronde commencée. | Consulter son état initial. |
| SF-TOU-07 | Le tournoi est conservé après redémarrage. | Fermer puis recharger. |
| SF-TOU-08 | Les participants sont sélectionnés dans le registre général. | Sélectionner des joueurs existants. |
| SF-TOU-09 | Un joueur ne peut être inscrit deux fois au même tournoi. | Répéter une sélection. |
| SF-TOU-10 | L'inscription ne modifie pas l'identité globale du joueur. | Comparer avant et après. |
| SF-TOU-11 | Aucun participant ne peut être ajouté après la création de la première ronde. | Créer `Round 1` puis tenter un ajout. |
| SF-TOU-12 | La création d'une ronde est refusée avec un nombre impair de participants. | Préparer trois joueurs puis créer la ronde. |
| SF-TOU-13 | Au moins une paire de joueurs est nécessaire pour créer une ronde. | Tester zéro ou un participant. |
| SF-TOU-14 | Tous les tournois enregistrés peuvent être affichés. | Afficher plusieurs tournois. |
| SF-TOU-15 | Un tournoi peut être chargé pour consultation ou poursuite. | Ouvrir un tournoi existant. |
| SF-TOU-16 | Une liste vide est signalée sans erreur. | Ouvrir un environnement neuf. |
| SF-TOU-17 | Le détail montre identité, dates, nombre de rondes, ronde courante et nombre de joueurs. | Comparer les données affichées au JSON. |

## 5. Déroulement et rondes

| ID | Fonction livrée | Vérification attendue |
| --- | --- | --- |
| SF-DER-01 | Le tournoi commence concrètement lors de la création de `Round 1`. | Préparer un tournoi puis créer la première ronde. |
| SF-DER-02 | Le chargement restaure participants, rondes, matchs et résultats. | Quitter en cours de tournoi puis rouvrir. |
| SF-DER-03 | Les scores et le classement sont recalculés depuis les résultats restaurés. | Recharger puis comparer les scores. |
| SF-DER-04 | Après création du nombre de rondes prévu, aucune ronde supplémentaire n'est possible. | Tenter une ronde de plus. |
| SF-RON-01 | Les rondes sont créées une par une. | Vérifier qu'une seule nouvelle ronde apparaît. |
| SF-RON-02 | Leur nom est séquentiel : `Round 1`, `Round 2`, etc. | Créer plusieurs rondes. |
| SF-RON-03 | Le début est horodaté automatiquement à la création. | Créer puis consulter une ronde. |
| SF-RON-04 | Une nouvelle ronde exige la clôture de la précédente. | Tenter deux rondes simultanées. |
| SF-RON-05 | Le nombre de rondes créées ne dépasse pas la valeur prévue. | Tenter une ronde supplémentaire. |
| SF-RON-06 | Une ronde ne se clôture qu'avec tous ses résultats. | Laisser un match incomplet. |
| SF-RON-07 | La fin est horodatée automatiquement à la clôture. | Clôturer puis consulter. |
| SF-RON-08 | Une ronde clôturée reste consultable avec ses matchs et résultats. | Ouvrir une ronde terminée. |
| SF-RON-09 | La dernière ronde clôturée constitue la fin fonctionnelle du tournoi ; aucun statut séparé n'est persisté. | Clôturer la dernière ronde puis tenter d'en créer une nouvelle. |

## 6. Appariements

| ID | Fonction livrée | Vérification attendue |
| --- | --- | --- |
| SF-APP-01 | La première ronde mélange aléatoirement une copie des participants. | Comparer plusieurs créations équivalentes. |
| SF-APP-02 | Les joueurs sont associés deux par deux sans oubli ni doublon. | Contrôler toutes les occurrences. |
| SF-APP-03 | Le nombre de matchs vaut la moitié du nombre de participants. | Tester 4, 6 et 8 joueurs. |
| SF-APP-04 | Les rondes suivantes utilisent un classement par score décroissant. | Préparer des scores connus. |
| SF-APP-05 | Les joueurs à égalité de score conservent leur ordre relatif dans la liste des participants. | Préparer plusieurs joueurs ex æquo. |
| SF-APP-06 | Pour chaque joueur, un adversaire pas encore rencontré est recherché en priorité. | Simuler plusieurs rondes. |
| SF-APP-07 | Si aucune revanche ne peut être évitée, une paire disponible est tout de même créée. | Tester un historique contraignant. |
| SF-APP-08 | Chaque participant apparaît exactement une fois par ronde générée. | Contrôler les paires produites. |

L'optimisation exhaustive et l'équilibrage des couleurs ne sont pas requis.

## 7. Matchs et résultats

| ID | Fonction livrée | Vérification attendue |
| --- | --- | --- |
| SF-MAT-01 | Un match oppose exactement deux participants distincts. | Contrôler la création des matchs. |
| SF-MAT-02 | La structure interne exigée est un tuple contenant deux listes `[joueur, score]`. | Inspecter le modèle `Match`. |
| SF-MAT-03 | L'organisateur peut choisir victoire du premier, victoire du second ou nul. | Tester les trois résultats. |
| SF-MAT-04 | Une victoire attribue 1 point au gagnant et 0 au perdant. | Enregistrer puis contrôler. |
| SF-MAT-05 | Un nul attribue 0,5 point à chaque joueur. | Enregistrer puis contrôler. |
| SF-MAT-06 | Toute autre combinaison est refusée. | Tester valeurs négatives, 2 points et texte libre. |
| SF-MAT-07 | Un résultat validé est sauvegardé immédiatement. | Quitter après une saisie puis rouvrir. |
| SF-MAT-08 | Un résultat déjà saisi peut être modifié. | Ressaisir un résultat puis recharger. |
| SF-MAT-09 | Les points restent propres au tournoi et sont calculés depuis les matchs. | Comparer le même joueur dans deux tournois. |
| SF-MAT-10 | Les coups joués ne sont jamais demandés. | Parcourir la saisie complète. |

## 8. Sauvegarde et reprise

| ID | Fonction livrée | Vérification attendue |
| --- | --- | --- |
| SF-PER-01 | Toute création, modification ou suppression validée d'un joueur est sauvegardée. | Redémarrer immédiatement après l'action. |
| SF-PER-02 | Toute création validée d'un tournoi est sauvegardée. | Redémarrer immédiatement après création. |
| SF-PER-03 | L'ajout d'un participant est sauvegardé. | Quitter après inscription puis reprendre. |
| SF-PER-04 | La création des rondes et des matchs est sauvegardée. | Quitter après création d'une ronde. |
| SF-PER-05 | Chaque résultat est sauvegardé sans attendre la fin de la ronde. | Quitter après un seul match. |
| SF-PER-06 | La clôture d'une ronde est sauvegardée. | Quitter après clôture puis reprendre. |
| SF-PER-07 | Sans fichier joueur existant, l'application démarre avec un registre vide. | Utiliser un environnement neuf. |
| SF-PER-08 | Un fichier JSON vide, invalide ou de mauvaise structure produit une erreur compréhensible. | Présenter plusieurs fichiers invalides. |
| SF-PER-09 | Une erreur de chargement du registre joueur empêche son écrasement par une écriture ultérieure. | Provoquer l'erreur puis tenter une modification. |
| SF-PER-10 | La reprise continue depuis la dernière action validée. | Interrompre entre deux étapes. |

## 9. Rapports

| ID | Fonction livrée | Vérification attendue |
| --- | --- | --- |
| SF-RAP-01 | Afficher tous les joueurs par nom puis prénom. | Comparer à un jeu désordonné. |
| SF-RAP-02 | Afficher tous les tournois. | Créer plusieurs tournois. |
| SF-RAP-03 | Afficher le détail d'un tournoi : nom, lieu, dates, description et avancement. | Comparer avec la création. |
| SF-RAP-04 | Afficher les participants d'un tournoi par ordre alphabétique. | Inscrire dans un ordre différent. |
| SF-RAP-05 | Afficher toutes les rondes dans leur ordre d'enregistrement. | Consulter un tournoi multi-rondes. |
| SF-RAP-06 | Afficher le nom, les horodatages et les matchs de chaque ronde. | Comparer aux données enregistrées. |
| SF-RAP-07 | Afficher les deux joueurs et le résultat de chaque match. | Comparer ronde en cours et terminée. |
| SF-RAP-08 | Afficher le classement du tournoi avec le score calculé de chaque joueur. | Comparer au calcul manuel. |
| SF-RAP-09 | Tous les rapports sont consultables dans la console. | Générer sans fichier externe. |
| SF-RAP-10 | L'absence de données produit un message explicite. | Demander un rapport vide. |

## 10. Cohérence globale

| ID | Fonction livrée | Vérification attendue |
| --- | --- | --- |
| SF-COH-01 | Un participant conservé dans un tournoi est reconstruit avec son identité enregistrée. | Recharger plusieurs tournois. |
| SF-COH-02 | Le score affiché égale la somme des résultats du tournoi. | Recalculer manuellement. |
| SF-COH-03 | Une ronde clôturée contient un résultat par match. | Contrôler les rondes terminées. |
| SF-COH-04 | `current_round` correspond au nombre de rondes créées. | Comparer avant et après création d'une ronde. |
| SF-COH-05 | Avec N participants, chaque ronde générée contient N/2 matchs complets. | Contrôler plusieurs tailles paires. |

## 11. Parcours nominal

1. L'organisateur démarre ChessFlow.
2. Il crée ou consulte les joueurs.
3. Il crée un tournoi et renseigne ses informations.
4. Il charge le tournoi et ajoute un nombre pair de participants.
5. Il crée la première ronde ; ChessFlow génère des appariements aléatoires.
6. Il saisit les résultats puis clôture la ronde.
7. ChessFlow calcule le classement depuis les résultats.
8. Les rondes suivantes sont générées selon le classement et l'historique des rencontres.
9. Après la dernière ronde prévue, aucune nouvelle ronde ne peut être créée.
10. L'organisateur consulte les rapports et le classement.
11. Chaque action validée reste disponible après redémarrage.
