#!/usr/bin/env python3
"""Install decoded runtime SC data as lazy file:// compatible JavaScript."""
from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parents[1] / "runtime_full" / "SC_Runtime_JSON_verified" / "runtime"
OUT = ROOT / "public" / "data" / "runtime" / "sc"
CATALOG = ROOT / "public" / "data" / "runtime" / "unit-catalog.js"


def load_catalog():
    text = CATALOG.read_text("utf-8")
    return json.loads(text.split("=", 1)[1].rstrip(" ;\r\n"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.js"):
        old.unlink()
    catalog = load_catalog()
    installed = 0
    for unit in catalog["units"]:
        src = SOURCE / f"{unit['id']}.runtime.json"
        if not src.exists():
            unit["renderMode"] = "unavailable"
            continue
        data = json.loads(src.read_text("utf-8"))
        unit["runtimeScript"] = f"public/data/runtime/sc/{unit['id']}.js"
        unit["atlases"] = [
            f"public/assets/atlases/{unit['id']}/{Path(a['file']).stem}.webp"
            for a in data.get("atlases", [])
        ]
        unit["renderMode"] = "sc"
        payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        js = (
            "window.SC_RUNTIME_DATA=window.SC_RUNTIME_DATA||{};"
            f"window.SC_RUNTIME_DATA[{json.dumps(unit['id'])}]={payload};\n"
        )
        (OUT / f"{unit['id']}.js").write_text(js, "utf-8")
        installed += 1
    catalog["runtimeInstalled"] = installed
    CATALOG.write_text(
        "window.UNIT_CATALOG=" + json.dumps(catalog, ensure_ascii=False, separators=(",", ":")) + ";\n",
        "utf-8",
    )
    status = {
        "format": "sc_battle_runtime_status_v1",
        "catalog_units": len(catalog["units"]),
        "runtime_installed": installed,
        "missing_runtime": [u["id"] for u in catalog["units"] if u.get("renderMode") != "sc"],
        "file_mode": "lazy JavaScript wrappers; fetch/local server not required",
    }
    (ROOT / "public" / "data" / "runtime" / "runtime-status.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=2) + "\n", "utf-8"
    )
    print(f"installed runtime SC for {installed}/{len(catalog['units'])} units")


if __name__ == "__main__":
    main()
