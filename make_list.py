"""Build gifs.json from the files in the gifs/ folder.

Run from the repo root after adding or removing files:
    python make_list.py

Categories and titles already in gifs.json are kept for files that still exist.
"""
import json
import pathlib

root = pathlib.Path(__file__).parent
exts = {".gif", ".webp", ".png", ".jpg", ".jpeg", ".avif", ".mp4", ".webm"}

files = sorted(p.name for p in (root / "gifs").iterdir() if p.suffix.lower() in exts)

categories, old = [], {}
try:
    data = json.loads((root / "gifs.json").read_text(encoding="utf-8"))
    if isinstance(data, dict):
        categories = data.get("categories", [])
        old = {g["file"]: g for g in data.get("gifs", []) if "file" in g}
except FileNotFoundError:
    pass

gifs = []
for name in files:
    prev = old.get(name, {})
    title = prev.get("title") or pathlib.Path(name).stem.replace("_", " ").replace("-", " ")
    gifs.append({"file": name, "title": title, "categories": prev.get("categories", [])})

(root / "gifs.json").write_text(
    json.dumps({"categories": categories, "gifs": gifs}, indent=1, ensure_ascii=False),
    encoding="utf-8",
)
print(f"Wrote gifs.json with {len(gifs)} files")
