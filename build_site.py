#!/usr/bin/env python3
"""Transforme raw/*.md (GitBook) -> docs/*.md (MkDocs Material) + génère mkdocs.yml.

- Nettoie l'en-tête et le pied "Agent Instructions" injectés par GitBook.
- Convertit la syntaxe GitBook ({% hint %}, {% content-ref %}, {% embed %}, {% file %}) en Markdown/admonitions MkDocs.
- Renomme l'organisation (Ministères Sociaux -> Ministère de la Transition Écologique).
- Retire tout le contenu spécifique santé/social (Pro Santé Connect, PLAGE/PASREL, Démat Social, FINESS, RPPS…).
- Réécrit les liens absolus du GitBook source en liens relatifs internes.
- Construit la navigation mkdocs.yml à partir de l'arborescence des chemins.
"""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "raw")
DOCS = os.path.join(ROOT, "docs")
BASE = "https://dnum-ministeres-sociaux.gitbook.io/ressources/"

# --- Renommage organisation (ordre important : du plus spécifique au plus général) ---
ORG_REPLACEMENTS = [
    (r"sous-direction des produits et communs numériques \(SDPC\) de la Direction du Numérique des Ministères Sociaux",
     "Direction du Numérique (DNUM) du Ministère de la Transition Écologique (MTE)"),
    (r"Direction du Numérique des Ministères [Ss]ociaux",
     "Direction du Numérique du Ministère de la Transition Écologique"),
    (r"DNUM des [Mm]inistères [Ss]ociaux", "DNUM du Ministère de la Transition Écologique"),
    (r"[Dd]es [Mm]inistères [Ss]ociaux", "du Ministère de la Transition Écologique"),
    (r"[Dd]u [Mm]inistère des [Ss]ociaux", "du Ministère de la Transition Écologique"),
    (r"[Mm]inistères [Ss]ociaux", "Ministère de la Transition Écologique"),
    (r"Min Sociaux", "Min. Transition Écologique"),
    # Sous-direction SDPC -> DNUM (générique MTE)
    (r"DNUM/SDPC/ST", "DNUM/ST"),
    (r"DNUM/SDPC", "DNUM"),
    (r"\bSDPC\b", "DNUM"),
]

HINT_MAP = {"info": "note", "warning": "warning", "danger": "danger",
            "success": "success", "tip": "tip"}

# Pages à supprimer entièrement (contenu exclusivement santé/social).
SKIP_PAGES = {
    "concevoir/authentification/authentification-pro-sante-connect.md",
    "concevoir/authentification/authentification-plage-pasrel.md",
}


