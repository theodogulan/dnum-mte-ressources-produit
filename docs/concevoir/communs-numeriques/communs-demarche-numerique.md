# Démarche Numérique

[**Démarche Numérique**](https://demarche.numerique.gouv.fr/) (anc. Démarches Simplifiées) est un SaaS interministériel de dématérialisation des démarches administratives.\

## Fonctionnalités notables de Démarche Numérique

### Pour l'usager (particulier, entreprise, association)

* Déposer un dossier pour soi ou pour autrui
* Transférer son dossier à une personne pour se faire aider
* Afficher une interface en anglais
* Récupérer automatiquement des données sur API Entreprises (DLNUF)
* Redresser automatiquement une adresse postale via la Base Adresse Nationale

### Pour l'agent instructeur

* Echanger par message avec le déposant
* Annoter un dossier avec des champs et des pièces-jointes propre à l'instruction
* Faire intervenir ponctuellement des experts externes pour enrichir l'instruction

### Pour l'administrateur de la démarche

* Paramétrer finement un formulaire avec un large choix de type de données
* Récupérer automatiquement des données dans un référentiel externe (DLNUF), avec ou sans autosuggestion
* Inviter des usagers à compléter un formulaire prérempli par l'administration (DLNUF)
* Définir les règles d'éligibilité à la démarche (ex : déploiement national progressif par région)
* Paramétrer le routage automatique des dossiers vers les équipes d'instruction (ex : par découpage géographique)
* Délivrer une attestation PDF en fin de parcours
* Définir les règles juridiques de la démarche en termes de Silence Vaut Accord (SVA) et Silence Vaut Rejet (SVR)
* Mesurer la satisfaction grâce au bouton Je donne mon avis (JDMA)
* S'inspirer des [50 000 démarches déjà existantes dans Démarche Numérique](https://demarche.numerique.gouv.fr/admin/procedures/all)

### Pour le développeur d'application back-office

* API GraphQL pour récupérer facilement les données nécessaires sur un ensemble de dossiers
* API GraphQL pour mettre à jour un dossier (statut, message à l'usager...)

## Limitations de Démarche Numérique

* Pas de personnalisation du workflow d'instruction. Démarche Numérique reste simple pour ne pas encourager la sur-administration.
* Pas de conservation des données vivantes au-delà de 12 mois (DN). En revanche il est possible de demander l'archivage sur 5 ans.
* Pas de duplication ou de mise à jour d'une démarche précédemment terminée
* Pas de modification des données déposées par l'instructeur (L'instructeur doit demander des modifications à l'usager)
* Pas d'API REST
* Pas de garantie de livraison des webhooks (messages sortant vers un autre système). A date, la perte possible d'information limite l'intérêt du webhook au seul déclenchement périodique de batch, dans une logique d'éco-conception.
