# Jixin Hou — Simple Research Website

This version intentionally has only four navigation items:

**Home · Research · Publications · CV**

## Easiest way to edit on Windows

1. Extract this folder.
2. Double-click `EDIT_WEBSITE.bat`.
3. The local editor opens.
4. Change text, research descriptions, links, publications, hero image, publication figures, or CV.
5. Click **Save & Build**.
6. Click **Preview** to open the updated site.

No third-party Python packages are required. It uses Python's built-in Tkinter GUI.

If `.bat` does not start because Python is not on PATH:
- Open PowerShell in this folder.
- Run: `python editor.py`

## Replace a publication thumbnail with your actual paper figure

Open the **Publications** tab → double-click the paper → **Choose figure…** → select PNG/JPG/SVG → Save.

The initial thumbnails are original schematic illustrations made for the website, rather than copied publisher figures.

## Add your CV

Open **CV & Links** → `Choose CV PDF…` → select your PDF → Save & Build.

## Files you usually do NOT need to edit manually

- `content.json` — all editable content
- `build_site.py` — generates the HTML
- `style.css` — visual design
- `editor.py` — local GUI
- `assets/` — images and CV
