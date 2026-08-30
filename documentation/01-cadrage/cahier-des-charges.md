# Cahier des charges de ChessFlow

## 1. Présentation

ChessFlow est une application locale de gestion de tournois d'échecs destinée à un club qui organise actuellement ses événements manuellement. Elle permet à un organisateur de préparer et suivre un tournoi de bout en bout sans connexion Internet ni abonnement à un service externe.

L'application est exécutée dans une console et conserve localement les joueurs, tournois, rondes, matchs et résultats.

## 2. Problème à résoudre

L'organisateur doit pouvoir :

1. enregistrer et retrouver les joueurs ;
2. créer un tournoi et sélectionner ses participants ;
3. générer les appariements de chaque ronde ;
4. saisir ou modifier les résultats des matchs ;
5. consulter les scores propres au tournoi ;
6. interrompre puis reprendre le travail sans perte de données validées ;
7. consulter les informations, classements et rapports demandés.

## 3. Utilisateurs et parties prenantes

### Utilisateur principal

L'organisateur ou directeur du tournoi utilise directement ChessFlow. Il gère les joueurs, les tournois, les rondes, les résultats et les rapports.

### Bénéficiaires

Les joueurs et membres du club consultent les appariements, résultats et classements produits par l'organisateur. Ils ne disposent pas de compte dans l'application.

### Partie prenante

Le club d'échecs attend une solution sans abonnement, portable, facile à installer et utilisable sur un site dépourvu de connexion Internet.

## 4. Objectifs

### Objectifs fonctionnels

- gérer un registre local de joueurs ;
- rechercher, modifier et supprimer un joueur du registre général ;
- créer et retrouver des tournois ;
- inscrire des joueurs existants à un tournoi avant le démarrage de la première ronde ;
- gérer un nombre défini de rondes, égal à 4 par défaut ;
- générer aléatoirement les matchs de la première ronde ;
- générer les rondes suivantes selon les scores et l'historique des rencontres ;
- enregistrer ou corriger les victoires, défaites et matchs nuls ;
- calculer les scores dans le contexte du tournoi à partir des résultats enregistrés ;
- sauvegarder automatiquement les modifications validées ;
- restaurer l'état du programme après fermeture ;
- afficher les listes, classements et rapports requis.

### Objectifs de qualité

- **Autonomie** : aucune connexion Internet nécessaire pendant l'utilisation.
- **Portabilité** : fonctionnement sous macOS, Windows et Linux.
- **Simplicité** : interface console compréhensible et parcours limités à l'essentiel.
- **Fiabilité** : sauvegarde après chaque modification significative.
- **Maintenabilité** : programmation orientée objet et architecture MVC.
- **Qualité du code** : conformité PEP 8 contrôlée avec Flake8.

## 5. Périmètre fonctionnel

### Joueurs

- créer un joueur avec nom, prénom, date de naissance et identifiant national d'échecs ;
- valider le format et l'unicité de l'identifiant national ;
- rechercher un joueur par identifiant national ;
- modifier les données d'un joueur avec les mêmes validations que lors de la création ;
- supprimer un joueur du registre général ;
- conserver les joueurs indépendamment des tournois ;
- afficher les joueurs par ordre alphabétique.

La suppression d'un joueur du registre général ne réécrit pas les tournois déjà sauvegardés : ceux-ci conservent l'identité des participants enregistrés dans leurs propres fichiers JSON.

### Tournois

- créer un tournoi avec nom, lieu, dates, nombre de rondes et description ;
- utiliser quatre rondes par défaut ;
- sélectionner les participants dans le registre des joueurs ;
- refuser les doublons et les nombres impairs de participants ;
- empêcher l'ajout de nouveaux participants après le démarrage de la première ronde ;
- suivre le nombre de rondes déjà créées ;
- recharger un tournoi enregistré pour le consulter ou poursuivre son déroulement.

### Rondes, matchs et scores

