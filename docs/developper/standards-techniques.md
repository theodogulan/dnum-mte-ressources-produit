# Standards techniques

Un standard technique est la meilleure façon connue aujourd'hui de réaliser un geste récurrent au sein d'une équipe. Il n'est pas figé : il est destiné à être amélioré au fur et à mesure des apprentissages.

!!! note

    Le [Cadre de Cohérence Technique (CCT)](cct.md) constitue l'ensemble des standards techniques obligatoires de la DNUM du MTE. La présente page décrit comment créer, appliquer et améliorer un standard d'équipe, quelle que soit sa portée.

### À quoi sert un standard ?

* **Former et embarquer** : un standard explicite permet à un nouveau membre de l'équipe d'atteindre rapidement le niveau attendu, sans transmission uniquement orale
* **Homogénéiser** : réduire la variabilité dans les pratiques, et donc dans la qualité des livrables
* **Améliorer en continu** : le standard est la base de référence à partir de laquelle on détecte les écarts et on fait progresser les pratiques (voir [résolution de problème](resolution-de-probleme.md))

### Points de contrôle

Un bon standard s'accompagne de points de contrôle simples et mémorisables : des questions ou critères permettant à tout membre de l'équipe de juger si le travail est conforme.

**Exemple pour un standard de revue de code :**

* [ ] Le code est-il couvert par des tests automatisés ?
* [ ] Les noms de fonctions et de variables sont-ils explicites ?
* [ ] La PR contient-elle une description suffisante pour être comprise sans échange oral ?

### Cycle de vie d'un standard

```
Création -> Application -> Détection d'écart -> Analyse de la cause -> Amélioration (Kaizen)
    ^_________________________ (boucle) _______________________________________________|
```

1. **Création** : l'équipe formalise la meilleure pratique connue, avec son contexte et ses points de contrôle
2. **Application** : le standard est partagé, expliqué et appliqué dans les pratiques quotidiennes
3. **Détection d'écart** : un point de contrôle révèle qu'une pratique s'écarte du standard (en revue, en rétrospective, lors d'un incident)
4. **Analyse de la cause** : comprendre pourquoi l'écart s'est produit (voir [résolution de problème](resolution-de-probleme.md))
5. **Amélioration** : mettre à jour le standard ; si la décision est structurante, la consigner dans un [ADR](architecture-decision-record.md)

### Gabarit

**Titre du geste**
[En une phrase : ce que décrit ce standard]

**Contexte**
Dans quelles situations ce standard s'applique-t-il ?

**Étapes**

1. ...
2. ...
3. ...

**Points de contrôle**

* [ ] ...
* [ ] ...

**Anti-patterns**
Ce qu'il ne faut pas faire, et pourquoi.

**Auteur / Dernière mise à jour**
[À COMPLÉTER]

---
