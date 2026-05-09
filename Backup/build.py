import os, json, re

PROJECTS_DIR = "clusters"
OUTPUT_FILE  = "data.js"

def parse_frontmatter(content):
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}, ""
    fm = {}
    for line in match.group(1).splitlines():
        if ':' in line:
            key, _, val = line.partition(':')
            key, val = key.strip(), val.strip()
            try:
                val = int(val)
            except ValueError:
                if len(val) >= 2 and val[0] in ('"', "'") and val[-1] == val[0]:
                    val = val[1:-1]
            fm[key] = val
    body = re.sub(r'^---\s*\n.*?\n---\s*\n?', '', content, flags=re.DOTALL).strip()
    return fm, body

def parse_linked(raw):
    """Parse 'Name|URL' or plain 'Name' into {'name': ..., 'url': ...}"""
    raw = str(raw).strip()
    if '|' in raw:
        name, _, url = raw.partition('|')
        return {'name': name.strip(), 'url': url.strip()}
    return {'name': raw, 'url': ''}

def parse_linked_list(raw):
    """Parse comma-separated 'Name|URL' entries"""
    if not raw:
        return []
    return [parse_linked(p) for p in str(raw).split(',') if p.strip()]

def parse_quellen(raw):
    """Parse semicolon-separated 'label|url' pairs"""
    quellen = []
    if not raw:
        return quellen
    for entry in str(raw).split(';'):
        entry = entry.strip()
        if '|' in entry:
            label, _, url = entry.partition('|')
            quellen.append({'label': label.strip(), 'url': url.strip()})
        elif entry:
            quellen.append({'label': entry, 'url': ''})
    return quellen

clusters_out = []

for folder in sorted(os.listdir(PROJECTS_DIR)):
    folder_path = os.path.join(PROJECTS_DIR, folder)
    if not os.path.isdir(folder_path):
        continue
    cluster_file = os.path.join(folder_path, "cluster.md")
    if not os.path.exists(cluster_file):
        continue
    with open(cluster_file, encoding='utf-8') as f:
        cfm, _ = parse_frontmatter(f.read())
    cluster_name  = cfm.get('name')
    cluster_color = cfm.get('color')
    if not cluster_name or not cluster_color:
        print(f"  Skipping {folder}: cluster.md missing 'name' or 'color'")
        continue

    projects = []
    for fname in sorted(os.listdir(folder_path)):
        if not fname.endswith('.md') or fname == 'cluster.md':
            continue
        with open(os.path.join(folder_path, fname), encoding='utf-8') as f:
            fm, body = parse_frontmatter(f.read())
        if not fm.get('name'):
            continue

        coordinator_raw = fm.get('coordinator', fm.get('org', ''))
        coordinator = parse_linked(coordinator_raw)

        projects.append({
            'name':         fm.get('name', ''),
            'org':          fm.get('org', ''),
            'subtitle':     fm.get('subtitle', ''),
            'beschreibung': body or fm.get('beschreibung', ''),
            'zukunft':      fm.get('zukunft', ''),
            'coordinator':  coordinator,
            'partners':     parse_linked_list(fm.get('partners', '')),
            'quellen':      parse_quellen(fm.get('quellen', '')),
            'image_url':    fm.get('image_url', ''),
            'trl':          fm.get('trl', 1),
            'srl':          fm.get('srl', 1),
            'axes': [
                fm.get('trl', 1),
                fm.get('srl', 1),
                fm.get('marktreife', 1),
                fm.get('skalierbarkeit', 1),
                fm.get('nachhaltigkeit', 1),
                fm.get('kooperationen', 1),
            ]
        })

    clusters_out.append({'name': cluster_name, 'color': cluster_color, 'projects': projects})

js = "window.INNOVATION_DATA = " + json.dumps(clusters_out, ensure_ascii=False, indent=2) + ";"
os.makedirs("visualizer", exist_ok=True)
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(js)

total = sum(len(c['projects']) for c in clusters_out)
print(f"Done — {total} Projekte in {len(clusters_out)} Clustern → {OUTPUT_FILE}")
