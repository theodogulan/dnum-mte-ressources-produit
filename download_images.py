#!/usr/bin/env python3
"""Récupère les images de contenu (balises <figure><img src="/files/ID">) restées non résolues.

Pour chaque page docs/*.md contenant des références /files/, on télécharge la page rendue,
on extrait dans l'ordre les images de contenu (spaces/.../uploads/...), on les enregistre sous
docs/assets/<page>/ et on réécrit les <img src> en chemins relatifs.
"""
import os, re, html, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
SRC_BASE = "https://dnum-ministeres-sociaux.gitbook.io/ressources/"
UA = {"User-Agent": "Mozilla/5.0"}


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read() if binary else r.read().decode("utf-8", "replace")


def content_images(html_text):
    """URLs directes des images de contenu, dans l'ordre du document, dédupliquées."""
    out, seen = [], set()
    for m in re.finditer(r'image\?url=([^"&]+)', html_text):
        dec = urllib.parse.unquote(html.unescape(m.group(1)))
        if "uploads" not in dec:
            continue  # logos / icônes / ogimage -> ignorés
        if dec in seen:
            continue
        seen.add(dec)
        out.append(dec)
    return out


def ext_of(url):
    path = urllib.parse.urlparse(url).path
    e = os.path.splitext(path)[1].lower()
    return e if e in (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp") else ".png"


def main():
    md_files = []
    for dirpath, _, names in os.walk(DOCS):
        for n in names:
            if n.endswith(".md"):
                p = os.path.join(dirpath, n)
                if "/files/" in open(p, encoding="utf-8").read():
                    md_files.append(p)
    print(f"{len(md_files)} pages avec images à résoudre")

    for p in sorted(md_files):
        rel = os.path.relpath(p, DOCS)
        page_url = SRC_BASE + rel[:-3]  # sans .md
        text = open(p, encoding="utf-8").read()
        file_ids = re.findall(r'src="(/files/[^"]+)"', text)
        try:
            page_html = fetch(page_url)
        except Exception as e:
            print(f"  ERREUR HTML {rel}: {e}")
            continue
        imgs = content_images(page_html)
        slug = rel[:-3].replace("/", "__")
        assets_dir = os.path.join(DOCS, "assets", slug)
        n = min(len(file_ids), len(imgs))
        if len(file_ids) != len(imgs):
            print(f"  ⚠ {rel}: {len(file_ids)} refs /files vs {len(imgs)} images trouvées -> {n} mappées")
        os.makedirs(assets_dir, exist_ok=True)
        for i in range(n):
            url = imgs[i]
            fname = f"img{i+1}{ext_of(url)}"
            try:
                data = fetch(url, binary=True)
            except Exception as e:
                print(f"    ERREUR img {url[:60]}: {e}")
                continue
            with open(os.path.join(assets_dir, fname), "wb") as f:
                f.write(data)
            # chemin relatif depuis la page vers l'asset
            relpath = os.path.relpath(os.path.join(assets_dir, fname), os.path.dirname(p))
            text = text.replace(file_ids[i], relpath, 1)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"  OK {rel}: {n} image(s)")


if __name__ == "__main__":
    main()
