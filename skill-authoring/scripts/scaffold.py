#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# ///
"""Create a new Agent Skill skeleton directory.

Usage:
    python3 scripts/scaffold.py <name> [--out DIR] [--force]

Example:
    python3 scripts/scaffold.py pdf-processing --out ./skills
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_NAME_LEN = 64

# Preferred template: assets/templates/SKILL.md.template (relative to the skill root).
TEMPLATE_PATH = (
    Path(__file__).resolve().parent.parent / "assets" / "templates" / "SKILL.md.template"
)

# Fallback used when the template file is missing.
SKILL_MD_TEMPLATE = """---
name: {name}
description: >
  TODO: 用一两句说明这个技能做什么，以及什么时候使用它。
  务必同时写清「做什么」与「何时用」，并带上便于检索的关键词。
---

# {title}

## 何时使用

TODO: 一句话说明适用场景，并点明不适用的情况。

## 快速开始

1. TODO

## 核心流程

1. TODO

## 资源路由表

| 当任务涉及… | 读取 |
|---|---|
| TODO | TODO |

## Gotchas

- TODO: 记录反直觉、容易踩坑的事实。
"""


def titleize(name: str) -> str:
    """Turn ``pdf-processing`` into ``Pdf Processing``."""
    return " ".join(word.capitalize() for word in name.split("-"))


def validate_name(name: str) -> list[str]:
    """Return a list of problems with ``name`` (empty means valid)."""
    errors: list[str] = []
    if not name:
        return ["name must not be empty"]
    if len(name) > MAX_NAME_LEN:
        errors.append(f"name exceeds {MAX_NAME_LEN} characters ({len(name)})")
    if name != name.lower():
        errors.append("name must be lowercase")
    if not NAME_RE.match(name):
        errors.append(
            "name may only contain lowercase letters, digits, "
            "and single hyphens (no leading/trailing/double hyphens)"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a new Agent Skill skeleton directory."
    )
    parser.add_argument("name", help="Skill name in kebab-case; also the directory name")
    parser.add_argument("--out", default=".", help="Parent directory (default: current dir)")
    parser.add_argument("--force", action="store_true", help="Write into a non-empty directory")
    args = parser.parse_args()

    errors = validate_name(args.name)
    if errors:
        print("Error: invalid skill name.", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        print(
            "Example: python3 scripts/scaffold.py pdf-processing --out ./skills",
            file=sys.stderr,
        )
        return 2

    parent = Path(args.out).expanduser().resolve()
    skill_dir = parent / args.name

    if skill_dir.exists() and any(skill_dir.iterdir()) and not args.force:
        print(
            f"Error: {skill_dir} already exists and is not empty. "
            "Use --force to write into it anyway.",
            file=sys.stderr,
        )
        return 1

    (skill_dir / "references").mkdir(parents=True, exist_ok=True)
    (skill_dir / "scripts").mkdir(exist_ok=True)
    (skill_dir / "assets").mkdir(exist_ok=True)

    skill_md = skill_dir / "SKILL.md"
    template = (
        TEMPLATE_PATH.read_text(encoding="utf-8")
        if TEMPLATE_PATH.is_file()
        else SKILL_MD_TEMPLATE
    )
    skill_md.write_text(
        template.format(name=args.name, title=titleize(args.name)),
        encoding="utf-8",
    )

    print(f"Created skill skeleton at {skill_dir}")
    print("Next steps:")
    print(f"  1. Fill in {skill_md} (description first — it drives triggering)")
    print(f"  2. Validate:  python3 scripts/validate.py {skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
