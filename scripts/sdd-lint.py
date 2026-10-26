#!/usr/bin/env python3
"""Validate requirement and task traceability in an opt-in SDD bundle."""

import argparse
import re
import sys
from pathlib import Path


REQUIREMENT_ID = re.compile(r"\bREQ-\d+\b")
EMPTY_ACCEPTANCE = {"", "-", "n/a", "none", "tbd", "todo"}


def markdown_blocks(content, prefix):
    heading = re.compile(rf"^###\s+({prefix}-\d+)\b[^\n]*\n", re.MULTILINE)
    matches = list(heading.finditer(content))
    blocks = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        blocks.append((match.group(1), content[match.end() : end]))
    return blocks


def acceptance_is_missing(block):
    match = re.search(r"^[ \t]*-[ \t]*Acceptance:[ \t]*(.*)$", block, re.MULTILINE | re.IGNORECASE)
    if not match:
        return True
    value = match.group(1).strip()
    return value.lower() in EMPTY_ACCEPTANCE or bool(re.fullmatch(r"\[.*\]", value))


def validate(spec_content, tasks_content):
    errors = []
    requirement_blocks = markdown_blocks(spec_content, "REQ")
    task_blocks = markdown_blocks(tasks_content, "TASK")
    requirement_ids = {requirement_id for requirement_id, _ in requirement_blocks}

    if not requirement_blocks:
        errors.append("No requirement definitions found (expected headings like '### REQ-001: ...').")

    seen_requirements = set()
    for requirement_id, block in requirement_blocks:
        if requirement_id in seen_requirements:
            errors.append(f"Duplicate requirement ID {requirement_id}.")
        seen_requirements.add(requirement_id)
        if acceptance_is_missing(block):
            errors.append(f"Requirement {requirement_id} has empty or missing acceptance criteria.")

    seen_tasks = set()
    for task_id, block in task_blocks:
        if task_id in seen_tasks:
            errors.append(f"Duplicate task ID {task_id}.")
        seen_tasks.add(task_id)
        requirement_line = re.search(r"^[ \t]*-[ \t]*Requirements:[ \t]*(.*)$", block, re.MULTILINE | re.IGNORECASE)
        linked_requirements = REQUIREMENT_ID.findall(requirement_line.group(1)) if requirement_line else []
        if not linked_requirements:
            errors.append(f"Task {task_id} has no requirement link.")
        for requirement_id in linked_requirements:
            if requirement_id not in requirement_ids:
                errors.append(f"Task {task_id} references undefined requirement {requirement_id}.")
        if acceptance_is_missing(block):
            errors.append(f"Task {task_id} has empty or missing acceptance criteria.")

    return errors, len(requirement_blocks), len(task_blocks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path, help="Markdown specification file")
    parser.add_argument("--tasks", required=True, type=Path, help="Markdown task list file")
    args = parser.parse_args()

    try:
        spec_content = args.spec.read_text(encoding="utf-8")
        tasks_content = args.tasks.read_text(encoding="utf-8")
    except OSError as error:
        parser.error(str(error))

    errors, requirement_count, task_count = validate(spec_content, tasks_content)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"SDD validation failed: {len(errors)} issue(s).")
        return 1

    print(f"SDD validation passed: {requirement_count} requirement(s), {task_count} task(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())