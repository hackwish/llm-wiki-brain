#!/usr/bin/env python3
"""Export explicitly approved project notes as a single static portfolio page."""

import argparse
import html
import re
import sys
from pathlib import Path


def parse_scalar(value):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        items = value[1:-1].split(",")
        return [parse_scalar(item) for item in items if item.strip()]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    metadata = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#") or line[0].isspace():
            continue
        key, separator, value = line.partition(":")
        if separator:
            metadata[key.strip()] = parse_scalar(value)
    return metadata, text[end + 5 :]


def markdown_inline(text):
    escaped = html.escape(text, quote=True)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
    link_pattern = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
    return link_pattern.sub(r'<a href="\2" rel="noreferrer">\1</a>', escaped)


def render_markdown(text):
    rendered = []
    paragraph = []
    list_items = []
    code_lines = []
    in_code = False

    def flush_paragraph():
        if paragraph:
            rendered.append(f"<p>{markdown_inline(' '.join(paragraph))}</p>")
            paragraph.clear()

    def flush_list():
        if list_items:
            items = "".join(f"<li>{markdown_inline(item)}</li>" for item in list_items)
            rendered.append(f"<ul>{items}</ul>")
            list_items.clear()

    for line in text.splitlines():
        if line.strip().startswith("```"):
            flush_paragraph()
            flush_list()
            if in_code:
                rendered.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
                code_lines.clear()
            in_code = not in_code
            continue
        if in_code:
            code_lines.append(line)
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        list_item = re.match(r"^\s*[-*]\s+(.+)$", line)
        if heading:
            flush_paragraph()
            flush_list()
            level = len(heading.group(1)) + 1
            rendered.append(f"<h{level}>{markdown_inline(heading.group(2))}</h{level}>")
        elif list_item:
            flush_paragraph()
            list_items.append(list_item.group(1))
        elif line.strip():
            flush_list()
            paragraph.append(line.strip())
        else:
            flush_paragraph()
            flush_list()

    flush_paragraph()
    flush_list()
    if code_lines:
        rendered.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
    return "\n".join(rendered)


def load_projects(projects_dir):
    projects = []
    for path in sorted(projects_dir.glob("*.md")):
        if path.name in {"README.md", "PROJECT-TEMPLATE.md"}:
            continue
        metadata, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        publishable = (
            str(metadata.get("portfolio", "")).lower() == "true"
            and str(metadata.get("visibility", "")).lower() == "public"
            and str(metadata.get("status", "")).lower() == "published"
        )
        if not publishable:
            continue
        title = str(metadata.get("title", "")).strip()
        description = str(metadata.get("description", "")).strip()
        if not title or not description:
            raise ValueError(f"{path}: published projects require title and description")
        skills = metadata.get("skills", [])
        if not isinstance(skills, list):
            skills = [skills]
        projects.append(
            {
                "title": title,
                "description": description,
                "role": str(metadata.get("role", "")).strip(),
                "period": str(metadata.get("period", "")).strip(),
                "skills": [str(skill).strip() for skill in skills if str(skill).strip()],
                "featured": str(metadata.get("featured", "")).lower() == "true",
                "body": body.strip(),
            }
        )
    return sorted(projects, key=lambda project: not project["featured"])


