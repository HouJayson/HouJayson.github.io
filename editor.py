from pathlib import Path
import json, shutil, subprocess, sys, webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
ROOT=Path(__file__).resolve().parent
DATA=ROOT/"content.json"
ASSETS=ROOT/"assets"

def load():
    return json.loads(DATA.read_text(encoding="utf-8"))
data=load()

app=tk.Tk()
app.title("Jixin Hou — Local Website Editor")
app.geometry("940x720")
app.minsize(820,620)

style=ttk.Style()
try: style.theme_use("vista")
except: pass

nb=ttk.Notebook(app); nb.pack(fill="both",expand=True,padx=14,pady=14)
home=ttk.Frame(nb,padding=18); research=ttk.Frame(nb,padding=18); pubs=ttk.Frame(nb,padding=18); settings=ttk.Frame(nb,padding=18)
nb.add(home,text="Home"); nb.add(research,text="Research"); nb.add(pubs,text="Publications"); nb.add(settings,text="CV & Links")

vars={}
def field(parent,label,key,row,width=70):
    ttk.Label(parent,text=label).grid(row=row,column=0,sticky="nw",pady=7)
    v=tk.StringVar(value=data.get(key,"")); vars[key]=v
    ent=ttk.Entry(parent,textvariable=v,width=width); ent.grid(row=row,column=1,sticky="ew",pady=7,padx=(12,0))
    return ent

home.columnconfigure(1,weight=1)
field(home,"Name","name",0); field(home,"Main title","tagline",1); field(home,"Subtitle","subtitle",2)
ttk.Label(home,text="Introduction").grid(row=3,column=0,sticky="nw",pady=7)
intro=tk.Text(home,height=7,wrap="word"); intro.insert("1.0",data["intro"]); intro.grid(row=3,column=1,sticky="nsew",pady=7,padx=(12,0))
home.rowconfigure(3,weight=1)
hero_var=tk.StringVar(value=data.get("hero_image","assets/hero_brain.svg"))
ttk.Label(home,text="Hero image").grid(row=4,column=0,sticky="w",pady=7)
hf=ttk.Frame(home); hf.grid(row=4,column=1,sticky="ew",padx=(12,0))
ttk.Entry(hf,textvariable=hero_var).pack(side="left",fill="x",expand=True)
def choose_hero():
    f=filedialog.askopenfilename(title="Choose hero image",filetypes=[("Images","*.png *.jpg *.jpeg *.webp *.svg"),("All files","*.*")])
    if f:
        src=Path(f); dst=ASSETS/("hero"+src.suffix.lower()); shutil.copy2(src,dst); hero_var.set("assets/"+dst.name)
ttk.Button(hf,text="Choose…",command=choose_hero).pack(side="left",padx=(8,0))

# research editing
research.columnconfigure(1,weight=1)
r_title=[]; r_text=[]
for i,r in enumerate(data["research"]):
    ttk.Label(research,text=f"Research {i+1} title").grid(row=i*2,column=0,sticky="nw",pady=6)
    tv=tk.StringVar(value=r["title"]); r_title.append(tv)
    ttk.Entry(research,textvariable=tv).grid(row=i*2,column=1,sticky="ew",padx=(12,0),pady=6)
    ttk.Label(research,text="Description").grid(row=i*2+1,column=0,sticky="nw",pady=6)
    tx=tk.Text(research,height=4,wrap="word"); tx.insert("1.0",r["text"]); tx.grid(row=i*2+1,column=1,sticky="ew",padx=(12,0),pady=6); r_text.append(tx)

# publications tree
pubs.columnconfigure(0,weight=1); pubs.rowconfigure(1,weight=1)
ttk.Label(pubs,text="Selected publications shown on the site. Double-click an entry to edit it.").grid(row=0,column=0,sticky="w",pady=(0,8))
tree=ttk.Treeview(pubs,columns=("year","journal","title"),show="headings",selectmode="browse")
tree.heading("year",text="Year"); tree.heading("journal",text="Journal"); tree.heading("title",text="Title")
tree.column("year",width=70,anchor="center"); tree.column("journal",width=190); tree.column("title",width=560)
tree.grid(row=1,column=0,sticky="nsew")
scroll=ttk.Scrollbar(pubs,orient="vertical",command=tree.yview); scroll.grid(row=1,column=1,sticky="ns"); tree.configure(yscrollcommand=scroll.set)
def refresh_tree():
    for x in tree.get_children(): tree.delete(x)
    for i,p in enumerate(data["publications"]): tree.insert("", "end", iid=str(i), values=(p["year"],p["journal"],p["title"]))
refresh_tree()

