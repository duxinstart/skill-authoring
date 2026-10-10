#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# ///
"""Check a skill's description for length, trigger phrasing, and coverage.

Emits a JSON report on stdout; human-readable suggestions go to stderr.

Usage:
    python3 scripts/lint_description.py <skill-dir>

Exit codes:
    0  no hard problems (warnings may still be present)
    1  hard problem found (e.g. missing or over-long description)
    2  usage error
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MAX_DESC_LEN = 1024
MIN_USEFUL_LEN = 40

TRIGGER_MARKERS = (
    "use when",
    "use this skill",
    "when the user",
    "when you",
    "使用",
    "当用户",
    "适用于",
    "触发",
)

WHAT_MARKERS = (
    "extract",
    "generate",
    "create",
    "analyze",
    "convert",
    "build",
    "validate",
    "创建",
    "生成",
    "分析",
    "提取",
    "校验",
    "转换",
    "构建",
)


def find_skill_md(skill_dir: Path) -> Path | None:
    for candidate in ("SKILL.md", "skill.md"):
        path = skill_dir / candidate
        if path.is_file():
            return path
    return None


def extract_description(frontmatter: str) -> str | None:
    """Pull the ``description`` value, handling `>`/`|` block scalars."""
    lines = frontmatter.splitlines()
    for index, raw in enumerate(lines):
        if not raw.startswith("description:"):
            continue
        value = raw[len("description:"):].strip()
        if value in (">", "|", ">-", "|-", ">+", "|+"):
            block: list[str] = []
            for following in lines[index + 1:]:
                if following.strip() == "":
                    block.append("")
                    continue
                if following[0] in " \t":
                    block.append(following.strip())
                else:
                    break
            return " ".join(part for part in block if part).strip()
        return value
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Lint a skill's description for triggering quality."
    )
    parser.add_argument("skill_dir", type=Path, help="Path to the skill directory")
    args = parser.parse_args()

    skill_dir = args.skill_dir.expanduser().resolve()
    skill_md = find_skill_md(skill_dir)
    if skill_md is None:
        print(f"Error: SKILL.md not found in {skill_dir}", file=sys.stderr)
        return 2

    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        print("Error: SKILL.md has no YAML frontmatter.", file=sys.stderr)
        return 2
    parts = text.split("---", 2)
    if len(parts) < 3:
        print("Error: frontmatter not closed with ---.", file=sys.stderr)
        return 2

    description = extract_description(parts[1])
    errors: list[str] = []
    warnings: list[str] = []

    if not description:
        errors.append("description is missing or empty")
    else:
        length = len(description)
        if length > MAX_DESC_LEN:
            errors.append(f"description exceeds {MAX_DESC_LEN} characters ({length})")
        if length < MIN_USEFUL_LEN:
            warnings.append(
                f"description is very short ({length} chars); "
                "it may not carry enough context to trigger reliably"
            )

        lowered = description.lower()
        if not any(marker in lowered for marker in TRIGGER_MARKERS):
            warnings.append(
                'no trigger phrasing found; add "Use when ..." / "当用户…时使用" '
                "so the agent knows when to act"
            )
        if not any(marker in lowered for marker in WHAT_MARKERS):
            warnings.append(
                "could not detect a clear action verb (extract/generate/analyze/…); "
                "make sure the description says what the skill does"
            )

    report = {
        "description_length": len(description) if description else 0,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
