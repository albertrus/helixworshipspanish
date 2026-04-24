#!/usr/bin/env python3
"""
Parse Line 6 Helix .hlx preset files (JSON-based).

Produces a JSON summary (name, tempo, per-DSP block list with model/enabled/position,
snapshot names and per-block bypass states) alongside each .hlx in study_presets/.
"""

import json
from pathlib import Path
from typing import Any

SPECIAL_BLOCK_MODELS = {
    "HD2_AppDSPFlowJoin",
    "HD2_AppDSPFlowSplitY",
    "HD2_AppDSPFlow1Input",
    "HD2_AppDSPFlow2Input",
    "HD2_AppDSPFlowOutput",
}


def load_hlx(filepath: Path) -> dict[str, Any]:
    with filepath.open("r", encoding="utf-8") as f:
        return json.load(f)


def summarize_dsp(dsp: dict[str, Any]) -> list[dict[str, Any]]:
    blocks = []
    for key, val in dsp.items():
        if not isinstance(val, dict) or "@model" not in val:
            continue
        model = val["@model"]
        if model in SPECIAL_BLOCK_MODELS:
            continue
        blocks.append({
            "slot": key,
            "model": model,
            "position": val.get("@position"),
            "enabled": val.get("@enabled"),
            "type": val.get("@type"),
        })
    blocks.sort(key=lambda b: (b["position"] is None, b["position"]))
    return blocks


def summarize_snapshots(tone: dict[str, Any]) -> list[dict[str, Any]]:
    snapshots = []
    for i in range(8):
        snap = tone.get(f"snapshot{i}")
        if not isinstance(snap, dict):
            continue
        snapshots.append({
            "index": i,
            "name": snap.get("@name"),
            "tempo": snap.get("@tempo"),
            "blocks": snap.get("blocks"),
        })
    return snapshots


def summarize_preset(data: dict[str, Any]) -> dict[str, Any]:
    root = data.get("data", {})
    meta = root.get("meta", {})
    tone = root.get("tone", {})
    global_cfg = tone.get("global", {}) if isinstance(tone.get("global"), dict) else {}

    return {
        "name": meta.get("name"),
        "application": meta.get("application"),
        "tempo": global_cfg.get("@tempo"),
        "current_snapshot": global_cfg.get("@current_snapshot"),
        "dsp0": summarize_dsp(tone.get("dsp0", {})),
        "dsp1": summarize_dsp(tone.get("dsp1", {})),
        "snapshots": summarize_snapshots(tone),
    }


def main() -> None:
    study_dir = Path("study_presets")
    if not study_dir.is_dir():
        raise SystemExit(f"Directory not found: {study_dir}")

    hlx_files = sorted(study_dir.glob("*.hlx"))
    if not hlx_files:
        raise SystemExit(f"No .hlx files in {study_dir}")

    for hlx_file in hlx_files:
        print(f"Parsing: {hlx_file.name}")
        data = load_hlx(hlx_file)
        summary = summarize_preset(data)

        print(f"  name       : {summary['name']}")
        print(f"  tempo      : {summary['tempo']}")
        print(f"  dsp0 blocks: {len(summary['dsp0'])}")
        print(f"  dsp1 blocks: {len(summary['dsp1'])}")
        print(f"  snapshots  : {[s['name'] for s in summary['snapshots']]}")

        out = hlx_file.with_suffix(".summary.json")
        with out.open("w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"  -> {out.name}\n")


if __name__ == "__main__":
    main()
