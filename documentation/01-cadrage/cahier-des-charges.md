# Cahier des charges de ChessFlow

## 1. Présentation

ChessFlow est une application locale de gestion de tournois d'échecs destinée à un club qui organise actuellement ses événements manuellement. Elle doit permettre à un organisateur de préparer et suivre un tournoi de bout en bout sans connexion Internet ni abonnement à un service externe.

L'application est exécutée dans une console et conserve localement les joueurs, tournois, rondes, matchs et résultats.

## 2. Problème à résoudre

L'organisateur doit pouvoir :

1. enregistrer et retrouver les joueurs ;
2. créer un tournoi et sélectionner ses participants ;
3. générer les appariements de chaque ronde ;
4. saisir les résultats des matchs ;
5. calculer les scores propres au tournoi ;
6. interrompre puis reprendre le travail sans perte de données ;
7. consulter les informations et rapports demandés.

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
- créer et retrouver des tournois ;
- inscrire des joueurs existants à un tournoi ;
- gérer un nombre défini de rondes, égal à 4 par défaut ;
- générer aléatoirement les matchs de la première ronde ;
- générer les rondes suivantes selon les scores et l'historique des rencontres ;
- enregistrer les victoires, défaites et matchs nuls ;
- maintenir le score de chaque participant dans le contexte de son tournoi ;
- sauvegarder automatiquement les modifications ;
- restaurer l'état du programme après fermeture ;
- afficher les listes et rapports requis.

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
- conserver les joueurs indépendamment des tournois ;
- afficher les joueurs par ordre alphabétique.

### Tournois

- créer un tournoi avec nom, lieu, dates, nombre de rondes et remarques ;
- utiliser quatre rondes par défaut ;
- sélectionner les participants dans le registre des joueurs ;
- refuser les doublons et les nombres impairs de participants ;
- suivre la ronde courante et l'état du tournoi.

### Rondes, matchs et scores

- créer les rondes progressivement ;
- horodater automatiquement le début et la fin d'une ronde ;
- associer les participants deux par deux ;
- enregistrer le résultat de chaque match ;
- attribuer 1 point pour une victoire, 0 pour une défaite et 0,5 à chaque joueur pour un nul ;
- recalculer les scores du tournoi après chaque ronde.

### Appariements

- mélanger les participants pour la première ronde ;
- classer ensuite les participants par score décroissant ;
- départager aléatoirement les joueurs à égalité ;
- éviter autant que possible les rencontres déjà jouées ;
- toujours produire une ronde complète lorsque le nombre de participants est valide.

### Persistance et consultation

- sauvegarder joueurs et tournois dans des fichiers JSON locaux ;
- sauvegarder après chaque modification significative ;
- restaurer participants, scores, rondes et matchs ;
- afficher les joueurs, les tournois, les participants et l'historique des rondes et matchs.

## 6. Contraintes

- application autonome exécutée avec Python depuis la console ;
- fonctionnement hors ligne obligatoire ;
- architecture modèle-vue-contrôleur ;
- utilisation d'instances de classes pour représenter le métier ;
- persistance JSON ;
- dépendances déclarées dans `requirements.txt` ;
- longueur maximale de ligne fixée à 119 caractères pour Flake8 ;
- rapport `flake8-html` généré dans `flake8_rapport` ;
- README contenant l'installation, l'exécution et le contrôle qualité.

## 7. Hors périmètre

- application web, mobile ou interface graphique ;
- comptes, authentification ou accès multi-utilisateur ;
- synchronisation distante, cloud ou API externe ;
- import de données historiques ;
- suppression de joueurs ;
- nombre impair de participants ou joueur exempt ;
- gestion détaillée des coups d'une partie ;
- calcul du classement national ou Elo ;
- génération de l'identifiant national ;
- équilibrage avancé des couleurs ;
- optimisation parfaite des appariements ;
- export PDF ou tableur des rapports.

## 8. Hypothèses

- Python et les dépendances sont installés avant l'utilisation hors ligne ;
- une seule personne utilise l'application à un instant donné ;
- l'identifiant national est connu et fourni lors de la création du joueur ;
- les joueurs sont enregistrés avant leur inscription à un tournoi ;
- chaque tournoi comporte un nombre pair de participants ;
- les fichiers locaux sont accessibles en lecture et en écriture.

## 9. Risques principaux

| Risque | Conséquence | Réponse prévue |
| --- | --- | --- |
| Fichier JSON supprimé ou endommagé | Données impossibles à restaurer | Écriture contrôlée, message explicite et sauvegarde externe recommandée |
| Fermeture pendant une saisie | Dernière action non validée perdue | Sauvegarde immédiatement après validation |
| Appariement contraint | Rencontre répétée possible | Éviter les répétitions autant que possible sans recherche exhaustive |
| Erreur de saisie | Donnée incohérente | Validation et nouvelle saisie |
| Identifiant dupliqué | Confusion entre joueurs | Contrôle d'unicité avant enregistrement |

## 10. Critères de réussite

ChessFlow est accepté lorsque :

- le parcours complet d'un tournoi fonctionne hors ligne ;
- les données sont restaurées après redémarrage ;
- les règles métier et invariants sont respectés ;
- les rapports demandés sont disponibles dans la console ;
- le code respecte la séparation MVC et la POO ;
- Flake8 ne signale aucune erreur ;
- l'installation et l'utilisation sont documentées.

