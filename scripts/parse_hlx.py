#!/usr/bin/env python3
"""
Parse Line 6 Helix .hlx preset files (they're text-based!)
Extract structure and settings for analysis
"""

import json
import re
from pathlib import Path
from typing import Dict, Any

def read_hlx_file(filepath: Path) -> str:
    """Read .hlx file as text"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def parse_hlx_structure(hlx_text: str) -> Dict[str, Any]:
    """
    Parse .hlx text into structured data

    Returns dict with:
    - name: preset name
    - blocks: list of effect/amp blocks
    - routing: signal routing info
    - snapshots: snapshot configurations
    """
    # This is a STARTER - you'll refine based on actual .hlx structure
    preset_data = {
        "name": "",
        "blocks": [],
        "routing": {},
        "snapshots": []
    }

    # Extract preset name (usually near top of file)
    name_match = re.search(r'"name"\s*:\s*"([^"]+)"', hlx_text)
    if name_match:
        preset_data["name"] = name_match.group(1)

    # Extract blocks (amps, effects, etc.)
    # Pattern will vary - inspect actual .hlx file to refine
    block_pattern = r'"dsp(\d+)"\s*:\s*{([^}]+)}'
    blocks = re.findall(block_pattern, hlx_text)

    for block_id, block_content in blocks:
        preset_data["blocks"].append({
            "id": f"dsp{block_id}",
            "content": block_content
        })

    return preset_data

def extract_amp_settings(preset_data: Dict) -> Dict:
    """Extract amp model and settings"""
    # Placeholder - refine based on actual structure
    amp_settings = {
        "model": "Unknown",
        "gain": 0,
        "bass": 0,
        "mid": 0,
        "treble": 0
    }
    return amp_settings

def main():
    """Parse all .hlx files in study_presets/"""
    study_dir = Path("study_presets")

    for hlx_file in study_dir.glob("*.hlx"):
        print(f"\n📁 Parsing: {hlx_file.name}")

        hlx_text = read_hlx_file(hlx_file)
        preset_data = parse_hlx_structure(hlx_text)

        print(f"   Name: {preset_data['name']}")
        print(f"   Blocks: {len(preset_data['blocks'])}")

        # Save parsed data as JSON for analysis
        output_file = hlx_file.with_suffix('.json')
        with open(output_file, 'w') as f:
            json.dump(preset_data, f, indent=2)

        print(f"   ✅ Saved to: {output_file}")

if __name__ == "__main__":
    main()
