from pathlib import Path
import json, html
ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/"content.json").read_text(encoding="utf-8"))
def e(x): return html.escape(str(x))
nav_cv="cv.html"
research_html="".join(f"""<article class="research-card"><span>0{i+1}</span><h3>{e(r['title'])}</h3><p>{e(r['text'])}</p></article>""" for i,r in enumerate(data["research"]))
pubs=sorted(data["publications"], key=lambda p: p.get("year",""), reverse=True)
pub_html="".join(f"""<a class="pub" href="{e(p['url'])}" target="_blank" rel="noopener"><img src="{e(p.get('image','assets/pub_folding.svg'))}" alt=""><div class="pub-body"><div class="pub-meta">{e(p['year'])} · {e(p['journal'])}</div><h3>{e(p['title'])}</h3><p>{e(p['authors'])}</p><p class="summary">{e(p.get('summary',''))}</p></div></a>""" for p in pubs)
index=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(data['name'])} — Research</title><meta name="description" content="{e(data['intro'])}"><link rel="stylesheet" href="style.css"></head><body>
<header><nav class="wrap"><a class="brand" href="#home">{e(data['name'])}</a><div class="links"><a href="#home">Home</a><a href="#research">Research</a><a href="#publications">Publications</a><a href="{nav_cv}">CV</a></div><button class="menu">☰</button></nav></header>
<main><div id="home" class="hero wrap"><div><div class="eyebrow">{e(data['subtitle'])}</div><h1>{e(data['tagline'])}</h1><p class="intro">{e(data['intro'])}</p><div class="buttons"><a class="button primary" href="#research">Explore research</a><a class="button" href="#publications">Publications</a></div></div><div class="hero-figure"><img src="{e(data['hero_image'])}" alt="Abstract visualization of developmental brain research"><div class="hero-note">Imaging × mechanics × development</div></div></div>
<section id="research"><div class="wrap"><div class="section-top"><h2>Research</h2><p>Three connected directions centered on understanding how the developing brain acquires its form.</p></div><div class="research-grid">{research_html}</div></div></section>
<section id="publications"><div class="wrap"><div class="section-top"><h2>Selected publications</h2><p>First-author work is shown visually. The thumbnails are original website schematics and can be replaced with your actual paper figures in the local editor.</p></div><div class="pub-grid">{pub_html}</div><a class="scholar-link" href="{e(data['scholar'])}" target="_blank">View complete Google Scholar profile →</a></div></section>
<section class="contact"><div class="wrap contact-row"><h2>Research, collaboration, or conversation.</h2><div class="small-links"><a href="mailto:{e(data['email'])}">Email</a><a href="{e(data['scholar'])}" target="_blank">Scholar</a>{f'<a href="{e(data["github"])}" target="_blank">GitHub</a>' if data.get("github") else ''}</div></div></section></main>
<footer><div class="wrap">© 2026 {e(data['name'])}</div></footer><script src="main.js"></script></body></html>"""
(ROOT/"index.html").write_text(index,encoding="utf-8")
cv=data.get("cv_path","").strip()
if cv:
    body=f'<p><a class="button primary" href="{e(cv)}" target="_blank">Open / download CV</a></p><p class="intro">If the PDF does not open automatically, use the button above.</p>'
else:
    body='<div class="notice"><strong>CV not added yet.</strong><p>Open <code>editor.py</code>, choose your CV PDF under Settings, and click Save & Build. The CV link will then work automatically.</p></div>'
cvhtml=f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CV — {e(data['name'])}</title><link rel="stylesheet" href="style.css"></head><body><header><nav class="wrap"><a class="brand" href="index.html">{e(data['name'])}</a><div class="links"><a href="index.html#home">Home</a><a href="index.html#research">Research</a><a href="index.html#publications">Publications</a><a href="cv.html">CV</a></div><button class="menu">☰</button></nav></header><main class="wrap cv-page"><div class="eyebrow">Curriculum vitae</div><h1>CV</h1>{body}</main><script src="main.js"></script></body></html>"""
(ROOT/"cv.html").write_text(cvhtml,encoding="utf-8")
print("Website rebuilt.")
