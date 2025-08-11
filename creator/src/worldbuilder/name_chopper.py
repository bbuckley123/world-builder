# worldbuilder/name_chopper.py
from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import Any, Dict, List

import yaml

from worldbuilder.paths import NAMES_RAW_YAML, NAMES_YAML


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_yaml(data: Dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def chop_list(items: List[Any], max_len: int, rng: random.Random) -> List[Any]:
    if max_len < 0:
        return items  # negative means ignore/keep all
    if not isinstance(items, list):
        return items
    if len(items) <= max_len:
        return items
    # Keep a random subset of size max_len, preserving no particular order
    return rng.sample(items, max_len)


def apply_limits(world: Dict[str, Any], limits: Dict[str, int], rng: random.Random) -> Dict[str, Any]:
    # Top-level oceans
    if "oceans" in limits and isinstance(world.get("oceans"), list):
        world["oceans"] = chop_list(world["oceans"], limits["oceans"], rng)

    # Top-level continents
    if "continents" in limits and isinstance(world.get("continents"), list):
        world["continents"] = chop_list(world["continents"], limits["continents"], rng)

    # Within each continent: regions & cities
    for c in world.get("continents", []) or []:
        if "regions" in limits and isinstance(c.get("regions"), list):
            c["regions"] = chop_list(c["regions"], limits["regions"], rng)
        if "cities" in limits and isinstance(c.get("cities"), list):
            c["cities"] = chop_list(c["cities"], limits["cities"], rng)

    return world


def parse_limits(kv_pairs: List[str]) -> Dict[str, int]:
    """
    Accepts ["oceans=1", "continents=2", "cities=2", "regions=1"] → dict
    Unknown keys are allowed but only these 4 are applied.
    """
    out: Dict[str, int] = {}
    for pair in kv_pairs:
        if "=" not in pair:
            raise ValueError(f"Invalid limit '{pair}'. Use key=value (e.g., oceans=1).")
        k, v = pair.split("=", 1)
        k = k.strip().lower()
        try:
            out[k] = int(v.strip())
        except ValueError as e:
            raise ValueError(f"Limit for '{k}' must be an integer, got '{v}'.") from e
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Randomly trim world YAML entities to specified maximum counts."
    )
    parser.add_argument(
        "--limit",
        "-l",
        action="append",
        default=[],
        help="Set a max: oceans=1, continents=2, regions=1, cities=2. "
             "Repeat for multiple (e.g., -l oceans=1 -l continents=2).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional RNG seed for reproducible chopping.",
    )
    parser.add_argument(
        "--in",
        dest="in_path",
        type=Path,
        default=NAMES_RAW_YAML,
        help="Input YAML path (defaults to NAMES_RAW_PATH).",
    )
    parser.add_argument(
        "--out",
        dest="out_path",
        type=Path,
        default=NAMES_YAML,
        help="Output YAML path (defaults to NAMES_PATH).",
    )
    args = parser.parse_args()

    limits = parse_limits(args.limit)
    rng = random.Random(args.seed)

    world = load_yaml(args.in_path)
    world = apply_limits(world, limits, rng)
    save_yaml(world, args.out_path)


if __name__ == "__main__":
    main()