def edit_pub(index=None):
    if index is None:
        p={"year":"","title":"","authors":"","journal":"","url":"","summary":"","image":"assets/pub_folding.svg","first_author":True}
    else: p=dict(data["publications"][index])
    w=tk.Toplevel(app); w.title("Publication"); w.geometry("720x580"); w.transient(app); w.grab_set()
    frm=ttk.Frame(w,padding=16); frm.pack(fill="both",expand=True); frm.columnconfigure(1,weight=1)
    entries={}
    labels=["year","title","authors","journal","url","summary","image"]
    for r,k in enumerate(labels):
        ttk.Label(frm,text=k.replace("_"," ").title()).grid(row=r,column=0,sticky="nw",pady=6)
        v=tk.StringVar(value=p.get(k,"")); entries[k]=v
        ttk.Entry(frm,textvariable=v).grid(row=r,column=1,sticky="ew",padx=(10,0),pady=6)
    def choose_thumb():
        f=filedialog.askopenfilename(title="Choose publication figure",filetypes=[("Images","*.png *.jpg *.jpeg *.webp *.svg"),("All files","*.*")])
        if f:
            src=Path(f); safe="pub_custom_"+str(len(data["publications"])+1)+src.suffix.lower(); dst=ASSETS/safe; shutil.copy2(src,dst); entries["image"].set("assets/"+dst.name)
    ttk.Button(frm,text="Choose figure…",command=choose_thumb).grid(row=7,column=1,sticky="w",padx=(10,0),pady=6)
    def savep():
        new={k:v.get().strip() for k,v in entries.items()}; new["first_author"]=True
        if not new["title"]: messagebox.showerror("Missing title","Please enter a title."); return
        if index is None: data["publications"].append(new)
        else: data["publications"][index]=new
        refresh_tree(); w.destroy()
    ttk.Button(frm,text="Save publication",command=savep).grid(row=8,column=1,sticky="e",padx=(10,0),pady=14)
def selected_index():
    s=tree.selection()
    return int(s[0]) if s else None
def do_edit(event=None):
    i=selected_index()
    if i is not None: edit_pub(i)
tree.bind("<Double-1>",do_edit)
bar=ttk.Frame(pubs); bar.grid(row=2,column=0,sticky="w",pady=10)
ttk.Button(bar,text="Add",command=lambda:edit_pub()).pack(side="left")
ttk.Button(bar,text="Edit",command=do_edit).pack(side="left",padx=6)
def delete_pub():
    i=selected_index()
    if i is not None and messagebox.askyesno("Delete","Remove selected publication from the website?"):
        data["publications"].pop(i); refresh_tree()
ttk.Button(bar,text="Delete",command=delete_pub).pack(side="left")

# settings
settings.columnconfigure(1,weight=1)
emailv=tk.StringVar(value=data.get("email","")); scholarv=tk.StringVar(value=data.get("scholar","")); githubv=tk.StringVar(value=data.get("github","")); cvv=tk.StringVar(value=data.get("cv_path",""))
for row,(lab,v) in enumerate([("Email",emailv),("Google Scholar",scholarv),("GitHub",githubv),("CV file",cvv)]):
    ttk.Label(settings,text=lab).grid(row=row,column=0,sticky="w",pady=8); ttk.Entry(settings,textvariable=v).grid(row=row,column=1,sticky="ew",padx=(12,0),pady=8)
def choose_cv():
    f=filedialog.askopenfilename(title="Choose CV PDF",filetypes=[("PDF","*.pdf")])
    if f:
        src=Path(f); dst=ASSETS/"Jixin_Hou_CV.pdf"; shutil.copy2(src,dst); cvv.set("assets/Jixin_Hou_CV.pdf")
ttk.Button(settings,text="Choose CV PDF…",command=choose_cv).grid(row=4,column=1,sticky="w",padx=(12,0),pady=8)

bottom=ttk.Frame(app,padding=(14,0,14,14)); bottom.pack(fill="x")
status=tk.StringVar(value="Edit locally, then Save & Build.")
ttk.Label(bottom,textvariable=status).pack(side="left")
def save_build(open_after=False):
    data["name"]=vars["name"].get().strip()
    data["tagline"]=vars["tagline"].get().strip()
    data["subtitle"]=vars["subtitle"].get().strip()
    data["intro"]=intro.get("1.0","end").strip()
    data["hero_image"]=hero_var.get().strip()
    data["email"]=emailv.get().strip(); data["scholar"]=scholarv.get().strip(); data["github"]=githubv.get().strip(); data["cv_path"]=cvv.get().strip()
    for i in range(len(data["research"])):
        data["research"][i]["title"]=r_title[i].get().strip()
        data["research"][i]["text"]=r_text[i].get("1.0","end").strip()
    DATA.write_text(json.dumps(data,indent=2),encoding="utf-8")
    try:
        subprocess.run([sys.executable,str(ROOT/"build_site.py")],check=True,cwd=ROOT)
        status.set("Saved and rebuilt successfully.")
        if open_after: webbrowser.open((ROOT/"index.html").as_uri())
    except Exception as ex:
        messagebox.showerror("Build failed",str(ex))
ttk.Button(bottom,text="Preview",command=lambda:save_build(True)).pack(side="right",padx=(8,0))
ttk.Button(bottom,text="Save & Build",command=lambda:save_build(False)).pack(side="right")

app.mainloop()