- créer les rondes progressivement ;
- horodater automatiquement le début d'une ronde lors de sa création ;
- associer les participants deux par deux ;
- enregistrer ou modifier le résultat de chaque match ;
- attribuer 1 point pour une victoire, 0 pour une défaite et 0,5 à chaque joueur pour un nul ;
- empêcher la clôture d'une ronde tant que tous ses matchs n'ont pas de résultat ;
- horodater automatiquement la fin d'une ronde à sa clôture ;
- calculer le classement et les scores à partir des résultats du tournoi.

### Appariements

- mélanger les participants pour la première ronde ;
- classer ensuite les participants par score décroissant ;
- conserver l'ordre existant entre joueurs à égalité de score ;
- rechercher en priorité un adversaire pas encore rencontré ;
- autoriser une revanche lorsqu'elle est nécessaire pour produire une ronde complète ;
- toujours produire une ronde complète lorsque le nombre de participants est valide.

### Persistance et consultation

- sauvegarder les joueurs dans `data/players.json` ;
- sauvegarder chaque tournoi dans `data/tournaments/` ;
- sauvegarder après chaque modification significative ;
- restaurer participants, rondes, matchs et résultats ;
- recalculer les scores depuis les matchs restaurés ;
- afficher les joueurs, les tournois, les participants, les classements et l'historique des rondes et matchs.

## 6. Contraintes

- application autonome exécutée avec Python depuis la console ;
- fonctionnement hors ligne obligatoire ;
- architecture modèle-vue-contrôleur ;
- utilisation d'instances de classes pour représenter le métier ;
- persistance JSON ;
- dépendances déclarées dans `requirements.txt` ;
- longueur maximale de ligne fixée à 119 caractères pour Flake8 ;
- rapport `flake8-html` généré dans `flake8_rapport` ;
- README contenant l'installation, l'exécution, les tests et le contrôle qualité.

## 7. Hors périmètre

- application web, mobile ou interface graphique ;
- comptes, authentification ou accès multi-utilisateur ;
- synchronisation distante, cloud ou API externe ;
- import de données historiques ;
- nombre impair de participants ou joueur exempt ;
- gestion détaillée des coups d'une partie ;
- calcul du classement national ou Elo ;
- génération de l'identifiant national ;
- équilibrage avancé des couleurs ;
- optimisation exhaustive des appariements ;
- export PDF ou tableur des rapports.

## 8. Hypothèses

- Python et les dépendances sont installés avant l'utilisation hors ligne ;
- une seule personne utilise l'application à un instant donné ;
- l'identifiant national est connu et fourni lors de la création du joueur ;
- les joueurs sont enregistrés avant leur inscription à un tournoi ;
- chaque tournoi comporte un nombre pair de participants avant la création de la première ronde ;
- les fichiers locaux sont accessibles en lecture et en écriture.

## 9. Risques principaux

| Risque | Conséquence | Réponse mise en œuvre |
| --- | --- | --- |
| Fichier JSON supprimé | Collection absente au démarrage | Registre joueur recréé comme collection vide ; tournoi absent signalé clairement |
| Fichier JSON vide ou endommagé | Données impossibles à restaurer | Erreur explicite et absence d'écriture sur un registre joueur non chargé |
| Fermeture pendant une saisie | Dernière saisie non validée perdue | Sauvegarde immédiatement après validation |
| Appariement contraint | Rencontre répétée possible | Éviter les répétitions autant que possible tout en produisant une ronde complète |
| Erreur de saisie | Donnée incohérente | Validation métier et messages d'erreur |
| Identifiant dupliqué | Confusion entre joueurs | Contrôle d'unicité avant création ou modification |

## 10. Critères de réussite

ChessFlow est accepté lorsque :

- le parcours complet d'un tournoi fonctionne hors ligne ;
- les données validées sont restaurées après redémarrage ;
- les règles métier et invariants sont respectés ;
- les rapports demandés sont disponibles dans la console ;
- le code respecte la séparation MVC et la POO ;
- les tests automatisés passent ;
- Flake8 ne signale aucune erreur ;
- le rapport HTML Flake8 est fourni ;
- l'installation et l'utilisation sont documentées.
