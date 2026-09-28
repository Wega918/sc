#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLASES = ROOT / "public/assets/atlases"
SFX = ROOT / "public/assets/audio/sfx"
ANIMATIONS = ROOT / "public/data/csv/animations.json"
OUT = ROOT / "public/data/runtime/unit-catalog.js"


def title(unit_id: str) -> str:
    return unit_id.removeprefix("chr_").replace("_", " ").title()


def tokens(unit_id: str):
    aliases = {
        "barbarian": ["barbarian", "barb", "new_barb"],
        "archer": ["archer", "new_archer"],
        "goblin": ["goblin", "gob_"],
        "wizard": ["wizard", "mage_"],
        "wall_breaker": ["wallbreaker", "wall_breaker", "bomber"],
    }
    base = unit_id.removeprefix("chr_")
    found = [base]
    for key, values in aliases.items():
        if key in base:
            found.extend(values)
    return sorted(set(found), key=len, reverse=True)


def main():
    animation_doc = json.loads(ANIMATIONS.read_text(encoding="utf-8"))
    groups = animation_doc.get("groups", {})
    audio_names = sorted(p.name for p in SFX.glob("*.ogg"))
    units = []

    for folder in sorted(p for p in ATLASES.iterdir() if p.is_dir() and p.name.startswith("chr_")):
        unit_id = folder.name
        atlas_files = sorted(folder.glob("*.webp"))
        swf = f"sc/{unit_id}.sc"
        matching_groups = {}
        for group_name, group in groups.items():
            actions = group.get("actions", {}) if isinstance(group, dict) else {}
            relevant = {}
            for action_name, variants in actions.items():
                selected = [v for v in variants if isinstance(v, dict) and v.get("swf") == swf]
                if selected:
                    relevant[action_name] = selected
            if relevant:
                matching_groups[group_name] = relevant

        low_tokens = tokens(unit_id)
        candidates = [name for name in audio_names if any(t in name.lower() for t in low_tokens)]
        deploy = [n for n in candidates if re.search(r"deploy|dep_", n, re.I)][:4]
        attack = [n for n in candidates if re.search(r"attack|atk|hit|swing", n, re.I)][:6]
        death = [n for n in candidates if re.search(r"death|die", n, re.I)][:3]
        units.append({
            "id": unit_id,
            "name": title(unit_id),
            "atlas": f"public/assets/atlases/{unit_id}/{atlas_files[0].name}" if atlas_files else None,
            "atlasCount": len(atlas_files),
            "sc": swf,
            "animationGroups": matching_groups,
            "renderMode": "sc" if unit_id == "chr_barbarian" else "marker",
            "speed": 54 + (sum(map(ord, unit_id)) % 25),
            "damage": 8 + (sum(map(ord, unit_id[::-1])) % 17),
            "sounds": {"deploy": deploy, "attack": attack, "death": death},
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {"format": "web_game_unit_catalog_v1", "count": len(units), "units": units}
    OUT.write_text("window.UNIT_CATALOG=" + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print(f"Wrote {len(units)} units to {OUT}")


if __name__ == "__main__":
    main()