def clean_social(text, relpath):
    """Retire tout le contenu spécifique santé/social. Appliqué sur le texte brut (avant clean_gitbook)."""

    # ── 1. communs-demarche-numerique : fichier partiellement santé/social ──────────────
    if relpath and "communs-demarche-numerique" in relpath:
        # Titre : "Démarche Numérique et Démat Social" → "Démarche Numérique"
        text = re.sub(r"(#+ Démarche Numérique) et Démat Social", r"\1", text)
        # Intro Démat Social (ligne débutant par "[**Démat Social**]...") → supprimée
        text = re.sub(r"^\[?\*?\*?Démat Social\*?\*?\]?[^\n]*\n", "", text, flags=re.M)
        # Heading de section limitations
        text = re.sub(r"(##+ Limitations de Démarche Numérique) et Démat Social", r"\1", text)
        # "ou 36 mois (Démat Social)" dans bullet
        text = re.sub(r"\s+ou\s+36\s+mois\s+\(Démat Social\)", "", text)
        # Supprimer tout le bloc "## Choisir entre..." jusqu'à la prochaine ## ou fin
        text = re.sub(
            r"\n## Choisir entre Démarche Numérique et Démat Social\b.*",
            "",
            text,
            flags=re.S,
        )

    # ── 2. authentification : retirer les lignes de tableau santé/social ────────────────
    # Lignes de tableau markdown contenant Pro Santé Connect, PLAGE/PASREL, DDETS, ATIH
    text = re.sub(r"^\|[^\n]*Professionnel de Santé[^\n]*\n", "", text, flags=re.M)
    text = re.sub(r"^\|[^\n]*Pro Santé Connect[^\n]*\n", "", text, flags=re.M)
    text = re.sub(r"^\|[^\n]*Domaine ATIH[^\n]*\n", "", text, flags=re.M)
    text = re.sub(r"^\|[^\n]*Plage\s*/\s*Pasrel[^\n]*\n", "", text, flags=re.M | re.I)
    text = re.sub(r"^\|[^\n]*PLAGE\s*/\s*PASREL[^\n]*\n", "", text, flags=re.M)
    # Ligne HTML de tableau contenant DDETS
    text = re.sub(r"^\|[^\n]*DDETS[^\n]*\n", "", text, flags=re.M)
    # Paragraphe de description "Pro Santé Connect authentifie..." (ligne longue)
    text = re.sub(r"^\[?\*?\*?Pro Santé Connect\*?\*?\][^\n]*Professionnels de Santé[^\n]*\n?", "", text, flags=re.M)

    # ── 3. Références Démat Social en texte courant ──────────────────────────────────────
    # "(ou Démat Social)" dans les listes, titres
    text = re.sub(r"\s*\(ou Démat Social\)", "", text)
    # "[Démat Social](url)" → supprimé (lien + texte)
    text = re.sub(r"\[Démat Social\]\([^)]+\)", "", text)
    # "Démat Social" seul dans une phrase
    text = re.sub(r"\bDémat Social\b", "", text)
    # "démat social" (casse basse)
    text = re.sub(r"\bdémat social\b", "", text, flags=re.I)
    # "Démat' Social"
    text = re.sub(r"Démat'\s+Social", "", text)
    # "demat.social.gouv.fr" URLs directes (pas dans un lien Markdown déjà supprimé)
    text = re.sub(r"https?://demat\.social\.gouv\.fr/?[^\s)\"]*", "", text)

    # ── 4. FINESS, RPPS, NIR (champs spécifiques santé) ─────────────────────────────────
    # Lignes de tableau entières qui contiennent ces identifiants
    text = re.sub(r"^\|[^\n]*\bFINESS\b[^\n]*\n", "", text, flags=re.M)
    text = re.sub(r"^\|[^\n]*\bRPPS\b[^\n]*\n", "", text, flags=re.M)
    text = re.sub(r"^\|[^\n]*\bNIR sécurisé\b[^\n]*\n", "", text, flags=re.M)
    # Bullet points listant ces APIs
    text = re.sub(r"^\*\s+API des (établissements|professionnels) de santé[^\n]*\n", "", text, flags=re.M | re.I)
    text = re.sub(r"^-\s+API des (établissements|professionnels) de santé[^\n]*\n", "", text, flags=re.M | re.I)

    # ── 5. PLAGE / PASREL en texte ────────────────────────────────────────────────────────
    text = re.sub(r"\[Plage\s*/\s*Pasrel\]\([^)]+\)[^\n]*", "", text, flags=re.I)
    text = re.sub(r"\bPLAGE\s*/\s*PASREL\b", "", text)
    # "et Plage" quand Plage désigne le système de santé (liste d'espaces partenaires)
    text = re.sub(r",?\s+et Plage\.?(\\)?$", ".", text, flags=re.M)
    text = re.sub(r",?\s+et Plage\b", "", text)
    # Bullet points ou phrases mentionnant Pro Santé Connect (ex: comparaison dans ProConnect)
    text = re.sub(r"^\s*\*\s.*Pro Santé Connect.*\n", "", text, flags=re.M)
    text = re.sub(r"[^\n]*Pro Santé Connect[^\n]*\n", "", text)

    # ── 6. Emails @sg.social.gouv.fr → placeholder ──────────────────────────────────────
    # Lien Markdown [texte](mailto:...@sg.social.gouv.fr)
    text = re.sub(
        r"\[([^\]]+)\]\(mailto:[^\)]*@sg\.social\.gouv\.fr[^\)]*\)",
        r"\1 *(adresse de contact MTE à renseigner)*",
        text,
        flags=re.I,
    )
    # Balise HTML <email@sg.social.gouv.fr>
    text = re.sub(
        r"<[^>]*@sg\.social\.gouv\.fr>",
        "*(adresse de contact MTE à renseigner)*",
        text,
    )
    # Emails bruts ...@sg.social.gouv.fr (sans balisage)
    text = re.sub(
        r"\S+@sg\.social\.gouv\.fr",
        "*(adresse de contact MTE à renseigner)*",
        text,
    )

    # ── 7. Liens GitHub DNUM-SocialGouv → garder le libellé, retirer le lien ───────────
    text = re.sub(
        r"\[([^\]]+)\]\(https://github\.com/DNUM-SocialGouv/[^\)]+\)",
        r"\1",
        text,
    )

    # ── 8. honorabilite.social.gouv.fr dans les exemples ────────────────────────────────
    text = re.sub(r"\[honorabilite\.social\.gouv\.fr[,\.]?\]\([^)]+\)[,\s]*", "", text)
    text = re.sub(r"honorabilite\.social\.gouv\.fr[,\s]*", "", text)

    # ── 9. "pour et par les Ministères Sociaux / Ministère de la Transition…" dans intro DématSocial ──
    # (déjà couvert par apply_org pour le renommage ; ici on retire les traces résiduelles)

    # ── 10. Nettoyage résiduel ───────────────────────────────────────────────────────────
    # Lignes devenues vides (juste "|  |  |" ou "|   |") après suppression des cellules
    text = re.sub(r"^\|\s*\|\s*\|\s*\n", "", text, flags=re.M)
    text = re.sub(r"^\|\s*\|\s*\n", "", text, flags=re.M)
    # Plusieurs lignes blanches consécutives → deux max
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text