def build_page(projects, title, description):
    cards = []
    for index, project in enumerate(projects, start=1):
        details = " · ".join(value for value in (project["role"], project["period"]) if value)
        skills = "".join(f"<li>{html.escape(skill)}</li>" for skill in project["skills"])
        cards.append(
            f"""<article class="project">
  <div class="project-heading"><span class="number">{index:02}</span><div>
    <h2>{html.escape(project['title'])}</h2>
    <p class="description">{html.escape(project['description'])}</p>
    <p class="meta">{html.escape(details)}</p>
  </div></div>
  <div class="project-body">{render_markdown(project['body'])}</div>
  {f'<ul class="skills">{skills}</ul>' if skills else ''}
</article>"""
        )
    content = "\n".join(cards) if cards else '<p class="empty">No projects are currently approved for publication.</p>'
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(description, quote=True)}">
  <title>{html.escape(title)}</title>
  <style>
    :root {{ color-scheme: light; --ink: #202822; --muted: #647067; --paper: #f5f6f1; --line: #d9ded6; --accent: #bd4b2d; --leaf: #315b45; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--paper); color: var(--ink); font: 16px/1.65 "Avenir Next", Avenir, "Segoe UI", sans-serif; }}
    header {{ padding: clamp(3rem, 9vw, 7rem) max(1.25rem, calc((100vw - 980px) / 2)); border-bottom: 1px solid var(--line); background: radial-gradient(circle at 90% 15%, #e3e9df 0, transparent 28rem); }}
    .eyebrow {{ color: var(--accent); font-size: .75rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }}
    h1 {{ max-width: 850px; margin: .5rem 0 1rem; font: 500 clamp(2.5rem, 7vw, 5rem)/1.02 "Iowan Old Style", "Palatino Linotype", Georgia, serif; }}
    header p {{ max-width: 640px; color: var(--muted); font-size: 1.1rem; }}
    main {{ max-width: 980px; margin: 0 auto; padding: 1rem 1.25rem 5rem; }}
    .project {{ padding: 3rem 0; border-bottom: 1px solid var(--line); }}
    .project-heading {{ display: grid; grid-template-columns: 3rem 1fr; gap: 1rem; }}
    .number {{ color: var(--accent); font: 1.25rem Georgia, serif; }}
    h2 {{ margin: 0; font: 500 2rem/1.15 "Iowan Old Style", "Palatino Linotype", Georgia, serif; }}
    .description {{ margin: .6rem 0 0; font-size: 1.1rem; }} .meta {{ margin: .25rem 0; color: var(--muted); font-size: .9rem; }}
    .project-body {{ margin: 1.5rem 0 0 4rem; max-width: 700px; }}
    h3 {{ margin: 1.7rem 0 .4rem; color: var(--leaf); font-size: 1rem; }}
    a {{ color: var(--leaf); }} code, pre {{ background: #e9ede6; border-radius: 3px; }} code {{ padding: .1rem .3rem; }} pre {{ overflow-x: auto; padding: 1rem; }}
    .skills {{ display: flex; flex-wrap: wrap; gap: .5rem; margin: 1.5rem 0 0 4rem; padding: 0; list-style: none; }}
    .skills li {{ border: 1px solid var(--line); padding: .2rem .65rem; color: var(--leaf); font-size: .82rem; }}
    .empty {{ padding: 3rem 0; color: var(--muted); }} footer {{ padding: 1.5rem; border-top: 1px solid var(--line); color: var(--muted); text-align: center; font-size: .8rem; }}
    @media (max-width: 600px) {{ .project-heading {{ grid-template-columns: 2rem 1fr; gap: .5rem; }} .project-body, .skills {{ margin-left: 2.5rem; }} h2 {{ font-size: 1.65rem; }} }}
  </style>
</head>
<body>
  <header><span class="eyebrow">Selected work</span><h1>{html.escape(title)}</h1><p>{html.escape(description)}</p></header>
  <main>{content}</main>
  <footer>Generated from explicitly published project notes.</footer>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="portfolio wiki root (default: current directory)")
    parser.add_argument("--projects", type=Path, help="project notes directory (default: ROOT/projects)")
    parser.add_argument("--output", type=Path, default=Path("public"), help="output directory (default: public)")
    parser.add_argument("--title", default="Selected Work", help="portfolio page title")
    parser.add_argument("--description", default="A selection of projects, experience, and learning.", help="portfolio introduction")
    args = parser.parse_args()

    root = args.root.resolve()
    projects_dir = args.projects if args.projects and args.projects.is_absolute() else root / (args.projects or Path("projects"))
    output_dir = args.output if args.output.is_absolute() else root / args.output
    if not projects_dir.is_dir():
        print(f"error: projects directory not found: {projects_dir}", file=sys.stderr)
        return 2
    try:
        projects = load_projects(projects_dir)
        page = build_page(projects, args.title, args.description)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "index.html"
    destination.write_text(page, encoding="utf-8")
    print(f"Portfolio generated: {destination} ({len(projects)} published project(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())