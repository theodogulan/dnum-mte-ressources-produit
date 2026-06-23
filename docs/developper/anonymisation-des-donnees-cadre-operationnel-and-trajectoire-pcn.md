# Anonymisation des données : cadre opérationnel & trajectoire PCN

### **1. Objet et périmètre**

Cette page couvre :

* l’anonymisation de données structurées en BDD (principalement PostgreSQL) ;
* les principes fondamentaux (RGPD, RGS) ;
* une trajectoire court terme **réaliste et immédiatement mobilisable par les équipes produit** ;
* des orientations moyen terme en cohérence avec la réorganisation et les capacités futures de l’organisation.

Elle ne couvre pas (encore) :

* la pseudonymisation (mécanisme différent, réversible, toujours soumis au RGPD) ;
* l’anonymisation dans les logs applicatifs, fichiers, documents, ou flux d’échanges ;
* les aspects de sécurité opérationnelle (chiffrement, cloisonnements, habilitations).

***

### **2. Prérequis – Ce qu’il faut avoir en tête**

#### **2.1 Anonymisation ≠ pseudonymisation**

L’anonymisation vise à rendre impossible, en pratique et de manière irréversible, l’identification d’une personne. Lorsqu’elle est correctement réalisée, la donnée sort du champ RGPD.\
La pseudonymisation, elle, remplace un identifiant par un alias, mais la ré‑identification reste possible via une clé séparée : **le RGPD continue de s’appliquer**.

#### **2.2 Risques à éviter**

Les trois risques classiques à maîtriser sont :

* **Individualisation** : possibilité d’isoler une personne unique dans un jeu de données ;
* **Corrélation** : possibilité de recroiser la donnée avec d’autres sources ;
* **Inférence** : possibilité de déduire une information sensible à partir d’attributs restants.

#### **2.3 Références**

*Lecture (en diagonale à minima) recommandée avant de poursuivre la lecture de la présente page.*

