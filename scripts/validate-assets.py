#!/usr/bin/env python3
"""
validate-assets.py — Quality and security validator for LLM Wiki Toolkit assets:
skills, agent instructions (AGENTS.md), prompts, templates, and scripts.
"""

import os
import sys
import re
import json
import argparse

# Secrets and sensitive data patterns
SECRET_PATTERNS = [
    (r'(?i)(api[_-]?key|secret[_-]?key|access[_-]?token|auth[_-]?token)\s*[:=]\s*["\']?[A-Za-z0-9_\-]{16,}["\']?', "Potential hardcoded API key or token"),
    (r'-----BEGIN (RSA|OPENSSH|PRIVATE) KEY-----', "Private key detected"),
    (r'ghp_[A-Za-z0-9]{36}', "GitHub Personal Access Token"),
    (r'sk-[A-Za-z0-9]{32,}', "OpenAI/Anthropic API Key pattern"),
]

# Prompt injection & dangerous instruction patterns for agent assets
INJECTION_PATTERNS = [
    (r'(?i)ignore (previous|all) instructions', "Potential prompt injection: ignore instructions"),
    (r'(?i)bypass (security|safety|rules)', "Potential security bypass instruction"),
    (r'rm\s+-rf\s+/', "Dangerous command: root directory removal"),
    (r'curl\s+.*\|\s*sh', "Dangerous command: piping web content to shell"),
    (r'wget\s+.*\|\s*sh', "Dangerous command: piping web content to shell"),
]

REQUIRED_SKILL_FIELDS = ["name", "description"]

def check_secrets_and_safety(content: str, filepath: str) -> list[str]:
    issues = []
    lines = content.splitlines()
    for line_idx, line in enumerate(lines, start=1):
        for pattern, desc in SECRET_PATTERNS:
            if re.search(pattern, line):
                issues.append(f"[{filepath}:{line_idx}] SECURITY: {desc}")
        for pattern, desc in INJECTION_PATTERNS:
            if re.search(pattern, line):
                issues.append(f"[{filepath}:{line_idx}] SAFETY: {desc}")
    return issues

def parse_yaml_frontmatter(content: str) -> dict:
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    yaml_text = parts[1]
    data = {}
    for line in yaml_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip("'\"")
            if val.startswith(">-") or val.startswith(">"):
                val = ""
            data[key] = val
    return data

def validate_skills(repo_root: str) -> tuple[list[str], list[str]]:
    warnings = []
    errors = []
    skills_dir = os.path.join(repo_root, ".agents", "skills")
    if not os.path.exists(skills_dir):
        errors.append(f"Skills directory missing: {skills_dir}")
        return warnings, errors

    for root, dirs, files in os.walk(skills_dir):
        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, repo_root)

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                errors.append(f"[{rel_path}] Could not read file: {e}")
                continue

            # Security & safety check
            sec_issues = check_secrets_and_safety(content, rel_path)
            errors.extend(sec_issues)

            if file == "SKILL.md":
                fm = parse_yaml_frontmatter(content)
                for field in REQUIRED_SKILL_FIELDS:
                    if field not in fm or not fm[field]:
                        # Check if present in content manually if parser missed multi-line
                        if f"{field}:" not in content:
                            errors.append(f"[{rel_path}] QUALITY: Missing required frontmatter field '{field}'")
                
                # Check section structure
                if "## " not in content:
                    warnings.append(f"[{rel_path}] QUALITY: SKILL.md has no markdown headings (##)")

            if file == "README.md":
                if len(content.strip()) < 20:
                    warnings.append(f"[{rel_path}] QUALITY: README.md seems too short or empty")

    return warnings, errors

