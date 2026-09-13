#!/usr/bin/env python3
"""Konservatives Publication Gate für dieses reine Dokumentations-Repository."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
MAX_TEXT_BYTES = 2 * 1024 * 1024
MAX_IMAGE_BYTES = 5 * 1024 * 1024
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
IGNORED_PARTS = {".git", ".pages-site", ".pages-src"}
FULL_ACTION_SHA = re.compile(r"^[0-9a-f]{40}$")
PROHIBITED_SUFFIXES = {
    ".7z", ".bin", ".ckpt", ".db", ".dmp", ".dump", ".env", ".fmb",
    ".gz", ".jks", ".keystore", ".onnx", ".p12", ".parquet", ".pem",
    ".pfx", ".pt", ".pth", ".rdf", ".safetensors", ".sqlite", ".tar", ".zip",
}
PROHIBITED_PARTS = {
    "adapters", "checkpoints", "client-data", "customer-data", "customer-projects",
    "datasets", "model-weights", "raw-data",
}
PATTERNS = {
    "privater Schlüssel": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub-Token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "AWS-Zugriffsschlüssel": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "Zugangsdaten-Zuweisung": re.compile(
        r"(?i)\b(?:password|passwd|pwd|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*['\"]?[^\s'\"<{]{8,}"
    ),
    "Vertraulichkeitsmarkierung": re.compile(
        r"\b(?:NVIDIA CONFIDENTIAL|CLIENT CONFIDENTIAL|INTERNAL USE ONLY|DO NOT DISTRIBUTE)\b"
    ),
    "aktive eingebettete Inhalte": re.compile(r"<\s*(?:script|iframe|object|embed)\b", re.IGNORECASE),
    "Git-LFS-Pointer": re.compile(r"^version https://git-lfs\.github\.com/spec/v1$", re.MULTILINE),
}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PRESENTATION_PAIRS = (
    ("README.md", "de/README.md"),
    ("docs/en/architecture.md", "docs/de/architecture.md"),
    ("docs/en/deployment.md", "docs/de/deployment.md"),
    ("docs/en/sizing.md", "docs/de/sizing.md"),
    ("docs/en/workflow.md", "docs/de/workflow.md"),
    ("docs/en/toolchain.md", "docs/de/toolchain.md"),
    ("docs/en/governance.md", "docs/de/governance.md"),
    ("SECURITY.md", "de/SECURITY.md"),
)


def pruefe_workflows(fehler: list[str]) -> None:
    """Verwirft privilegierte PR-Trigger und veränderliche Action-Referenzen."""
    workflow_dir = ROOT / ".github" / "workflows"
    for path in sorted(workflow_dir.glob("*.y*ml")):
        content = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        if re.search(r"(?m)^\s*(?:pull_request_target|workflow_run|issue_comment)\s*:", content):
            fehler.append(f"{rel}: privilegierter oder indirekter Trigger ist nicht erlaubt")
        is_pull_request = bool(re.search(r"(?m)^\s*pull_request\s*:", content))
        if is_pull_request and re.search(
            r"(?m)^\s*(?:contents|actions|checks|deployments|id-token|packages|pages|pull-requests)\s*:\s*write\s*$",
            content,
        ):
            fehler.append(f"{rel}: Pull-Request-Workflow verlangt Schreibrechte")
        if is_pull_request and "secrets." in content:
            fehler.append(f"{rel}: Pull-Request-Workflow referenziert Repository Secrets")
        for line in content.splitlines():
            match = re.match(r"\s*-?\s*uses:\s*([^\s#]+)", line)
            if not match:
                continue
            action = match.group(1)
            if action.startswith("./"):
                continue
            if "@" not in action or not FULL_ACTION_SHA.fullmatch(action.rsplit("@", 1)[1]):
                fehler.append(f"{rel}: Action ist nicht auf vollständige Commit-SHA fixiert: {action}")


def pruefe_sprachpfade(fehler: list[str]) -> None:
    """Erzwingt parallele monolinguale Präsentationspfade mit gleicher Struktur."""
    for english_name, german_name in PRESENTATION_PAIRS:
        english_path = ROOT / english_name
        german_path = ROOT / german_name
        if not english_path.is_file() or not german_path.is_file():
            fehler.append(f"fehlendes Sprachpaar: {english_name} <-> {german_name}")
            continue
        english = english_path.read_text(encoding="utf-8")
        german = german_path.read_text(encoding="utf-8")
        english_nav = next((line for line in english.splitlines()[:8] if line.startswith("[")), "")
        german_nav = next((line for line in german.splitlines()[:8] if line.startswith("[")), "")
        expected_nav_links = 7 if english_name == "SECURITY.md" else 8
        if (
            english_nav.count("](") != german_nav.count("](")
            or english_nav.count("](") != expected_nav_links
        ):
            fehler.append(f"Navigation weicht ab: {english_name} <-> {german_name}")
        if "Deutsch" not in english_nav or "English" not in german_nav:
            fehler.append(f"Sprachwechsel fehlt: {english_name} <-> {german_name}")
        if english.count("```mermaid") != german.count("```mermaid"):
            fehler.append(f"Mermaid-Anzahl weicht ab: {english_name} <-> {german_name}")
        english_sections = sum(line.startswith(("## ", "### ")) for line in english.splitlines())
        german_sections = sum(line.startswith(("## ", "### ")) for line in german.splitlines())
        if english_sections != german_sections:
            fehler.append(f"Abschnittsanzahl weicht ab: {english_name} <-> {german_name}")


def main() -> int:
    fehler: list[str] = []
    pruefe_sprachpfade(fehler)
    pruefe_workflows(fehler)
    for path in sorted(p for p in ROOT.rglob("*") if p.is_file()):
        if IGNORED_PARTS.intersection(path.parts):
            continue
        rel = path.relative_to(ROOT)
        if path.is_symlink():
            fehler.append(f"{rel}: symbolische Links sind nicht erlaubt")
            continue
        lowered_parts = {part.lower() for part in rel.parts}
        suffix = path.suffix.lower()
        size = path.stat().st_size

        if lowered_parts & PROHIBITED_PARTS:
            fehler.append(f"{rel}: gesperrter Pfad")
            continue
        if suffix in PROHIBITED_SUFFIXES:
            fehler.append(f"{rel}: gesperrter Dateityp")
            continue
        if suffix in IMAGE_SUFFIXES:
            if size > MAX_IMAGE_BYTES:
                fehler.append(f"{rel}: Bild ist größer als {MAX_IMAGE_BYTES} Bytes")
            continue
        if size > MAX_TEXT_BYTES:
            fehler.append(f"{rel}: Datei ist größer als {MAX_TEXT_BYTES} Bytes")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            fehler.append(f"{rel}: nicht freigegebene Binärdatei")
            continue
        if path.resolve() == SELF:
            continue
        for target in MARKDOWN_LINK.findall(content):
            clean_target = target.split("#", 1)[0]
            if not clean_target or "://" in clean_target or clean_target.startswith("mailto:"):
                continue
            if not (path.parent / clean_target).resolve().exists():
                fehler.append(f"{rel}: defekter relativer Link auf {target}")
        for label, pattern in PATTERNS.items():
            if pattern.search(content):
                fehler.append(f"{rel}: möglicher Fund – {label}")

    if fehler:
        print("Publication Gate fehlgeschlagen:")
        for fund in fehler:
            print(f"- {fund}")
        print("Auch nach Korrektur ist ein menschliches Provenienz- und Vertraulichkeitsreview Pflicht.")
        return 1

    print("Automatisches Publication Gate bestanden.")
    print("Es ersetzt kein menschliches Review von Provenienz, Lizenz, Vertraulichkeit und Datenschutz.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
