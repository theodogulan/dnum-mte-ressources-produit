#!/usr/bin/env python3
"""Télécharge toutes les pages .md du GitBook source dans raw/, en préservant l'arborescence."""
import os, re, time, urllib.request

BASE = "https://dnum-ministeres-sociaux.gitbook.io/ressources/"
ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "raw")

def parse_llms():
    """Retourne une liste de (titre, url, description) dans l'ordre du document."""
    entries = []
    with open(os.path.join(ROOT, "llms.txt"), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            m = re.match(r"-\s+\[(.+?)\]\((https://\S+?)\)(?::\s*(.*))?$", line)
            if m:
                entries.append((m.group(1).strip(), m.group(2).strip(),
                                (m.group(3) or "").strip()))
    return entries

def url_to_relpath(url):
    rel = url[len(BASE):]  # ex: cadrer/xxx.md  ou readme.md
    if rel == "readme.md":
        return "index.md"
    return rel

def main():
    entries = parse_llms()
    print(f"{len(entries)} pages à télécharger")
    for i, (title, url, desc) in enumerate(entries, 1):
        rel = url_to_relpath(url)
        dest = os.path.join(RAW, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            print(f"[{i:>2}/{len(entries)}] cache  {rel}")
            continue
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            with open(dest, "wb") as out:
                out.write(data)
            print(f"[{i:>2}/{len(entries)}] OK     {rel} ({len(data)} o)")
        except Exception as e:
            print(f"[{i:>2}/{len(entries)}] ERREUR {rel}: {e}")
        time.sleep(0.3)

if __name__ == "__main__":
    main()