def validate_prompts(repo_root: str) -> tuple[list[str], list[str]]:
    warnings = []
    errors = []
    prompts_dir = os.path.join(repo_root, "prompts")
    if not os.path.exists(prompts_dir):
        warnings.append("Prompts directory does not exist")
        return warnings, errors

    for root, dirs, files in os.walk(prompts_dir):
        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, repo_root)

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                errors.append(f"[{rel_path}] Could not read file: {e}")
                continue

            sec_issues = check_secrets_and_safety(content, rel_path)
            errors.extend(sec_issues)

            if file.endswith(".md"):
                if len(content.strip()) < 10:
                    warnings.append(f"[{rel_path}] QUALITY: Prompt file is nearly empty")

    return warnings, errors

def validate_templates_and_presets(repo_root: str) -> tuple[list[str], list[str]]:
    warnings = []
    errors = []
    presets_dir = os.path.join(repo_root, "templates", "presets")
    if os.path.exists(presets_dir):
        for file in os.listdir(presets_dir):
            if file.endswith(".json"):
                filepath = os.path.join(presets_dir, file)
                rel_path = os.path.relpath(filepath, repo_root)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    required_keys = ["preset", "title", "purpose"]
                    for k in required_keys:
                        if k not in data:
                            errors.append(f"[{rel_path}] QUALITY: Preset JSON missing key '{k}'")
                except json.JSONDecodeError as e:
                    errors.append(f"[{rel_path}] SYNTAX: Invalid JSON syntax: {e}")

    agents_template = os.path.join(repo_root, "templates", "schema", "AGENTS.md.template")
    if os.path.exists(agents_template):
        with open(agents_template, "r", encoding="utf-8") as f:
            content = f.read()
        sec_issues = check_secrets_and_safety(content, "templates/schema/AGENTS.md.template")
        errors.extend(sec_issues)
        placeholders = ["{{KIT_INTRO}}", "{{KIT_LAYERS}}", "{{KIT_STRUCTURE}}"]
        for p in placeholders:
            if p not in content:
                warnings.append(f"[templates/schema/AGENTS.md.template] QUALITY: Expected placeholder '{p}' missing")

    return warnings, errors

def validate_agents_md(repo_root: str) -> tuple[list[str], list[str]]:
    warnings = []
    errors = []
    agents_path = os.path.join(repo_root, "AGENTS.md")
    if os.path.exists(agents_path):
        with open(agents_path, "r", encoding="utf-8") as f:
            content = f.read()
        sec_issues = check_secrets_and_safety(content, "AGENTS.md")
        errors.extend(sec_issues)
        if "# AGENTS.md" not in content and "# " not in content:
            warnings.append("[AGENTS.md] QUALITY: Missing main title heading")
    else:
        errors.append("AGENTS.md is missing in repo root")

    return warnings, errors

def main():
    parser = argparse.ArgumentParser(description="Validate skills, agents, prompts, and templates.")
    parser.add_argument("--repo-root", default=".", help="Root directory of the repository")
    args = parser.parse_args()

    repo_root = os.path.abspath(args.repo_root)
    print(f"🔍 Validating LLM Wiki Toolkit assets in: {repo_root}\n")

    all_warnings = []
    all_errors = []

    # Run checks
    w, e = validate_skills(repo_root)
    all_warnings.extend(w)
    all_errors.extend(e)

    w, e = validate_prompts(repo_root)
    all_warnings.extend(w)
    all_errors.extend(e)

    w, e = validate_templates_and_presets(repo_root)
    all_warnings.extend(w)
    all_errors.extend(e)

    w, e = validate_agents_md(repo_root)
    all_warnings.extend(w)
    all_errors.extend(e)

    # Output results
    if all_warnings:
        print("⚠️ WARNINGS:")
        for w in all_warnings:
            print(f"  - {w}")
        print()

    if all_errors:
        print("❌ ERRORS / SECURITY & QUALITY ISSUES FOUND:")
        for e in all_errors:
            print(f"  - {e}")
        print(f"\nTotal: {len(all_errors)} error(s), {len(all_warnings)} warning(s).")
        sys.exit(1)

    print("✅ All quality and security validations passed successfully!")
    sys.exit(0)

if __name__ == "__main__":
    main()