* [CNIL — *Anonymisation de données*](https://www.cnil.fr/fr/technologies/lanonymisation-de-donnees-personnelles)
* [CNIL — *Guide RGPD du développeur* (fiche 7 : minimisation).](https://github.com/LINCnil/Guide-RGPD-du-developpeur/blob/main/07-Minimiser%20les%20donn%C3%A9es%20collect%C3%A9es.md)

***

### **3. Schéma simple – Avant / Après**

```
              ┌───────────────┐
              │Collecte (prod)│
              └──────┬────────┘
                     │
                     ▼
             ┌────────────────────┐
             │ Données réelles    │
             │  (production)      │
             └──────┬─────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │ Anonymisation (règles +    │
        │ génération d’un jeu dédié) │
        └──────┬────────────┬────────┘
               │            │
               ▼            ▼
     ┌────────────────┐   ┌─────────────────────────┐
     │ Environnements │   │ Usages en production     │
     │   non‑prod     │   │ (stats, BI, open data…) │
     └────────────────┘   └─────────────────────────┘
```

***

### **4. Enjeux dans notre contexte**

#### **4.1 Conformité**

Le RGPD impose minimisation, contrôle des accès, sécurité des traitements. Le RGS fournit une méthode d’analyse de risques et un cadre d’homologation.\
L’anonymisation répond à un double besoin : réduire l’exposition aux risques et permettre des usages légitimes de données en non‑prod.

#### **4.2 Approche produit**

Les équipes produit doivent conserver une autonomie de mise en œuvre, surtout face à un existant hétérogène.\
L’enjeu est de leur donner un **cadre lisible** et plusieurs trajectoires possibles, sans imposer un outil unique.

#### **4.3 Usages légitimes des données anonymisées**

Les données anonymisées peuvent être utilisées dans différents contextes (non exhaustifs) :

* **Hors production (**&#x69;ntégration, préproduction, etc.) pour réaliser différents tests (fonctionnels, non régression, performance, etc.)
* **Diagnostic et support** :
  * reproduction de bugs
  * analyses d’incidents,
  * investigation fonctionnelle ou technique.
* **Usages en production** :
  * analyses statistiques internes,
  * alimentation de tableaux de bord décisionnels,
  * études ad hoc (ex. simulations, analyses transverses),
  * publication en open data lorsque c’est pertinent.

Ces usages reposent sur un **jeu anonymisé distinct** des données réelles, généré à partir des règles définies par l’équipe produit.

***

### **5. Constat DNUM**

Le sujet de l’anonymisation s’inscrit dans un paysage technique varié, construit par strates successives. Cela se traduit par une pluralité de pratiques :

* un outil historique (DOT‑A) qui arrive aujourd’hui au terme de son cycle,
* des scripts spécifiques intégrés dans certains produits,
* la mise en place d'outils spécialisés (et parfois sous-exploités) dans d'autres produits,
* des opérations d’anonymisation réalisées au niveau hébergeur,
* et, dans certains cas, des besoins encore récents ou inexistants.

La réorganisation en cours devrait faciliter une évolution vers une approche plus homogène, mais ce n’est pas le cas à court terme.

**Conséquence :**\
La priorité est d’offrir aux équipes un **cadre simple et immédiatement activable**, sans attendre l’arrivée d’un socle mutualisé.

***

### **6. Principes structurants**

#### **6.1 Minimiser et purger**

Ne collecter que les données nécessaires, supprimer ce qui ne sert plus.\
[Pour aller plus loin](https://github.com/LINCnil/Guide-RGPD-du-developpeur/blob/main/07-Minimiser%20les%20donn%C3%A9es%20collect%C3%A9es.md)

#### **6.2 Pas de données personnelles réelles en non‑prod**

Toute circulation vers non‑prod doit être **anonymisée au préalable**.

#### **6.3 Logs et traces sans données personnelles identifiables**

Limiter les logs aux identifiants techniques.\
C’est un prérequis autant sécurité que conformité.

#### **6.4 Données sensibles à anonymiser**

* Identité : nom, prénom, identifiants.
* Coordonnées : email, téléphone, adresse.
* Données financières : IBAN, RIB.
* Données sensibles (santé, etc.) selon contexte.
* Données à fort pouvoir d’inférence : dates, localisation, identifiants indirects.

Pour aller plus loin, [identifier les données à caractères personnelles](https://github.com/LINCnil/Guide-RGPD-du-developpeur/blob/main/01-Identifier%20les%20donn%C3%A9es%20personnelles.md) (et donc sensibles)

***

## **7. Court terme – Ce que les équipes peuvent faire immédiatement**

Objectif : rendre possible une anonymisation sur chaque projet, dès maintenant.\
On cherche une solution réalisable, pas “la solution parfaite”.

!!! warning

    A*ssumer une solution imparfaite mais en place vaut mieux qu’une solution idéale jamais mise en œuvre*.


Si vous explorez une autre option à court terme, ✉️ parlons-en *(adresse de contact MTE à renseigner)* rapidement en amont : cela permettra de confirmer qu’elle est compatible avec notre environnement et, le cas échéant, d'enrichir cette documentation.

***

### **Option A — Approche “autonomie produit”**

L’équipe met en place son anonymisation à l’aide de :

* scripts utilisant la stack existante du produit (`sh`, Python, java, node, etc.),
* ou anonymisation au niveau du code (Java, Node, etc.),
* exécutés sur un **schéma de travail** dans la base de production,
* puis diffusés en non‑prod selon les besoins.

#### Forces

* Immédiatement actionnable.
* Compatible avec tous les projets, même legacy.
* Peu dépendant de l’hébergement.

#### Limites

* Hétérogénéité d’un produit à l’autre.
* Faible traçabilité RGPD.
* Scalabilité limitée si volumes importants.
* Approche limitée en cas de besoins avancées (plusieurs dizaines de champs de tables différentes à anonymiser avec des règles différentes).

***

### **Option B — S'appuyer sur un outil existant**

#### Greenmask

Dump → transformation → restore. Puissant, flexible.\
⚠️ À cadrer avec l’hébergement (installation, dépendances, stockages).

#### PostgreSQL Anonymizer (`anon`)

Masquage dynamique+statique au niveau base.\
⚠️ Nécessite installation côté serveur PostgreSQL.

#### Forces

* Approches plus techniques et plus propres.
* Potentiel de standardisation à moyen terme.

#### Limites

* Besoin de coordination avec les hébergeurs.
* ROI à considérer puisque vous allez le porter au niveau produit (outil "overkill" pour anonymiser quelques champs de différentes tables)
* Pas activable partout immédiatement ([un accompagnement](../aide/etre-accompagne/accompagnement-technique.md) peut être déclenchée pour faciliter la mise en œuvre dans votre contexte).

***

## **8. Moyen terme – Trois trajectoires possibles**

Le moyen terme vise à réduire l’effort pour les produits et à apporter de la cohérence.\
Ces trajectoires ne sont **ni décidées ni engagées** aujourd’hui : elles dépendent de priorisations futures.

### **1. Trajectoire “socle data”**

Lorsqu’un socle data sera plus largement déployé, il pourrait accueillir une fonction d’anonymisation lors des flux d’alimentation ou des exports.

### **2. Trajectoire “hébergement / infra”**

Certaines de nos offres d'hébergement pourraient intégrer l’anonymisation dans leurs routines (dump/restaure, pipelines).

### **3. Trajectoire “studio technique / commun”**

Production d’un starter kit, d’un outillage plus robuste, ou d’une offre “clef en main” pour les produits.<br>

#### Forces transverses

* Mutualisation.
* Alignement organisationnel.
* Réduction du coût unitaire par produit.

#### Limites

* Ressources limitées.
* Pas d’échéance réaliste à ce stade.

#### Activation

Les projets en tension (délais, volumes, risques) doivent **remonter** leur besoin pour arbitrage.

***

## **9. Acteurs impliqués**

#### **Équipe produit**

* Identifie les données sensibles ;
* Choisit la solution court terme qui lui convient ;
* Met en place, exécute et valide l’anonymisation ;
* Documente a minima.

#### **Hébergeur / infogérant**

* Fournit les capacités techniques nécessaires (dump, restore, droits sur schéma de travail) ;
* Peut exécuter certaines manipulations si demandé.

#### **Responsable de traitement**

* Valide les finalités d’usage des données anonymisées ;
* Peut demander des précisions sur les risques résiduels.

#### **Référent SSI / RGS**

* Vérifie la cohérence sécurité, la minimisation des risques, les habilitations ;
* Aide à interpréter les obligations RGPD/RGS.

#### **Équipe d’accompagnement**

* Soutient les équipes dans le choix de la trajectoire (script, code, outil) ;
* Peut **prendre la décision** sur demande de l’équipe produit (ex. difficulté technique, incertitude, manque de ressources) ;
* Assure la cohérence globale.

***

### **10. Conclusion**

Cette page propose une trajectoire **réaliste, progressive et adaptée** à la diversité de nos produits et à la maturité actuelle de l’organisation.

* **Court terme** : une solution simple, autonome, “qui marche”.
* **Moyen terme** : plusieurs chemins possibles, à prioriser.
* **Cap général** : ne pas laisser circuler de données personnelles réelles hors production, et avancer même si la solution n’est pas idéale.

---
