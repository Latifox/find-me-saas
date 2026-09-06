#!/usr/bin/env python3
"""Validation harness for the idea-validation skill system.

Checks two things:

1. The runtime corpus under ``memory/`` (idea directories and market insight
   files) against the output contracts in ``tests/schemas.json``, including a
   recomputation of every ``scores.json`` and a shape check of every
   ``decision_memo.md``.
2. The specs themselves (``--check-specs``): every JSON block in
   ``skills/*/SKILL.md`` parses, every file a workflow reads is produced by a
   skill, every skill has a stub in all three platform adapters, and the
   structural requirements from task 1 are present.

Standard library only. Report lines go to stdout via ``print`` on purpose:
they are the product of this tool. Diagnostics go through ``logging``.

Exit codes: 0 = no errors (warnings allowed); 1 = at least one error;
``--baseline`` always exits 0 and is meant for legacy corpora.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

LOG = logging.getLogger("validate_memory")

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = Path(__file__).resolve().parent / "schemas.json"

DIMENSIONS = (
    "demand",
    "competition",
    "monetization",
    "distribution",
    "retention",
    "founder_market_fit",
)
DEFAULT_WEIGHTS = {
    "demand": 0.20,
    "competition": 0.10,
    "monetization": 0.20,
    "distribution": 0.20,
    "retention": 0.15,
    "founder_market_fit": 0.15,
}
VERDICT_BANDS = ((75, "pursue"), (55, "test"), (35, "pivot"), (0, "drop"))
RANK_BANDS = ((65, "strong-candidate"), (50, "candidate"), (0, "weak-candidate"))
FAST_DIMENSIONS = ("demand", "competition", "distribution", "founder_market_fit")
IDEA_STATUSES = {"candidate", "in-validation", "scored", "active", "paused", "dropped"}
BUSINESS_MODELS = {"b2c", "prosumer", "b2b-smb", "b2b2c"}
INSIGHT_PLATFORMS = {"tiktok", "reddit", "apps", "web-search", "x-twitter", "b2b-communities", "multi"}
MEMO_HEADINGS = (
    "## Verdict",
    "## Why This Score",
    "## Top 3 Strengths",
    "## Top 3 Risks",
    "## Riskiest Assumption",
    "## Pre-mortem",
    "## Devil's Advocate",
    "## What To Do Now",
    "## If That Doesn't Work",
    "## Sources",
)
MEMO_WORDS_MIN, MEMO_WORDS_WARN, MEMO_WORDS_MAX = 700, 1000, 1200
# Candidate quick-scores cap competition because unresearched estimates run high:
# five full validations landed at 38, 45, 65, 32 and 22. See skills/idea-scoring/SKILL.md.
CANDIDATE_COMPETITION_CAP = 45
STUB_SKILLS = (
    "desire-evaluator",
    "retention-predictor",
    "weakness-detection",
    "user-segmentation-profiler",
)
LANE_SKILLS = (
    "distribution-analysis",
    "pricing-and-wtp",
    "cac-modeler",
    "tam-sam-som-builder",
    "competitor-mapper",
    "retention-predictor",
    "pivot-engine",
    "idea-scoring",
)
IMPROVISATION_PHRASES = ("assumes b2c", "replaced with an equivalent")


class Report:
    """Collects findings and prints them grouped by severity."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checked = 0

    def error(self, where: str, msg: str) -> None:
        """Record a contract violation."""
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        """Record a non-fatal finding."""
        self.warnings.append(f"{where}: {msg}")

    def emit(self) -> None:
        """Print the findings and a one-line summary."""
        for line in self.errors:
            print(f"ERROR  {line}")
        for line in self.warnings:
            print(f"WARN   {line}")
        print(
            f"SUMMARY checked={self.checked} errors={len(self.errors)} "
            f"warnings={len(self.warnings)}"
        )


# --------------------------------------------------------------------------
# Small parsers
# --------------------------------------------------------------------------


def read_text(path: Path) -> str:
    """Read a UTF-8 file, tolerating a BOM."""
    return path.read_text(encoding="utf-8-sig")


