# Innovation Map – Maintenance & Update Guide

## Repo Structure

```
InnovationMap_OE_BEL_27/
├── .github/
│   └── workflows/
│       └── update-data.yml   ← GitHub Actions workflow
├── data/
│   └── clusters/
│       ├── cluster-name/
│       │   ├── cluster.md    ← cluster metadata (name, color)
│       │   └── project.md    ← one file per project
│       └── ...
├── scripts/
│   ├── build.py              ← generates data.js from the .md files
│   ├── fix_quellen.py        ← normalises quellen separators to semicolons
│   └── run.bat               ← runs both scripts locally (Windows)
└── index.html                ← the site
```

---

## How the Pipeline Works

```
.md files in data/clusters/
        ↓
  fix_quellen.py        (fixes commas → semicolons in quellen fields)
        ↓
    build.py            (reads all .md files, outputs data/data.js)
        ↓
   index.html           (reads data.js and renders the map)
```

When you push changes to anything inside `data/`, GitHub Actions runs this pipeline automatically and deploys the updated site to GitHub Pages.

---

## Adding a New Project

1. Navigate to the correct cluster folder inside `data/clusters/`.
2. Create a new `.md` file (e.g. `my-project.md`).
3. Use this template:

```markdown
---
name: Project Name
subtitle: Short one-line description
org: Organisation Name
coordinator: Coordinator Name|https://coordinator-url.com
partners: Partner A|https://partner-a.com; Partner B|https://partner-b.com
trl: 7
srl: 6
marktreife: 5
skalierbarkeit: 8
nachhaltigkeit: 7
kooperationen: 9
zukunft: A short paragraph about the future outlook of this project.
quellen: Source Label A|https://source-a.com; Source Label B|https://source-b.com
image_url: https://images.unsplash.com/photo-XXXXXXXXX?w=800&q=80
---
Project description goes here. This is the main body text shown in the detail panel.

Separate paragraphs with a blank line.
```

**Field rules:**
- `partners` and `quellen` — separate entries with **semicolons** `;`
- `coordinator` and each partner/source — use `Name|URL` format
- `trl`, `srl`, and the other scores — integers from 1 to 9
- `marktreife` is optional; omit the line if not applicable

---

## Adding a New Cluster

1. Create a new folder inside `data/clusters/` (e.g. `data/clusters/my-cluster/`).
2. Inside it, create a `cluster.md` file:

```markdown
---
name: Cluster Display Name
color: #4A90D9
---
```

3. Add project `.md` files to the folder as described above.

---

## Updating an Existing Project

Just open the relevant `.md` file, edit the fields or body text, and save.

---

## Previewing Locally

Run the scripts manually before committing to check everything looks right:

```bat
cd scripts
run.bat
```

Then open `index.html` directly in your browser.

> **Note:** `data/data.js` is not stored in the repo — it only exists locally after you run the scripts, and is generated fresh by the workflow on each deploy.

---

## Pushing Changes to GitHub

From the repo root:

```bash
git add .
git commit -m "describe what you changed"
git push
```

The GitHub Actions workflow then:
1. Runs `fix_quellen.py` on all `.md` files
2. Runs `build.py` to generate `data.js`
3. Deploys the updated site to GitHub Pages

You can monitor the workflow under the **Actions** tab on GitHub. A green checkmark means the site is live with your changes.

---

## Checking the Live Site

Your site is at:
```
https://devnoob01.github.io/InnovationMap_OE_BEL_27/
```

Allow ~30–60 seconds after the workflow finishes for the deployment to propagate.

---

## Common Git Issues

### Push rejected (remote has new commits)
This happens when the remote has commits your local doesn't have yet.
```bash
git pull --rebase
git push
```

### Vim opens during a rebase
Type `:wq` and press Enter to save and continue.

### Accidentally committed to the wrong folder
Check where you are before committing:
```bash
git status
```
Always run `git add .` and `git commit` from the **repo root**, not from inside `scripts/`.

---

## Quick Reference

| Task | Command |
|---|---|
| Stage all changes | `git add .` |
| Commit | `git commit -m "message"` |
| Push | `git push` |
| Pull latest | `git pull --rebase` |
| Preview locally | run `scripts/run.bat` then open `index.html` |
| Check workflow status | GitHub → Actions tab |
