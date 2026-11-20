"""Builds the Ortus website into site/: the guide from docs/*.md and the API
reference from api/openapi.json (the core's and every app's operations, as
`ortus reference` prints them at the pinned program). Standard library only.
"""
import html, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")

STYLE = """
:root{--bg:#0b0d12;--surface:#13161c;--line:rgba(255,255,255,.1);--text:#edf0f5;--text2:#9ea6b5;--accent:#8c9eff}
@media (prefers-color-scheme: light){:root{--bg:#fff;--surface:#f4f5f8;--line:rgba(0,0,0,.12);--text:#14161b;--text2:#555c69;--accent:#3d52d5}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.6 system-ui,sans-serif}
header{border-bottom:1px solid var(--line);padding:12px 24px;display:flex;gap:20px;align-items:center;flex-wrap:wrap}
header a{color:var(--text2);text-decoration:none}header a.home{color:var(--text);font-weight:600}
main{max-width:860px;margin:0 auto;padding:32px 16px 64px}
a{color:var(--accent)}code{font:14px ui-monospace,monospace;background:var(--surface);padding:1px 4px;border-radius:4px}
pre{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px;overflow-x:auto}pre code{background:none;padding:0}
table{border-collapse:collapse;width:100%;font-size:15px;display:block;overflow-x:auto}td,th{border:1px solid var(--line);padding:6px 10px;text-align:start;vertical-align:top}
.op{border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin:10px 0}.m{font:600 13px ui-monospace,monospace;color:var(--accent);margin-inline-end:8px}
.access{color:var(--text2);font-size:13px}
"""

NAV = [("index.html", "Ortus"), ("install.html", "One machine"), ("kubernetes.html", "Kubernetes"), ("backups.html", "Backups"),
       ("upgrades.html", "Upgrades"), ("integrations.html", "Integrations"), ("phones.html", "Phones"), ("releases.html", "Releases"), ("api/index.html", "API")]


def page(title, body, depth=0):
    up = "../" * depth
    nav = "".join(f'<a href="{up}{href}"{" class=home" if i == 0 else ""}>{html.escape(name)}</a>' for i, (href, name) in enumerate(NAV))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · Ortus</title><style>{STYLE}</style></head><body><header>{nav}</header><main>{body}</main></body></html>
"""


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def markdown(src):
    out, lines, i = [], src.split("\n"), 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
        elif m := re.match(r"^(#{1,3}) (.*)", line):
            n = len(m.group(1))
            slug = re.sub(r"[^a-z0-9]+", "-", m.group(2).lower()).strip("-")
            out.append(f'<h{n} id="{slug}">{inline(m.group(2))}</h{n}>')
        elif line.startswith("| "):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(set(c) <= set("-: ") for c in cells):
                    rows.append(cells)
                i += 1
            i -= 1
            head, *body = rows
            out.append("<table><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr>" +
                       "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body) + "</table>")
        elif line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:])
                i += 1
            i -= 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
        elif line.strip():
            para = [line]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"^(#|```|\| |- )", lines[i + 1]):
                i += 1
                para.append(lines[i])
            out.append("<p>" + inline(" ".join(para)) + "</p>")
        i += 1
    return "\n".join(out)


def reference():
    spec = json.load(open(os.path.join(ROOT, "api", "openapi.json")))
    by_tag = {}
    for path, ops in sorted(spec["paths"].items()):
        for method, op in ops.items():
            by_tag.setdefault((op.get("tags") or ["other"])[0], []).append((method.upper(), path, op))
    pages = {}
    index = ["<h1>API reference</h1>",
             f"<p>{inline(spec.get('info', {}).get('description', ''))}</p>",
             "<p>Every call sends the session token as <code>Authorization: Bearer &lt;token&gt;</code> (browsers use the session cookie); "
             "every change also sends <code>X-Requested-With: ortus</code>. Errors are one JSON shape: "
             "<code>{\"error\": {\"code\", \"message\", \"request_id\"}}</code>.</p>",
             f"<p>{sum(len(v) for v in by_tag.values())} operations:</p><ul>"]
    for tag in sorted(by_tag):
        index.append(f'<li><a href="{tag}.html">{html.escape(tag)}</a> ({len(by_tag[tag])})</li>')
        body = [f"<h1>{html.escape(tag)}</h1>"]
        for method, path, op in by_tag[tag]:
            body.append(f'<div class="op" id="{html.escape(op.get("operationId", ""))}"><span class="m">{method}</span><code>{html.escape(path)}</code>'
                        f'<p>{inline(op.get("summary", ""))}</p></div>')
        pages[tag] = "\n".join(body)
    index.append("</ul><p>The machine-readable reference: <a href=\"openapi.json\">openapi.json</a>.</p>")
    return "\n".join(index), pages


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(os.path.join(OUT, "api"))
    for name in sorted(os.listdir(os.path.join(ROOT, "docs"))):
        if name.endswith(".md"):
            src = open(os.path.join(ROOT, "docs", name), encoding="utf-8").read()
            title = src.split("\n", 1)[0].lstrip("# ").strip()
            open(os.path.join(OUT, name[:-3] + ".html"), "w", encoding="utf-8").write(page(title, markdown(src)))
    index, pages = reference()
    open(os.path.join(OUT, "api", "index.html"), "w", encoding="utf-8").write(page("API reference", index, 1))
    for tag, body in pages.items():
        open(os.path.join(OUT, "api", f"{tag}.html"), "w", encoding="utf-8").write(page(tag, body, 1))
    shutil.copy(os.path.join(ROOT, "api", "openapi.json"), os.path.join(OUT, "api", "openapi.json"))
    print(f"site: {len(os.listdir(OUT)) - 1} pages and the API ({len(pages)} sections)")


if __name__ == "__main__":
    sys.exit(main())
