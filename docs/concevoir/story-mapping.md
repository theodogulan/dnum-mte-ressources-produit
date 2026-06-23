# Story mapping

Le story mapping est un atelier collaboratif qui permet de visualiser l'ensemble des fonctionnalités d'un produit, de définir le périmètre du [MVP](../cadrer/mvp.md) et d'organiser les prochaines itérations (releases).

!!! note

    Le story mapping se place après le [parcours utilisateur](parcours-utilisateur.md) et la [recherche utilisateur](ru.md), dont il exploite les résultats. Il alimente directement la [roadmap](../cadrer/la-roadmap.md).

### Prérequis

Avant de démarrer l'atelier, s'assurer que :

* [ ] Une phase de [recherche utilisateur](ru.md) a été menée
* [ ] Le [parcours utilisateur](parcours-utilisateur.md) est formalisé
* [ ] Les principales parties prenantes sont présentes (responsable produit, responsable métier, design, technique)

### Structure d'un story map

Un story map est organisé en trois niveaux :

**1. L'épine dorsale (activités)**
Les grandes activités que l'usager réalise pour atteindre son objectif, dans l'ordre chronologique. Exemple : "Préparer", "Saisir", "Transmettre", "Consulter".

**2. Les fonctionnalités**
Pour chaque activité, les actions spécifiques que l'usager doit pouvoir réaliser. Exemple : sous "Saisir", on trouve "Remplir le formulaire", "Joindre une photo", "Valider la saisie".

**3. La ligne de découpe MVP / releases**
Une ligne horizontale sépare ce qui entre dans le MVP (au-dessus) de ce qui est reporté aux itérations suivantes.

```
ÉPINE DORSALE :  [Activité 1]       [Activité 2]       [Activité 3]
                 [Fonctionna. 1.1]  [Fonctionna. 2.1]  [Fonctionna. 3.1]
MVP :            [Fonctionna. 1.2]  [Fonctionna. 2.2]  [Fonctionna. 3.2]
- - - - - - - - - - - - limite MVP - - - - - - - - - - - - - - - - - - -
RELEASE 2 :      [Fonctionna. 1.3]  [Fonctionna. 2.3]  [Fonctionna. 3.3]
- - - - - - - - - - - - limite release 2 - - - - - - - - - - - - - - - -
```

### Comment animer l'atelier ?

1. **Poser l'épine dorsale** : en partant du parcours utilisateur, identifier les grandes activités (post-its en haut du tableau)
2. **Dérouler les fonctionnalités** : pour chaque activité, lister toutes les fonctionnalités possibles sans filtre (phase divergente)
3. **Tracer la ligne MVP** : décider collectivement du minimum permettant à un usager d'accomplir son objectif de bout en bout
4. **Organiser les releases** : regrouper les fonctionnalités restantes en itérations cohérentes
5. **Affiner les arbitrages** avec la [matrice RICE](../cadrer/matrice-rice.md) si plusieurs sujets sont en concurrence à l'intérieur du MVP

### Gabarit

| | Activité 1 | Activité 2 | Activité 3 |
|---|---|---|---|
| **Fonctionnalités MVP** | ... | ... | ... |
| *(limite MVP)* | | | |
| **Release 2** | ... | ... | ... |
| **Release 3** | ... | ... | ... |

### Exemple

Story map pour un outil de déclaration d'inspection terrain.

| | Préparer | Saisir | Transmettre |
|---|---|---|---|
| **MVP** | Consulter les dossiers existants | Remplir le formulaire réglementaire | Envoyer au service de traitement |
| *(limite MVP)* | | | |
| **Release 2** | Filtrer par secteur géographique | Joindre des photos | Suivi du statut de traitement |
| **Release 3** | Historique des inspections | Signature électronique | Export PDF personnalisé |

---
