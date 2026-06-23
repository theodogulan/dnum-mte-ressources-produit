# Résolution de problème

Un problème est un écart entre une situation observée et un standard (la situation attendue). La première étape, souvent négligée, est de bien définir la situation cible : sans référence claire, il est impossible de mesurer l'écart réel et de traiter la bonne cause.

!!! note

    Une fois la cause racine traitée, mettre à jour le [standard](standards-techniques.md) concerné. Si la décision prise est structurante pour l'architecture ou la technique, la consigner dans un [ADR](architecture-decision-record.md).

### La méthode P-C-A

La méthode P-C-A structure la résolution en trois temps : Problème, Causes, Actions.

#### P — Problème

Décrire l'écart de façon factuelle et mesurable :

* Quelle est la situation observée ? (avec chiffres si possible)
* Quelle est la situation attendue (le standard ou la cible) ?
* Depuis quand ? Dans quel contexte ?

Éviter les formulations vagues ("ça ne marche pas", "c'est lent") et préférer les faits mesurables ("le temps de traitement d'un dossier est de 3 jours, contre 1 jour attendu").

#### C — Causes

Identifier 1 à 3 causes directes, puis remonter aux causes racines par la technique des 5 pourquoi :

> Pourquoi ? → Réponse → Pourquoi ? → Réponse → ... (jusqu'à la cause racine)

**Règle pratique :** s'arrêter quand la réponse pointe vers un processus, un manque de compétence, un outil défaillant ou un standard absent ou mal défini.

#### A — Actions

Définir deux niveaux d'action :

* **Action immédiate** : traiter le symptôme rapidement pour limiter l'impact
* **Action de fond** : traiter la cause racine pour éviter la récurrence

Pour chaque action : responsable, délai, indicateur de vérification.

### Gabarit P-C-A

**Problème**

* Situation observée : [À COMPLÉTER]
* Situation attendue : [À COMPLÉTER]
* Écart : [À COMPLÉTER]

**Causes**

* Cause directe : ...
  * Pourquoi ? : ...
  * Pourquoi ? : ...
  * Cause racine : ...

**Actions**

| Action | Type | Responsable | Délai | Indicateur de vérification |
|---|---|---|---|---|
| ... | Immédiate | | | |
| ... | De fond | | | |

**Suivi**

* Standard à mettre à jour : [lien ou [À CRÉER]]
* ADR à rédiger : oui / non

### Exemple

**Problème**
Situation observée : 30 % des revues de code prennent plus de 48 h, bloquant les mises en production.
Situation attendue : toute revue de code est traitée en moins de 24 h ouvrées.

**Causes**
Cause directe : les relecteurs ne sont pas notifiés de façon systématique.
Pourquoi ? : pas de règle d'assignation dans l'outil de gestion du code.
Pourquoi ? : aucun standard n'a été défini pour le processus de revue.
Cause racine : absence de standard de revue de code.

**Actions**

| Action | Type | Responsable | Délai | Indicateur |
|---|---|---|---|---|
| Assigner manuellement les relecteurs en attendant | Immédiate | Responsable produit | Immédiat | Délai moyen < 24 h |
| Rédiger et appliquer le standard de revue de code | De fond | Lead technique | 2 semaines | 100 % des PRs avec relecteur assigné |

---
