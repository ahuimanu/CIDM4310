import pandas as pd, numpy as np, re, pathlib, zipfile

BASE = pathlib.Path(".")    # folder containing your CSVs + roster

# Load roster (keep titles)
roster = [ln.strip() for ln in open("WTAMU_COB_Faculty_Names.txt") if ln.strip()]
TITLE_RE = re.compile(r"^(Dr\.|Mr\.|Ms\.|Mrs\.)\s+", re.I)
def strip_title(n): return TITLE_RE.sub("", n).strip()
def norm(n):
    n = strip_title(str(n or ""))
    if "," in n:
        p = [i.strip() for i in n.split(",")]
        if len(p) > 1: n = f"{p[1]} {p[0]}"
    return re.sub(r"\s+"," ",n).lower()
def last_name_key(n):
    base = strip_title(n)
    parts = base.replace(",","").split()
    return parts[-1].lower() if parts else base.lower()
roster_df = pd.DataFrame({"faculty_formal":roster})
roster_df["faculty_norm"] = roster_df["faculty_formal"].map(norm)

# Merge all COB-only CSVs
frames=[]
for f in sorted(BASE.glob("Course_Sections_*_COB_only.csv")):
    df=pd.read_csv(f); df.columns=df.columns.str.strip()
    m=re.search(r"Course_Sections_(\d{4})(FA|SP)_COB_only",f.stem,re.I)
    df["year"],df["term"]=int(m[1]),m[2].upper() if m else (None,None)
    frames.append(df)
sched=pd.concat(frames,ignore_index=True)

# Build full faculty name (Title+First+Last)
def full(r):
    t=str(r.get("Faculty Title","")or"").strip()
    f=str(r.get("Faculty First Name","")or"").strip()
    l=str(r.get("Faculty Last Name","")or"").strip()
    return re.sub(r"\s+"," ",f"{t} {f} {l}".strip())
sched["faculty_full"]=sched.apply(full,axis=1)
sched["faculty_norm"]=sched["faculty_full"].map(norm)
sched=sched.merge(roster_df,on="faculty_norm",how="inner")

# 4️⃣  Standard fields
sched["subject"]=sched["Subject"].astype(str).str.strip().str.upper()
sched["course_no"]=sched["Course No"].astype(str).str.strip()
sched["course_title"]=sched["Short Title"].astype(str).str.strip()
sched["section"]=sched["Sec No"].astype(str).str.strip()
sched["enrollment"]=pd.to_numeric(sched["Active Students"],errors="coerce")

# 5️⃣  Academic year
def ay(t,y): y=int(y); return f"{y}–{y+1}" if t=="FA" else f"{y-1}–{y}"
sched["academic_year"]=[ay(t,y) for t,y in zip(sched["term"],sched["year"])]

# 6️⃣  Cross-listing by course number
sched["num_key"]=sched["course_no"].str.replace(r"\s+","",regex=True).str.upper()
sched["code_compact"]=(sched["subject"]+sched["num_key"]).str.upper()

# 7️⃣  Per-term averages
term_avg=sched.groupby("term")["enrollment"].agg(["sum","count"])
term_avg["cob_overall_avg_term"]=term_avg["sum"]/term_avg["count"]
fac_term=sched.groupby(["faculty_formal","term"])["enrollment"].agg(["sum","count"])
fac_term["faculty_avg_term"]=fac_term["sum"]/fac_term["count"]
fac_term.rename(columns={"sum":"faculty_total_term"},inplace=True)

tight=sched.merge(fac_term,on=["faculty_formal","term"],how="left")
tight=tight.merge(term_avg["cob_overall_avg_term"],on="term",how="left")
tight["delta"]=tight["faculty_avg_term"]-tight["cob_overall_avg_term"]
cols=["faculty_formal","year","term","academic_year","subject","course_no",
      "section","course_title","enrollment","faculty_total_term",
      "faculty_avg_term","cob_overall_avg_term","delta"]
tight.to_csv("WTAMU_COB_Course_Data_2020FA_to_2025SP.csv",index=False)

# 8️⃣  Faculty-Course Summary (merge cross-lists by number)
cl_display=(sched.groupby(["faculty_formal","num_key"])
                 .apply(lambda x:"/".join(sorted(set(x["subject"]+x["num_key"])))).reset_index(name="display_code"))
counts=sched.groupby(["faculty_formal","num_key"]).size().reset_index(name="times_taught")
summary=counts.merge(cl_display,on=["faculty_formal","num_key"])
summary=summary.sort_values(["faculty_formal","display_code"])
lines=["# WTAMU COB Faculty Course Summary (2020FA–2025SP)\n"]
for fac in sorted(summary["faculty_formal"].unique(),key=last_name_key):
    grp=summary[summary["faculty_formal"]==fac]
    lines.append(f"### {fac}\n| Course | Times Taught |\n|---|---|")
    for _,r in grp.iterrows():
        lines.append(f"| {r['display_code']} | {int(r['times_taught'])} |")
    lines.append("")
open("WTAMU_COB_Faculty_Course_Summary.md","w",encoding="utf-8").write("\n".join(lines))

# 9️⃣  Individual + All-in-one reports
def start_year(a): return int(a.split("–")[0])
zipf=zipfile.ZipFile("Faculty_Teaching_Reports.zip","w",zipfile.ZIP_DEFLATED)
fac_order=sorted(roster,key=last_name_key)
for fac in fac_order:
    sub=sched[sched["faculty_formal"]==fac]
    md=[f"### {fac}\n"]
    for ay in sorted(sub["academic_year"].unique(),key=start_year,reverse=True):
        block=sub[sub["academic_year"]==ay]; fy=int(ay.split("–")[0]); sy=fy+1
        md.append(f"#### Academic Year {ay}")
        for label,code,yr in [("Fall","FA",fy),("Spring","SP",sy)]:
            t=block[block["term"]==code]
            if t.empty: md.append(f"*No {label} sections.*")
            else:
                md.append(f"### {label} {yr}\n| Term | Course | Section | Title | Enrollment |\n|---|---|---|---|---|")
                t=t.sort_values(["subject","course_no","section"])
                for _,r in t.iterrows():
                    md.append(f"| {label} | {r['subject']} {r['course_no']} | {r['section']} | {r['course_title']} | {int(r['enrollment']) if not np.isnan(r['enrollment']) else ''} |")
    text="\n".join(md)
    name=re.sub(r"[^A-Za-z0-9]+","_",fac).strip("_")+"_Teaching_Report.md"
    open(name,"w",encoding="utf-8").write(text)
    zipf.write(name)
zipf.close()
open("Faculty_Teaching_Report_All.md","w",encoding="utf-8").write("# Faculty Teaching Report (COB)\n\n"+"\n---\n".join(open(re.sub(r'[^A-Za-z0-9]+','_',f).strip('_')+'_Teaching_Report.md').read() for f in fac_order))
print("All artifacts written.")