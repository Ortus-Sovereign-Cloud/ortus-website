"""Checks the built site: every link inside it leads to a page that exists,
and every `ortus <command>` the guide names is one the program has."""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
site = os.path.join(ROOT, "site")
bad = []
for folder, _, files in os.walk(site):
    for f in files:
        if not f.endswith(".html"):
            continue
        text = open(os.path.join(folder, f), encoding="utf-8").read()
        for href in re.findall(r'href="([^"#]+)', text):
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(folder, href))):
                bad.append(f"{os.path.relpath(os.path.join(folder, f), site)}: {href}")
commands = set(open(os.path.join(ROOT, "api", "commands.txt")).read().split())
for f in os.listdir(os.path.join(ROOT, "docs")):
    # `ortus <command>` as typed (not "helm install ortus …", "-u ortus …").
    for cmd in re.findall(r"(?<!install )(?<!upgrade )(?<!-u )(?<!user )\bortus ([a-z][a-z-]+)", open(os.path.join(ROOT, "docs", f), encoding="utf-8").read()):
        if cmd not in commands:
            bad.append(f"docs/{f}: `ortus {cmd}` is not a command of the program")
    for cmd in re.findall(r"\bortusctl ([a-z][a-z-]+)", open(os.path.join(ROOT, "docs", f), encoding="utf-8").read()):
        if cmd not in commands:
            bad.append(f"docs/{f}: `ortusctl {cmd}` is not a command of the program")
# Every ORTUS_* setting the guide names is one the program reads.
settings = set(open(os.path.join(ROOT, "api", "settings.txt")).read().split())
for f in os.listdir(os.path.join(ROOT, "docs")):
    for name in re.findall(r"\bORTUS_[A-Z0-9_]*[A-Z0-9]", open(os.path.join(ROOT, "docs", f), encoding="utf-8").read()):
        if name not in settings:
            bad.append(f"docs/{f}: {name} is not a setting of the program")
for b in bad:
    print("check:", b, file=sys.stderr)
sys.exit(1 if bad else 0)