# Liens internes opaques GitBook (/pages/ID) résolus avec certitude (texte de lien + cible unique).
PAGE_ID_MAP = {
    "by10ywdpX0pqCBeFFoxB": "concevoir/authentification/authentification-proconnect.md",  # "ProConnect"
    "jduL6pDOtlIqhXokOpHO": "developper/cct/jdk.md",                                        # "Temurin"
}

# Index titre normalisé -> relpath (rempli dans main()), pour relier les cartes par titre.
TITLE_INDEX = {}


def norm_title(s):
    s = re.sub(r"\([^)]*\)", "", s)   # retirer suffixes type (PM), (PO)
    return re.sub(r"\s+", " ", s).strip().lower()


def convert_cards(text):
    """Convertit les tableaux GitBook <table data-view="cards"> en liste Markdown.

    La colonne « libellé » est identifiée via le <thead> (ni content-ref, ni cover).
    Le libellé est relié à une page sœur uniquement si son titre correspond exactement
    (sinon : texte simple, pour ne jamais créer de lien erroné). Les couvertures (/files)
    et les références opaques (/pages/ID) sont abandonnées."""
    def repl(m):
        block = m.group(0)
        thead = re.search(r"<thead>(.*?)</thead>", block, flags=re.S)
        ths = re.findall(r"<th([^>]*)>", thead.group(1)) if thead else []
        label_idx = 0
        for i, attrs in enumerate(ths):
            is_ref = "content-ref" in attrs
            is_cover = "data-card-cover" in attrs or 'data-type="files"' in attrs
            if not is_ref and not is_cover:
                label_idx = i
                break
        tbody = re.search(r"<tbody>(.*?)</tbody>", block, flags=re.S)
        rows = re.findall(r"<tr>(.*?)</tr>", tbody.group(1), flags=re.S) if tbody else []
        items = []
        for row in rows:
            tds = re.findall(r"<td[^>]*>(.*?)</td>", row, flags=re.S)
            if label_idx >= len(tds):
                continue
            label = re.sub(r"<[^>]+>", "", tds[label_idx]).strip()
            if not label:
                continue
            rel = TITLE_INDEX.get(norm_title(label))
            items.append(f"* [{label}](/{rel})" if rel else f"* {label}")
        return "\n".join(items) + "\n" if items else ""
    return re.sub(r'<table data-view="cards">.*?</table>', repl, text, flags=re.S)


