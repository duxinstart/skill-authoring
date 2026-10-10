#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# ///
"""Validate an Agent Skill directory.

Prefers the official ``skills-ref`` CLI; falls back to a built-in,
format-only check when it is not installed. Emits a JSON report on stdout
and human-readable diagnostics on stderr.

Usage:
    python3 scripts/validate.py <skill-dir>

Exit codes:
    0  valid
    1  invalid
    2  usage error
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

MAX_NAME_LEN = 64
MAX_DESC_LEN = 1024
MAX_COMPAT_LEN = 500
ALLOWED_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def find_skill_md(skill_dir: Path) -> Path | None:
    for candidate in ("SKILL.md", "skill.md"):
        path = skill_dir / candidate
        if path.is_file():
            return path
    return None


def split_frontmatter(text: str) -> tuple[str | None, str | None]:
    """Return (frontmatter, error)."""
    if not text.startswith("---"):
        return None, "SKILL.md must start with YAML frontmatter (---)"
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, "SKILL.md frontmatter not properly closed with ---"
    return parts[1], None


def read_top_level_fields(frontmatter: str) -> dict[str, str]:
    """Extract top-level ``key: value`` lines. Nested blocks are skipped."""
    fields: dict[str, str] = {}
    for raw in frontmatter.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[0] in " \t":  # indented -> belongs to a nested block
            continue
        if ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def builtin_check(skill_dir: Path) -> list[str]:
    """Format-only validation used when skills-ref is unavailable."""
    skill_md = find_skill_md(skill_dir)
    if skill_md is None:
        return [f"Missing required file: SKILL.md in {skill_dir}"]

    text = skill_md.read_text(encoding="utf-8")
    frontmatter, err = split_frontmatter(text)
    if err:
        return [err]
    assert frontmatter is not None

    fields = read_top_level_fields(frontmatter)
    errors: list[str] = []

    extra = set(fields) - ALLOWED_FIELDS
    if extra:
        errors.append(
            "Unexpected frontmatter fields: "
            f"{', '.join(sorted(extra))}. Allowed: {', '.join(sorted(ALLOWED_FIELDS))}"
        )

    name = fields.get("name", "")
    if not name:
        errors.append("Missing required field: name")
    else:
        norm = unicodedata.normalize("NFKC", name)
        if len(norm) > MAX_NAME_LEN:
            errors.append(f"name exceeds {MAX_NAME_LEN} characters ({len(norm)})")
        if norm != norm.lower():
            errors.append("name must be lowercase")
        if not NAME_RE.match(norm):
            errors.append(
                "name may only contain lowercase letters, digits, and single hyphens"
            )
        if norm != skill_dir.name:
            errors.append(
                f"name '{norm}' must match directory name '{skill_dir.name}'"
            )

    description = fields.get("description", "")
    if not description:
        errors.append("Missing required field: description")
    elif len(description) > MAX_DESC_LEN:
        errors.append(f"description exceeds {MAX_DESC_LEN} characters")

    compatibility = fields.get("compatibility", "")
    if compatibility and len(compatibility) > MAX_COMPAT_LEN:
        errors.append(f"compatibility exceeds {MAX_COMPAT_LEN} characters")

    return errors


def run_skills_ref(skill_dir: Path) -> subprocess.CompletedProcess[str] | None:
    exe = shutil.which("skills-ref")
    if not exe:
        return None
    return subprocess.run(
        [exe, "validate", str(skill_dir)],
        capture_output=True,
        text=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an Agent Skill directory.")
    parser.add_argument("skill_dir", type=Path, help="Path to the skill directory")
    args = parser.parse_args()

    skill_dir = args.skill_dir.expanduser().resolve()
    if not skill_dir.is_dir():
        print(
            json.dumps(
                {"valid": False, "engine": "none", "errors": [f"Not a directory: {skill_dir}"]},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    proc = run_skills_ref(skill_dir)
    if proc is not None:
        valid = proc.returncode == 0
        errors: list[str] = []
        if not valid:
            errors = [
                line.strip().lstrip("-").strip()
                for line in proc.stderr.splitlines()
                if line.strip().startswith("-")
            ] or [proc.stderr.strip() or "skills-ref reported an error"]
        report = {"valid": valid, "engine": "skills-ref", "errors": errors}
    else:
        print(
            "skills-ref not found; falling back to built-in format-only check.",
            file=sys.stderr,
        )
        errors = builtin_check(skill_dir)
        report = {"valid": not errors, "engine": "builtin", "errors": errors}

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
