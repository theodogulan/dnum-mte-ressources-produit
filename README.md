# Guide DNUM — Ministère de la Transition Écologique (MTE)

Clone générique du GitBook *Ressources* de la DNUM, adapté pour la **Direction du Numérique (DNUM) du Ministère de la Transition Écologique (MTE)**, publié sous forme de site [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

> Contenu repris de la documentation publique d'origine ; seules les références à l'organisation (Ministères Sociaux / SDPC) ont été renommées en MTE / DNUM. Le reste du contenu est conservé tel quel et reste **à relire/adapter** au contexte MTE.

## Structure

```
dnum-mte-ressources/
├── docs/            # contenu Markdown (90 pages, arborescence Cadrer/Concevoir/Développer/Déployer/Aide)
├── mkdocs.yml       # configuration du site + navigation
├── requirements.txt # dépendances Python
├── download.py        # (régénération) télécharge les pages sources Markdown dans raw/
├── build_site.py      # (régénération) transforme raw/ -> docs/ + génère mkdocs.yml
├── download_images.py # (régénération) récupère les images de contenu dans docs/assets/
└── llms.txt           # index des pages sources
```

## Lancer en local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve            # http://127.0.0.1:8000
```

## Construire le site statique

```bash
mkdocs build            # génère le dossier site/
```

Le dossier `site/` est déployable tel quel (GitHub Pages, GitLab Pages, Netlify, S3, serveur statique…).
Pour GitHub Pages : `mkdocs gh-deploy`.

## Régénérer depuis la source

Pipeline complet (à relancer dans cet ordre) :

```bash
python3 download.py         # 1. télécharge les .md sources -> raw/ (avec cache)
python3 build_site.py       # 2. transforme raw/ -> docs/ + génère mkdocs.yml
python3 download_images.py  # 3. récupère et rehéberge les images de contenu -> docs/assets/
```

Les règles de renommage de l'organisation sont dans `build_site.py` (constante `ORG_REPLACEMENTS`) —
ajustez-les pour affiner l'adaptation MTE. La résolution des liens internes opaques GitBook
(`/pages/ID`) sans ambiguïté est dans `PAGE_ID_MAP` ; les composants « cards » sont reliés
automatiquement par correspondance de titre.

## À adapter / points d'attention

Le périmètre choisi était « renommer l'organisation seulement ». Restent donc dans le contenu
des éléments propres au ministère d'origine, à revoir selon les besoins MTE :

- **URLs externes** vers les ressources d'origine (SharePoint `msociauxfr`, dépôts GitHub
  `DNUM-SocialGouv`, autres espaces GitBook) et **adresses e-mail de contact** (`@sg.social.gouv.fr`).
- **Briques sectorielles** santé/social conservées telles quelles : Pro Santé Connect,
  PLAGE/PASREL, hébergement CEGEDIM, Démat' Social, champs NIR/FINESS/RPPS, etc.
- Quelques **ancres internes** de sommaire (liens `#…`) héritées de la source dont le libellé
  ne correspond pas exactement au titre — sans impact sur l'affichage des pages.
