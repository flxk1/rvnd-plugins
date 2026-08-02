#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2026 flxk1
"""Fail closed when the RVND catalog and its pinned source disagree."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(f"MARKETPLACE GATE FAIL: {message}")


def load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"cannot read {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()

    market = load(ROOT / ".claude-plugin" / "marketplace.json")
    plugins = market.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        fail("catalog must contain exactly one canonical plugin")
    entry = plugins[0]
    source = entry.get("source")
    if not isinstance(source, dict) or source.get("source") != "github":
        fail("plugin source must use Claude's supported github source type")
    if source.get("repo") != "flxk1/RVND":
        fail("plugin source must remain owned by flxk1/RVND")
    if not re.fullmatch(r"[0-9a-f]{40}", str(source.get("sha", ""))):
        fail("plugin source must pin a full immutable commit")

    manifest = load(args.source_root / ".claude-plugin" / "plugin.json")
    for field in ("name", "version"):
        if manifest.get(field) != entry.get(field):
            fail(f"catalog and source disagree on {field}")
    if manifest.get("license") != "AGPL-3.0-only":
        fail("source plugin must remain AGPL-3.0-only")
    for field in ("skills", "mcpServers"):
        relative = manifest.get(field)
        if not isinstance(relative, str) or not relative.startswith("./"):
            fail(f"source plugin {field} must be a repository-local path")
        target = args.source_root / relative.removeprefix("./")
        if not target.exists():
            fail(f"source plugin {field} path does not exist: {relative}")
    skill_root = args.source_root / manifest["skills"].removeprefix("./")
    if not list(skill_root.glob("*/SKILL.md")):
        fail("source plugin exposes no discoverable skills")

    print(
        f"MARKETPLACE GATE PASS: {entry['name']} {entry['version']} "
        f"@ {source['sha']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