def parse_frontmatter(text: str) -> dict[str, Any]:
    """Parse the YAML-ish frontmatter block the skills write.

    Supports ``key: scalar``, ``key: [a, b]``, ``key: "quoted"`` and block
    lists (``key:`` followed by ``  - item`` lines). Anything more exotic is
    kept as the raw string. Returns an empty dict when no frontmatter exists.
    """
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not match:
        return {}
    data: dict[str, Any] = {}
    current_list: str | None = None
    for raw in match.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.lstrip().startswith("- ") and current_list is not None:
            data[current_list].append(_scalar(raw.lstrip()[2:]))
            continue
        key_match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", raw)
        if not key_match:
            continue
        key, value = key_match.group(1), key_match.group(2)
        value = re.sub(r"\s+#.*$", "", value).strip()
        if value == "":
            data[key] = []
            current_list = key
        elif value.startswith("["):
            inner = value.strip("[]").strip()
            data[key] = [_scalar(v) for v in inner.split(",")] if inner else []
            current_list = None
        else:
            data[key] = _scalar(value)
            current_list = None
    return data


def _scalar(value: str) -> Any:
    """Strip quotes and coerce simple booleans/numbers."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    if value in ("true", "false"):
        return value == "true"
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value


def load_json(path: Path, report: Report) -> Any:
    """Load a JSON file, recording a parse failure instead of raising."""
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        report.error(rel(path), f"invalid JSON ({exc.msg} at line {exc.lineno})")
        return None


def rel(path: Path) -> str:
    """Repo-relative path with forward slashes for stable report output."""
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


# --------------------------------------------------------------------------
# Schema evaluation (six directives, see tests/README.md)
# --------------------------------------------------------------------------


def check_schema(doc: Any, schema: dict[str, Any], where: str, report: Report) -> None:
    """Apply the contract directives from schemas.json to one document."""
    known = {"required", "enums", "nullable", "conditional", "nested_required", "one_of", "_comment"}
    for key in schema:
        if key not in known:
            report.warn(where, f"schema directive '{key}' is not implemented and was ignored")
    if not isinstance(doc, dict):
        report.error(where, "top level is not a JSON object")
        return
    nullable = set(schema.get("nullable", []))
    _require(doc, schema.get("required", []), nullable, where, report)
    for field, allowed in schema.get("enums", {}).items():
        value = doc.get(field)
        if value is None:
            continue
        if isinstance(value, str) and value not in allowed:
            report.error(where, f"'{field}' = {value!r} not in {allowed}")
    for rule in schema.get("conditional", []):
        if all(doc.get(k) == v for k, v in rule.get("when", {}).items()):
            _require(doc, rule.get("required", []), nullable, where, report)
            for field in rule.get("absent", []):
                if field in doc:
                    report.error(where, f"'{field}' must be absent when {rule['when']}")
    for path_expr, keys in schema.get("nested_required", {}).items():
        for item, label in _walk(doc, path_expr):
            if isinstance(item, dict):
                missing = [k for k in keys if k not in item]
                if missing:
                    report.error(where, f"{label} missing {missing}")
            else:
                report.error(where, f"{label} is not an object")
    groups = schema.get("one_of", [])
    if groups and not any(all(k in doc for k in group) for group in groups):
        report.error(where, f"none of the key groups {groups} is fully present")


def _require(doc: dict, keys: list[str], nullable: set[str], where: str, report: Report) -> None:
    for key in keys:
        if key not in doc:
            report.error(where, f"missing required key '{key}'")
        elif doc[key] is None and key not in nullable:
            report.error(where, f"'{key}' is null but not nullable")


def _walk(doc: Any, path_expr: str) -> list[tuple[Any, str]]:
    """Resolve ``a.b[].c`` style paths into (value, label) pairs."""
    results: list[tuple[Any, str]] = [(doc, "")]
    for part in path_expr.split("."):
        is_list = part.endswith("[]")
        name = part[:-2] if is_list else part
        next_results: list[tuple[Any, str]] = []
        for value, label in results:
            if not isinstance(value, dict) or name not in value:
                continue
            child = value[name]
            child_label = f"{label}.{name}" if label else name
            if is_list:
                if isinstance(child, list):
                    next_results.extend((c, f"{child_label}[{i}]") for i, c in enumerate(child))
            else:
                next_results.append((child, child_label))
        results = next_results
    return results


# --------------------------------------------------------------------------
# Idea directory checks
# --------------------------------------------------------------------------


def check_idea_dir(idea_dir: Path, schemas: dict[str, Any], report: Report) -> None:
    """Run every corpus check that applies to one idea directory."""
    slug = idea_dir.name
    where = rel(idea_dir)
    idea_md = idea_dir / "idea.md"
    front: dict[str, Any] = {}
    if idea_md.exists():
        front = parse_frontmatter(read_text(idea_md))
        if front.get("idea_slug") != slug:
            report.error(rel(idea_md), f"idea_slug {front.get('idea_slug')!r} != directory name {slug!r}")
        if front.get("status") not in IDEA_STATUSES:
            report.error(rel(idea_md), f"status {front.get('status')!r} not in {sorted(IDEA_STATUSES)}")
        if "business_model" not in front:
            report.error(rel(idea_md), "missing business_model (legacy ideas predate this field)")
        elif front["business_model"] not in BUSINESS_MODELS:
            report.error(rel(idea_md), f"business_model {front['business_model']!r} not in {sorted(BUSINESS_MODELS)}")
        check_lineage(front, idea_dir, rel(idea_md), report)
    else:
        report.error(where, "idea.md missing")

    for json_path in sorted(idea_dir.glob("*.json")):
        report.checked += 1
        doc = load_json(json_path, report)
        if doc is None:
            continue
        schema = schemas.get(json_path.name)
        if schema is None:
            report.warn(rel(json_path), "no schema for this file name")
            continue
        check_schema(doc, schema, rel(json_path), report)
        if json_path.name == "scores.json" or json_path.name == "pivot_scores.json":
            check_scores(doc, idea_dir, rel(json_path), report)
        if json_path.name == "pivot_options.json":
            check_pivot_options(doc, rel(json_path), report)
        for name in ("sources",):
            if name in doc and isinstance(doc[name], list):
                for i, src in enumerate(doc[name]):
                    url = src.get("url", "") if isinstance(src, dict) else ""
                    if not str(url).startswith("http"):
                        report.error(rel(json_path), f"sources[{i}].url is not an http(s) URL")

    memo = idea_dir / "decision_memo.md"
    if memo.exists():
        report.checked += 1
        check_memo(memo, report)
        if front and front.get("status") in ("candidate", "in-validation"):
            report.error(rel(idea_md), f"decision_memo.md exists but status is {front.get('status')!r}; expected scored/active/paused/dropped")

    for text_path in list(idea_dir.glob("*.json")) + list(idea_dir.glob("*.md")):
        lowered = read_text(text_path).lower()
        for phrase in IMPROVISATION_PHRASES:
            if phrase in lowered:
                report.warn(rel(text_path), f"improvisation phrase found: {phrase!r} (spec lane did not fit)")


def check_scores(doc: dict[str, Any], idea_dir: Path, where: str, report: Report) -> None:
    """Recompute the multiplicative-floor score and verify stage semantics."""
    dims = doc.get("dimension_scores", {})
    weights = doc.get("weights_applied", DEFAULT_WEIGHTS)
    if abs(sum(weights.values()) - 1.0) > 0.001:
        report.error(where, f"weights_applied sum to {sum(weights.values()):.3f}, expected 1.0")
    available = {k: v for k, v in dims.items() if isinstance(v, (int, float)) and k in weights}
    for key in DIMENSIONS:
        if key not in dims:
            report.error(where, f"dimension_scores missing '{key}' (use null when unscored)")
    base = sum(available[k] * weights[k] for k in available)
    floor = 1.0
    for value in available.values():
        if value < 25:
            floor *= value / 25
    discount = len(available) / len(DIMENSIONS)
    final = round(base * floor * discount)

    _close(doc, "base_score", base, 0.6, where, report)
    _close(doc, "floor_penalty", floor, 0.01, where, report)
    _close(doc, "missing_discount", discount, 0.01, where, report)
    if doc.get("final_score") != final:
        report.error(where, f"final_score {doc.get('final_score')} != recomputed {final}")

    stage = doc.get("scoring_stage")
    if stage == "candidate-quick-score":
        if "verdict" in doc:
            report.error(where, "candidate-quick-score must not carry a verdict; use rank_label")
        expected = _band(base, RANK_BANDS)
        if doc.get("rank_label") != expected:
            report.error(where, f"rank_label {doc.get('rank_label')!r} != expected {expected!r} for base {base:.1f}")
        if not (idea_dir / "competitors.json").exists():
            comp = dims.get("competition")
            if isinstance(comp, (int, float)) and comp > CANDIDATE_COMPETITION_CAP:
                report.error(where, f"competition {comp} exceeds the {CANDIDATE_COMPETITION_CAP} prior cap without competitors.json")
            if doc.get("competition_prior_capped") is not True:
                report.error(where, "competition_prior_capped must be true when competitors.json is absent")
    else:
        expected = _band(doc.get("final_score", 0), VERDICT_BANDS)
        if doc.get("verdict") != expected:
            report.error(where, f"verdict {doc.get('verdict')!r} != table value {expected!r} for {doc.get('final_score')}")
        if len(available) < 3 or "demand" not in available or "distribution" not in available:
            report.error(where, "minimum viable input not met (3 dimensions incl. demand and distribution)")
        if stage == "fast-validation" and len(available) > len(FAST_DIMENSIONS):
            extra = sorted(set(available) - set(FAST_DIMENSIONS))
            report.error(where, f"fast-validation scores {len(available)} dimensions; at most {len(FAST_DIMENSIONS)} ({', '.join(FAST_DIMENSIONS)}), unexpected: {extra}")
    # Skills may downgrade confidence but never upgrade it past what the data supports.
    confidence = "high" if len(available) >= 6 else "medium" if len(available) >= 4 else "low"
    order = ["low", "medium", "high"]
    claimed = str(doc.get("score_confidence", "low"))
    if claimed in order and order.index(claimed) > order.index(confidence):
        report.error(where, f"score_confidence {claimed!r} is higher than {confidence!r} allowed by {len(available)} dimensions")


def _close(doc: dict, key: str, expected: float, tol: float, where: str, report: Report) -> None:
    value = doc.get(key)
    if not isinstance(value, (int, float)):
        report.error(where, f"'{key}' missing or not numeric")
    elif abs(value - expected) > tol:
        report.error(where, f"{key} {value} != recomputed {expected:.3f}")


def _band(score: float, bands: tuple[tuple[int, str], ...]) -> str:
    for threshold, label in bands:
        if score >= threshold:
            return label
    return bands[-1][1]


def check_pivot_options(doc: dict[str, Any], where: str, report: Report) -> None:
    """Check micro-pivot invariants and slug-decision consistency."""
    options = doc.get("pivot_options") or []
    if doc.get("pivot_scope") == "micro":
        if len(options) != 1:
            report.error(where, f"micro pivot must contain exactly one option, found {len(options)}")
        for i, option in enumerate(options):
            if isinstance(option, dict) and option.get("variables_changed") != 1:
                report.error(where, f"pivot_options[{i}].variables_changed must be 1 in a micro pivot")
    if doc.get("slug_decision") == "new-slug" and not doc.get("new_slug"):
        report.error(where, "slug_decision is 'new-slug' but new_slug is empty")


def check_lineage(front: dict[str, Any], idea_dir: Path, where: str, report: Report) -> None:
    """Check pivot_of / superseded_by pointers against the sibling directories."""
    ideas_root = idea_dir.parent
    superseded = front.get("superseded_by")
    if superseded:
        if front.get("status") not in ("paused", "dropped"):
            report.error(where, f"superseded_by is set but status is {front.get('status')!r}; expected paused or dropped")
        if not (ideas_root / str(superseded)).is_dir():
            report.error(where, f"superseded_by target directory {str(superseded)!r} not found")
    pivot_of = front.get("pivot_of")
    if pivot_of and not (ideas_root / str(pivot_of)).is_dir():
        report.error(where, f"pivot_of source directory {str(pivot_of)!r} not found")


def check_memo(memo: Path, report: Report) -> None:
    """Check decision memo frontmatter, headings, length, and URL sources."""
    where = rel(memo)
    text = read_text(memo)
    front = parse_frontmatter(text)
    for key in ("idea_slug", "verdict", "final_score", "score_confidence"):
        if key not in front:
            report.error(where, f"frontmatter missing '{key}'")
    for heading in MEMO_HEADINGS:
        if heading not in text:
            report.error(where, f"missing section '{heading}'")
    body = re.sub(r"^---.*?---", "", text, count=1, flags=re.S)
    full_words = len(re.findall(r"\b\w+\b", body))
    # The band applies to prose only; a citation list should not compete with analysis for space.
    prose = re.split(r"\n## Sources", body, maxsplit=1)[0]
    words = len(re.findall(r"\b\w+\b", prose))
    if full_words > MEMO_WORDS_MAX:
        report.error(where, f"{full_words} words in the full body, above the {MEMO_WORDS_MAX} hard cap")
    elif words < MEMO_WORDS_MIN:
        report.warn(where, f"{words} words of prose, below the {MEMO_WORDS_MIN} minimum")
    elif words > MEMO_WORDS_WARN:
        report.warn(where, f"{words} words of prose, above the {MEMO_WORDS_WARN} target")
    urls = re.findall(r"https?://\S+", text)
    if len(urls) < 3:
        report.error(where, f"only {len(urls)} URL(s) cited; at least 3 required under ## Sources")


# --------------------------------------------------------------------------
# Market insights checks
# --------------------------------------------------------------------------


def check_insights(insights_dir: Path, report: Report) -> None:
    """Validate frontmatter of every market insight file."""
    required = (
        "niche", "platform", "analyzed_at", "status", "stale_after",
        "trend_velocity", "overall_verdict", "key_insight", "top_signals", "monetization_evidence",
    )
    for path in sorted(insights_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        report.checked += 1
        where = rel(path)
        front = parse_frontmatter(read_text(path))
        for key in required:
            if key not in front:
                report.error(where, f"frontmatter missing '{key}'")
        platform = str(front.get("platform", ""))
        if platform and platform not in INSIGHT_PLATFORMS:
            report.error(where, f"platform {platform!r} not in {sorted(INSIGHT_PLATFORMS)}")
        analyzed = _parse_date(front.get("analyzed_at"))
        stale = _parse_date(front.get("stale_after"))
        if analyzed and stale:
            expected = _add_months(analyzed, 6)
            if abs((stale - expected).days) > 3:
                report.error(where, f"stale_after {stale} != analyzed_at + 6 months ({expected})")
            if date.today() > stale and front.get("status") != "stale":
                report.warn(where, f"past stale_after {stale} but status is {front.get('status')!r}")
        elif "stale_after" in front:
            report.error(where, "analyzed_at / stale_after are not YYYY-MM-DD dates")
        if not re.search(r"https?://", read_text(path)):
            report.error(where, "no URLs cited; a ## Sources section with links is required")


def _parse_date(value: Any) -> date | None:
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None


def _add_months(start: date, months: int) -> date:
    """Add calendar months, clamping the day to the target month's length."""
    month_index = start.month - 1 + months
    year = start.year + month_index // 12
    month = month_index % 12 + 1
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    days_in_month = (31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    return date(year, month, min(start.day, days_in_month[month - 1]))


# --------------------------------------------------------------------------
# Spec checks
# --------------------------------------------------------------------------


def check_specs(report: Report) -> None:
    """Validate the skill and workflow specs rather than a corpus."""
    skills_dir = ROOT / "skills"
    workflows_dir = ROOT / "workflows"
    produced: set[str] = set()

    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        report.checked += 1
        where = rel(skill_md)
        text = read_text(skill_md)
        name = skill_md.parent.name
        stripped = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        blocks = re.findall(r"```json\s*\n(.*?)```", stripped, re.S)
        outputs_json = re.search(r"outputs:[^\n]*\.json", text) is not None
        if not blocks and outputs_json:
            report.warn(where, "no ```json block found although the skill outputs JSON")
        for i, block in enumerate(blocks):
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                report.error(where, f"json block {i + 1} does not parse ({exc.msg} at line {exc.lineno})")
        for line in text.splitlines():
            if "outputs:" in line or re.search(r"\bwrite(s)? to\b", line, re.I):
                produced.update(re.findall(r"memory/ideas/<slug>/([\w.-]+\.(?:json|md))", line))
                produced.update(re.findall(r"`((?:pivot_)?[\w-]+\.(?:json|md))`", line))
        for adapter in (
            ROOT / ".claude" / "skills" / name / "SKILL.md",
            ROOT / ".codex" / "skills" / name / "SKILL.md",
            ROOT / ".cursor" / "rules" / f"{name}.mdc",
        ):
            if not adapter.exists():
                report.error(where, f"adapter stub missing: {rel(adapter)}")
        if name in STUB_SKILLS and "<!-- TODO" in text:
            report.error(where, "stub skill still contains <!-- TODO placeholders")
        if name in LANE_SKILLS:
            if "business_model" not in text:
                report.error(where, "lane skill does not mention business_model")
            if not re.search(r"\bb2b\b", text, re.I):
                report.error(where, "lane skill has no B2B rubric row or heading")
        if name == "retention-predictor" and "d30_equivalent" not in text:
            report.error(where, "retention-predictor spec lacks d30_equivalent")
        if name == "idea-scoring":
            if "3 of 7" in text:
                report.error(where, "says '3 of 7 dimensions' but there are 6")
            if "fast-validation" not in text:
                report.error(where, "Scoring Stages does not define fast-validation")
        if name == "pivot-engine":
            for needle, label in (("## Micro-pivot Mode", "micro-pivot mode"), ("## Slug Rule", "slug rule"), ("pivot_scope", "pivot_scope field")):
                if needle not in text:
                    report.error(where, f"missing {label}")
        if name == "decision-memo" and "Superseded by" not in text:
            report.error(where, "missing the superseded-memo rule")
        if name == "user-background-interviewer":
            for needle, label in (
                ("## First-Run Onboarding", "first-run onboarding section"),
                ("risk_tolerance", "risk tolerance capture"),
                ("preferred_business_model", "target-buyer capture"),
            ):
                if needle not in text:
                    report.error(where, f"onboarding is missing the {label}")
        if "(task-2)" in text:
            report.error(where, "unresolved (task-2) TODO")

    for wf in sorted(workflows_dir.glob("*.md")):
        if wf.name == "README.md":
            continue
        report.checked += 1
        where = rel(wf)
        text = read_text(wf)
        for line in text.splitlines():
            if "reads" not in line:
                continue
            optional = bool(re.search(r"\((?:optional|opt|if present|if available)\)", line, re.I))
            for fname in re.findall(r"memory/ideas/<slug>/([\w.-]+\.(?:json|md))", line):
                if fname not in produced and not optional:
                    report.error(where, f"reads '{fname}' which no skill produces")
        if "pivot_options.md" in text:
            report.error(where, "references pivot_options.md (should be pivot_options.json)")
        if wf.name == "idea-validation.md":
            for needle, label in (
                ("tam-sam-som-builder", "tam-sam-som-builder step"),
                ("profile gap", "profile-gap gate"),
                ("concurrently", "note on independent steps"),
                ("business_model", "business_model at entry"),
                ("status: scored", "status update after memo"),
                ("### Fast path", "fast path chain"),
            ):
                if needle not in text:
                    report.error(where, f"missing {label}")
        if wf.name == "market-deep-dive.md":
            if "-deep-dive-" in text:
                report.error(where, "exit output uses a '-deep-dive-' filename outside the naming convention")
            if "### Quick scan" not in text:
                report.error(where, "missing quick scan section")
        if wf.name == "pivot-optimization.md":
            for needle, label in (("### Micro-pivot", "micro-pivot chain"), ("Slug Rule", "slug rule")):
                if needle not in text:
                    report.error(where, f"missing {label}")
        if "(task-2)" in text:
            report.error(where, "unresolved (task-2) TODO")

    for readme in (ROOT / "memory" / "README.md",):
        text = read_text(readme)
        if "signal-aggregator" in text:
            report.error(rel(readme), "references non-existent skill signal-aggregator")
        for phantom in ("user_extraction.json", "weighted_signals.json", "signals.json", "keywords.json", "complexity.json"):
            if phantom in text:
                report.error(rel(readme), f"lists phantom file {phantom}")

    for router in (ROOT / "CLAUDE.md", ROOT / "AGENTS.md"):
        router_text = read_text(router)
        if "gut check" not in router_text:
            report.error(rel(router), "intent router does not mention the fast path (gut check)")
        if "first-run onboarding" not in router_text.lower():
            report.error(rel(router), "intent router does not route first-run onboarding")

    settings = ROOT / ".claude" / "settings.json"
    doc = load_json(settings, report)
    if isinstance(doc, dict):
        allow = doc.get("permissions", {}).get("allow", [])
        for needed in ("WebSearch", "WebFetch", "Read(memory/**)", "Write(memory/**)"):
            if needed not in allow:
                report.error(rel(settings), f"permissions.allow lacks {needed}")

    prompt = ROOT / "skills" / "trend-analysis" / "prompts" / "b2b-communities.md"
    if not prompt.exists():
        report.error(rel(prompt), "B2B communities prompt missing")
    else:
        front = parse_frontmatter(read_text(prompt))
        if front.get("prompt_for") != "b2b-communities":
            report.error(rel(prompt), "frontmatter prompt_for must be 'b2b-communities'")
        sections = re.findall(r"^\d+\.\s+\*\*", read_text(prompt), re.M)
        if len(sections) < 8:
            report.error(rel(prompt), f"only {len(sections)} numbered sections; web-search.md has 8")


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Parse arguments, run the selected checks, return the exit code."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--baseline", action="store_true", help="report everything but always exit 0")
    parser.add_argument("--strict", action="store_true", help="alias for the default mode (exit 1 on errors)")
    parser.add_argument("--check-specs", action="store_true", help="validate skills/workflows instead of the corpus")
    parser.add_argument("--idea", metavar="SLUG", help="validate a single idea directory")
    parser.add_argument("--memory", metavar="DIR", default=str(ROOT / "memory"), help="memory root (default: repo memory/)")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING, format="%(levelname)s %(message)s")

    report = Report()
    if args.check_specs:
        check_specs(report)
    else:
        try:
            schemas = json.loads(read_text(SCHEMA_PATH))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERROR  {rel(SCHEMA_PATH)}: cannot load schemas ({exc})")
            return 1
        memory = Path(args.memory)
        ideas_dir = memory / "ideas"
        if args.idea:
            targets = [ideas_dir / args.idea]
            if not targets[0].is_dir():
                print(f"ERROR  idea directory not found: {rel(targets[0])}")
                return 1
        else:
            targets = sorted(p for p in ideas_dir.glob("*") if p.is_dir()) if ideas_dir.exists() else []
        LOG.debug("validating %d idea directories", len(targets))
        for idea_dir in targets:
            check_idea_dir(idea_dir, schemas, report)
        if not args.idea and (memory / "market_insights").exists():
            check_insights(memory / "market_insights", report)
        if not targets and not args.idea:
            print("INFO   0 ideas found (empty corpus is valid)")

    report.emit()
    if args.baseline:
        return 0
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
