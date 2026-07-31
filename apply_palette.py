"""One-time MedIntel AI palette update.
Run this file once from the folder that contains app.py.
It only replaces colour values; it does not change any feature, text, layout, or logic.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
PALETTE = {"blue": "#4CA9EE", "teal": "#238878", "green": "#5ECD81", "grey": "#B2B7BB"}

# Each original visual colour is assigned to one of the four colours supplied.
COLOURS = {
    # original dark backgrounds / neutral text / borders
    "0b1220":"grey", "111827":"grey", "172033":"grey", "1e293b":"grey",
    "2b3648":"teal", "334155":"teal", "475569":"teal", "64748b":"teal",
    "94a3b8":"teal", "aebbd0":"teal", "cbd5e1":"teal", "e2e8f0":"teal",
    "f8fafc":"teal", "e4ecfa":"teal", "edf3ff":"teal", "9eabc0":"teal",
    "d1fae5":"teal", "fef3c7":"teal", "fcd34d":"teal",
    # blues / purples
    "2563eb":"blue", "1d4ed8":"blue", "60a5fa":"blue", "93c5fd":"blue",
    "bfdbfe":"blue", "1e3a5f":"blue", "0f2744":"blue", "0f1f3d":"blue",
    "1a2f5c":"blue", "7c3aed":"blue", "a78bfa":"blue", "c4b5fd":"blue",
    "0891b2":"blue",
    # greens
    "059669":"green", "16a34a":"green", "4ade80":"green", "34d399":"green",
    "6ee7b7":"green", "052e16":"green",
    # warm/red colours become teal, to retain only the requested four palette colours
    "d97706":"teal", "f59e0b":"teal", "fbbf24":"teal", "fcd34d":"teal",
    "92400e":"teal", "451a03":"teal", "1c1a07":"teal", "1c1207":"teal",
    "dc2626":"teal", "f87171":"teal", "450a0a":"teal",
}

# RGB values in existing transparent plot backgrounds and gradients.
RGB = {
    "37,99,235":"blue", "96,165,250":"blue", "124,58,237":"blue",
    "5,150,105":"green", "74,222,128":"green",
}

def replace_hex(match):
    old = match.group(1).lower()
    return PALETTE[COLOURS.get(old, "grey")]

def replace_rgba(match):
    rgb, alpha = match.group(1).replace(" ", ""), match.group(2)
    chosen = PALETTE[RGB.get(rgb, "grey")]
    r, g, b = (int(chosen[i:i+2], 16) for i in (1, 3, 5))
    return f"rgba({r},{g},{b},{alpha})"

changed = []
for path in ROOT.rglob("*.py"):
    if path.name == "apply_palette.py" or ".venv" in path.parts:
        continue
    content = path.read_text(encoding="utf-8")
    updated = re.sub(r"#([0-9A-Fa-f]{6})\b", replace_hex, content)
    updated = re.sub(r"rgba\(\s*([0-9]+\s*,\s*[0-9]+\s*,\s*[0-9]+)\s*,\s*([0-9.]+)\s*\)", replace_rgba, updated)
    if updated != content:
        path.write_text(updated, encoding="utf-8")
        changed.append(path.relative_to(ROOT).as_posix())

print("Palette applied successfully. Only colour values were updated in:")
print("\n".join(changed) if changed else "No old colour values found.")
