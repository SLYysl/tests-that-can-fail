"""Check that every skill in skills/ is well formed and that relative links resolve."""
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parent.parent
errors = []

for skill in sorted((root / "skills").glob("*/SKILL.md")):
    text = skill.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        errors.append(f"{skill}: missing front matter")
        continue
    fields = dict(line.split(":", 1) for line in match.group(1).splitlines() if ":" in line)
    name = fields.get("name", "").strip()
    description = fields.get("description", "").strip()
    if name != skill.parent.name:
        errors.append(f"{skill}: name {name!r} does not match folder {skill.parent.name!r}")
    if not description:
        errors.append(f"{skill}: empty description")
    if len(description) > 1024:
        errors.append(f"{skill}: description is {len(description)} characters (limit 1024)")

for doc in sorted(root.rglob("*.md")):
    if ".git" in doc.parts:
        continue
    for target in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", doc.read_text(encoding="utf-8")):
        if re.match(r"[a-z]+://|mailto:", target):
            continue
        if not (doc.parent / target).exists():
            errors.append(f"{doc.relative_to(root)}: broken link {target}")

print("\n".join(errors) or "skills OK")
sys.exit(1 if errors else 0)