def parse_llms():
    entries = []
    with open(os.path.join(ROOT, "llms.txt"), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            m = re.match(r"-\s+\[(.+?)\]\((https://\S+?)\)(?::\s*(.*))?$", line)
            if m:
                entries.append((m.group(1).strip(), m.group(2).strip(), (m.group(3) or "").strip()))
    return entries


def url_to_relpath(url):
    rel = url[len(BASE):]
    return "index.md" if rel == "readme.md" else rel


def clean_gitbook(text):
    # 0. Convertir les composants "cards" GitBook en listes Markdown
    text = convert_cards(text)
    # 1. Retirer la ligne d'en-tête "> For the complete documentation index..."
    text = re.sub(r"^> For the complete documentation index.*?\n", "", text, flags=re.S | re.M)
    # 2. Couper tout ce qui suit "# Agent Instructions"
    text = re.split(r"\n#+\s*Agent Instructions", text)[0]
    # 3. hint -> admonition
    def hint_repl(m):
        style = HINT_MAP.get(m.group(1), "note")
        body = m.group(2).strip("\n")
        body = "\n".join("    " + l if l.strip() else "" for l in body.splitlines())
        return f"!!! {style}\n\n{body}\n"
    text = re.sub(r'\{%\s*hint\s+style="(\w+)"\s*%\}(.*?)\{%\s*endhint\s*%\}',
                  hint_repl, text, flags=re.S)
    # 4. content-ref -> lien
    def cref_repl(m):
        url = m.group(1)
        return f"\n➡️ Voir : <{url}>\n"
    text = re.sub(r'\{%\s*content-ref\s+url="([^"]+)"\s*%\}.*?\{%\s*endcontent-ref\s*%\}',
                  cref_repl, text, flags=re.S)
    # 5. embed -> lien simple
    text = re.sub(r'\{%\s*embed\s+url="([^"]+)"\s*%\}', r"<\1>", text)
    text = re.sub(r'\{%\s*endembed\s*%\}', "", text)
    # 6. file / autres balises {% ... %} restantes : on retire la balise en gardant un éventuel url=
    def file_repl(m):
        inner = m.group(0)
        u = re.search(r'url="([^"]+)"|src="([^"]+)"', inner)
        if u:
            link = u.group(1) or u.group(2)
            return f"<{link}>"
        return ""
    text = re.sub(r'\{%\s*(?:file|tabs|tab|endtabs|endtab|code|endcode|stepper|step|endstep|endstepper|columns|column|endcolumns|endcolumn)[^%]*%\}',
                  file_repl, text)
    # 7. Toute balise {% ... %} résiduelle -> supprimée
    text = re.sub(r"\{%.*?%\}", "", text, flags=re.S)
    # 8. Liens absolus du gitbook source -> liens relatifs
    text = text.replace(BASE, "/")
    text = text.replace("https://dnum-ministeres-sociaux.gitbook.io/ressources", "")
    # 9. Assets GitBook (/files/...) non récupérables : retirer les images mortes,
    #    conserver le libellé pour les liens. (après normalisation des URLs absolues)
    text = re.sub(r"!\[[^\]]*\]\(/files/[^)]*\)", "", text)
    text = re.sub(r"\[([^\]]*)\]\(/files/[^)]*\)", r"\1", text)
    return text


def apply_org(text):
    for pat, repl in ORG_REPLACEMENTS:
        text = re.sub(pat, repl, text)
    return text


def fix_links(text, current_rel, valid):
    """Réécrit les liens internes (absolus façon GitBook) en chemins relatifs MkDocs valides."""
    cur_dir = os.path.dirname(current_rel)

    # Liens opaques /pages/ID -> cible connue.
    #  - Markdown ](/pages/ID) -> ](/relpath.md), résolu ensuite par repl() ci-dessous.
    text = re.sub(r"\]\(/pages/([A-Za-z0-9]+)\)",
                  lambda m: f"](/{PAGE_ID_MAP[m.group(1)]})" if m.group(1) in PAGE_ID_MAP else m.group(0),
                  text)
    #  - HTML href="/pages/ID" -> URL-répertoire MkDocs relative (le HTML brut n'est pas réécrit par MkDocs).
    def html_pid(m):
        rid = m.group(1)
        if rid not in PAGE_ID_MAP:
            return m.group(0)
        rel = os.path.relpath(PAGE_ID_MAP[rid][:-3], cur_dir or ".") + "/"
        return f'href="{rel}"'
    text = re.sub(r'href="/pages/([A-Za-z0-9]+)"', html_pid, text)

    def repl(m):
        label, target = m.group(1), m.group(2).strip()
        if re.match(r"^(https?:|mailto:|tel:|#)", target):
            return m.group(0)
        path, _, anchor = target.partition("#")
        # Normaliser vers un relpath depuis la racine docs/
        cand = path
        if cand.startswith("/ressources/"):
            cand = cand[len("/ressources/"):]
        elif cand.startswith("/"):
            cand = cand[1:]
        if cand in ("readme.md", "ressources/readme.md", ""):
            cand = "index.md"
        if cand not in valid:
            return m.group(0)  # ex: /files/... (asset non récupéré) -> laissé tel quel
        relp = os.path.relpath(cand, cur_dir or ".")
        if anchor:
            relp += "#" + anchor
        return f"[{label}]({relp})"

    return re.sub(r"\[([^\]]*)\]\(([^)]+)\)", repl, text)


def process_all(entries):
    titles = {}        # relpath -> titre (depuis llms.txt)
    cleaned = {}       # relpath -> contenu nettoyé (avant réécriture des liens)
    for title, url, desc in entries:
        rel = url_to_relpath(url)
        titles[rel] = title
        if rel in SKIP_PAGES:
            continue   # page santé/social supprimée
        src = os.path.join(RAW, rel)
        if not os.path.exists(src):
            print("  MANQUE:", rel)
            continue
        with open(src, encoding="utf-8") as f:
            text = f.read()
        text = clean_social(text, rel)  # avant tout — sur le texte brut
        text = clean_gitbook(text)
        text = apply_org(text)
        cleaned[rel] = text.strip() + "\n"

    # Les pages supprimées ne font pas partie des liens valides
    valid = set(cleaned.keys())
    for rel, text in cleaned.items():
        text = fix_links(text, rel, valid)
        dest = os.path.join(DOCS, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(text)
    return titles


# ---------- Construction de la navigation ----------
SECTION_TITLES = {
    "cadrer": "Cadrer", "concevoir": "Concevoir", "developper": "Développer",
    "deployer": "Déployer", "aide": "Aide",
}


def build_nav(entries):
    """Construit une nav imbriquée en respectant l'ordre de llms.txt et la profondeur des chemins.

    Une page parente possédant des enfants devient une section dont la 1re entrée
    est la page elle-même.
    """
    # Liste ordonnée de (relpath, title) — hors pages supprimées
    pages = [(url_to_relpath(u), t) for t, u, d in entries if url_to_relpath(u) not in SKIP_PAGES]

    # Index des enfants par préfixe de dossier
    def stem(rel):
        return rel[:-3]  # retire .md

    rel_set = {r for r, _ in pages}
    # Un dossier "X/" correspond à une page X.md (parent) si elle existe.
    nav = ["index.md"]  # accueil

    # Grouper par section (1er segment), en gardant l'ordre d'apparition
    sections = []
    seen = set()
    for rel, _ in pages:
        if rel == "index.md":
            continue
        seg = rel.split("/")[0]
        if seg not in seen:
            seen.add(seg)
            sections.append(seg)

    def children_of(prefix_stem):
        """Pages directement enfants de prefix_stem (dossier = stem)."""
        res = []
        for rel, title in pages:
            if rel == "index.md":
                continue
            d = os.path.dirname(rel)
            if d == prefix_stem:
                res.append((rel, title))
        return res

    def make_entry(rel, title):
        st = stem(rel)
        kids = children_of(st)
        if not kids:
            return {title: rel}
        # page parente avec enfants -> section
        items = [{title: rel}]
        for k_rel, k_title in kids:
            items.append(make_entry(k_rel, k_title))
        return {title: items}

    for seg in sections:
        seg_title = SECTION_TITLES.get(seg, seg.capitalize())
        # pages dont le 1er segment == seg et qui sont au 1er niveau (dossier == seg)
        top = [(r, t) for r, t in pages if r.split("/")[0] == seg and os.path.dirname(r) == seg]
        items = [make_entry(r, t) for r, t in top]
        nav.append({seg_title: items})
    return nav


def yaml_nav(nav, indent=2):
    """Sérialise la nav (liste de str|dict) en YAML lisible."""
    lines = []
    pad = " " * indent

    def emit(items, level):
        for it in items:
            p = pad * level
            if isinstance(it, str):
                lines.append(f"{p}- {it}")
            else:
                (k, v), = it.items()
                key = k.replace('"', '\\"')
                if isinstance(v, str):
                    lines.append(f'{p}- "{key}": {v}')
                else:
                    lines.append(f'{p}- "{key}":')
                    emit(v, level + 1)
    emit(nav, 1)
    return "\n".join(lines)


def write_mkdocs(nav):
    nav_yaml = yaml_nav(nav)
    cfg = f"""site_name: Guide DNUM — Ministère de la Transition Écologique
site_description: Ressources, méthodes et bonnes pratiques de la Direction du Numérique (DNUM) du Ministère de la Transition Écologique (MTE).
site_author: DNUM du Ministère de la Transition Écologique
docs_dir: docs

theme:
  name: material
  language: fr
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-night
        name: Passer en mode sombre
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-sunny
        name: Passer en mode clair
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.sections
    - navigation.top
    - navigation.indexes
    - toc.follow
    - search.suggest
    - search.highlight
    - content.code.copy

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.highlight
  - pymdownx.tabbed:
      alternate_style: true
  - tables
  - attr_list
  - md_in_html
  - toc:
      permalink: true

plugins:
  - search:
      lang: fr

nav:
{nav_yaml}
"""
    with open(os.path.join(ROOT, "mkdocs.yml"), "w", encoding="utf-8") as f:
        f.write(cfg)


def main():
    entries = parse_llms()
    active = [(t, u, d) for t, u, d in entries if url_to_relpath(u) not in SKIP_PAGES]
    print(f"{len(entries)} pages sources, {len(active)} conservées ({len(entries)-len(active)} supprimées)")
    for title, url, desc in active:
        TITLE_INDEX[norm_title(title)] = url_to_relpath(url)
    process_all(entries)   # entries complet — skip interne
    nav = build_nav(active)  # nav uniquement sur les pages actives
    write_mkdocs(nav)
    n = sum(1 for _ in __import__('pathlib').Path(DOCS).rglob("*.md"))
    print(f"docs/: {n} fichiers .md générés ; mkdocs.yml écrit.")


if __name__ == "__main__":
    main()
