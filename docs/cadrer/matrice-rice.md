# Matrice RICE

La matrice RICE est un outil de priorisation qui permet de comparer objectivement des sujets en les notant sur quatre critères : Portée (Reach), Impact, Confiance (Confidence) et Effort.

Elle s'utilise pour arbitrer le contenu d'un [MVP](mvp.md), d'un jalon de [macroplan](la-roadmap.md) ou d'un backlog en cours de construction.

### Les quatre critères

| Critère | Définition | Exemple d'unité |
|---|---|---|
| **Portée** (Reach) | Nombre d'utilisateurs touchés par le sujet sur une période donnée | Nombre d'agents, nombre de dossiers par mois |
| **Impact** | Niveau d'amélioration de l'expérience ou de l'objectif pour chaque utilisateur touché | Échelle 0,25 (minime) à 3 (massif) |
| **Confiance** (Confidence) | Niveau de certitude sur les estimations de portée et d'impact, exprimé en % | 80 % = bonne connaissance du sujet |
| **Effort** | Charge de travail estimée pour réaliser le sujet | Semaines-équipe |

**Formule :**

> **Score RICE = (Portée × Impact × Confiance) / Effort**

Plus le score est élevé, plus le sujet est prioritaire.

### Comment mener un atelier RICE ?

1. **Réunir les bonnes personnes** : responsable produit, responsable métier, représentants techniques et, si possible, quelqu'un proche des utilisateurs
2. **Lister les sujets à prioriser** : fonctionnalités, améliorations, correctifs
3. **Scorer chaque critère collectivement** pour chaque sujet, en ajustant ensemble la portée et l'impact
4. **Calculer le score** et ordonner la liste par score décroissant
5. **Challenger les écarts** : un score surprenant révèle souvent un désaccord à expliciter avant de prendre une décision

!!! note

    La matrice RICE objective le débat, elle ne remplace pas le jugement de l'équipe. L'arbitrage final reste une décision humaine, tenant compte de contraintes non modélisables (politique, calendaire, réglementaire).

### Gabarit de scoring

| Sujet | Portée | Impact | Confiance | Effort | Score RICE |
|---|---|---|---|---|---|
| [Fonctionnalité A] | | | | | |
| [Fonctionnalité B] | | | | | |
| [Fonctionnalité C] | | | | | |

### Exemple

| Sujet | Portée | Impact | Confiance | Effort | Score |
|---|---|---|---|---|---|
| Formulaire de déclaration numérique | 200 agents/mois | 2 | 0,8 | 4 sem. | (200 × 2 × 0,8) / 4 = **80** |
| Export PDF automatisé | 50 agents/mois | 1 | 0,6 | 2 sem. | (50 × 1 × 0,6) / 2 = **15** |
| Tableau de bord de suivi | 30 agents/mois | 3 | 0,5 | 6 sem. | (30 × 3 × 0,5) / 6 = **7,5** |

Le formulaire de déclaration est nettement prioritaire dans cet exemple. Les chiffres restent à calibrer avec les données réelles du projet.

---
