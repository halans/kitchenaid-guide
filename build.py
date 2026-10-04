#!/usr/bin/env python3
"""Build the self-contained online HTML page into dist/index.html from the data/template. No dependencies."""
import pathlib,json,html,base64,re,argparse,sys
ROOT=pathlib.Path(__file__).resolve().parent
DIST=ROOT/'dist'
def esc(s):return html.escape(str(s),quote=True)
def link(url,title):return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(title)} ↗</a>'
assets={a['id']:a for a in json.loads((ROOT/'assets/manifest.json').read_text())}
def img(name,hero=False):
 a=assets[name]
 load='fetchpriority="high"' if hero else 'loading="lazy"'
 return f'<figure class="{ "hero-photo" if hero else "chapter-photo" }"><img src="{a["path"]}" alt="{esc(a["alt"])}" width="{a["width"]}" height="{a["height"]}" {load}><figcaption>Photo · {link(a["source"],a["credit"])}</figcaption></figure>'
def recipe(r,n):
 labels={'standard':'Standard tools','roller':'Pasta roller required','icecream':'Ice-cream bowl required'}
 search=' '.join([r['title'],r['intro'],r['equipment'],r['category']]+r['ingredients']).lower()
 steps=''.join(f'<li>{esc(x)}</li>' for x in r['steps']);ingredients=''.join(f'<li>{esc(x)}</li>' for x in r['ingredients']);sources=''.join(f'<li>{link(s["url"],s["title"])}</li>' for s in r['sources'])
 note=r['note'].replace('Standard-tool savoury preparation grouped under batter for this four-category collection. ','')
 return f'''<article class="recipe" id="{esc(r['id'])}" data-search="{esc(search)}" data-requirement="{r['requirement']}"><div class="recipe-head"><div class="recipe-top"><span class="tag">{labels[r['requirement']]}</span><span class="recipe-number">{n:02d} / 25</span></div><h3>{esc(r['title'])}</h3><p>{esc(r['intro'])}</p><p class="yield">Makes {esc(r['yield']).rstrip('.')}</p></div><details class="recipe-body"><summary>Ingredients & method<span class="sr-only"> — {esc(r['title'])}</span></summary><div class="recipe-content"><p class="small-label">Allow time</p><p class="equipment">{esc(r['time'])}</p><p class="equipment"><strong>Bowl:</strong> {esc(r['bowl'])}</p><p class="equipment"><strong>Equipment:</strong> {esc(r['equipment'])}</p><p class="small-label">The ingredients</p><ul class="ingredients">{ingredients}</ul><p class="small-label">The method</p><ol class="method">{steps}</ol><p class="endpoint"><strong>The endpoint:</strong> {esc(r['cue'])}</p><p class="small-label">If it goes wrong</p><p class="trouble">{esc(r['troubleshoot'])}</p><details class="sources"><summary>Sources & adaptation notes</summary><ul>{sources}</ul><p>{esc(note)}</p></details></div></details></article>'''
chapters=[
 ('dough','01','Dough & pastry','Strength for bread.<br>Restraint for pastry.','Bread needs gluten; pastry needs tenderness. The same mixer can make both, but not with the same tool or the same finish.','A wet dough can cling to the bowl and still be ready.','bread','#ff9569'),
 ('batter','02','Batter & baking','Put the air in.<br>Then keep it there.','Creaming butter is deliberate aeration. Once flour arrives, gentleness takes over. Meringue is the other end of the spectrum: the whisk builds the structure.','Cream before flour. Brief mixing after flour.','batter','#e4c679'),
 ('pasta','03','Fresh pasta','A little flour.<br>A little patience.','The mixer brings dough together. Resting makes it workable; rolling makes it thin. Cut tagliatelle by hand, use the cutter for fettuccine, or shape semolina dough on the bench.','KSM195 + optional KSMPRA. Mixer speed ≠ thickness dial.','pasta','#bed09d'),
 ('frozen','04','Ice cream, gelato & sorbet','Cold bowl ready?<br>Churn and eat.','The first recipe is a cold, no-cook base for soft-serve straight after churning. There is also a no-churn option, plus richer bases and sorbets. Sugar and fat are part of the structure, not just the flavour.','Start the dasher on Stir before pouring in cold base.','frozen','#a8cfd9'),
 ('everyday','05','Everyday bowl jobs','Not everything<br>needs an attachment.','Cream, butter, mash and cooked chicken all use the familiar bowl tools. The stove still cooks; the mixer only supplies the movement.','Thirty seconds can be enough. Watch the texture.',None,'#bed09d')]
def section(ch,recipes):
 id,num,name,title,intro,principle,photo,accent=ch
 subset=[r for r in recipes if r['category']==id]
 art=img(photo) if photo else '<div class="everyday-art"><span>The same bowl, four jobs</span>Whip cream.<br>Churn butter.<br>Mash potatoes.<br>Shred chicken.</div>'
 extra=''
 if id=='pasta':extra='<div class="rulebox"><p><strong>For the documented KSMPRA family:</strong> roller speed 2, fettuccine cutter 5, spaghetti cutter 7. Start thickness dial at 1 and progress gradually; dial 4–5 suits many sheet recipes. Follow your own attachment manual. A pasta press is a different tool with different dough and speeds.</p></div><div style="height:25px"></div>'
 if id=='frozen':extra='''<p class="rulebox"><strong>Start simple:</strong> the first recipe uses the fully frozen attachment bowl and is ready to eat as soft-serve after churning. The condensed-milk no-churn recipe uses only the whisk and freezer. Bowl preparation below applies only to the six churned recipes.</p><div class="prep-strip"><div><b>≥24 h</b><p>Freeze bowl fully. Follow the exact manual if longer.</p></div><div><b>≤4°C</b><p>Chill the base. Room temperature is not cold enough.</p></div><div><b>20–30 min</b><p>Churn on Stir to soft-serve texture, not to a fixed timer.</p></div><div><b>Optional 2–4 h</b><p>Freeze for firm scoops. For immediate soft-serve, skip hardening and eat after churning.</p></div></div><div class="rulebox"><p><strong>1.9 L finished is not 1.9 L liquid.</strong> KitchenAid’s guidance limits starting base to 1.4 L; these recipes are smaller. The AU bowl page says 16 hours minimum freeze time; this guide allows 24 hours for planning. Measure cooled base and follow your exact bowl manual. The optional AU 5KSMICM explicitly fits KSM195; it replaces your normal bowl and uses its own dasher and drive. It is not a universal hub accessory. Fully refreeze between batches.</p></div><div style="height:25px"></div>'''
 return f'<section class="category {id}" id="{id}" style="--accent:{accent}"><div class="wrap"><div class="section-intro"><div><p class="section-num">{num} / {name} · {len(subset)} recipes</p><h2>{title}</h2><p class="intro">{intro}</p><p class="principle">{principle}</p></div>{art}</div>{extra}<div class="recipes">'+''.join(recipe(r,recipes.index(r)+1) for r in subset)+'</div></div></section>'
def render():
 recipes=json.loads((ROOT/'data/recipes.json').read_text()); attachments=json.loads((ROOT/'data/attachments.json').read_text())
 fontcss=(ROOT/'assets/fonts/fonts.css').read_text();template=(ROOT/'template.html').read_text();fontcss += '\n.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}\n'
 parts={'@@FONTS@@':fontcss,'@@HERO@@':img('bread',True),'@@SECTIONS@@':''.join(section(ch,recipes) for ch in chapters),'@@ATTACHMENTS@@':''.join(f'<article class="attachment"><p class="small-label">{esc(a["label"])}</p><h3>{esc(a["title"])}</h3><p>{esc(a["does"])}</p><p class="limit">{esc(a["limit"])}</p>{link(a["url"],"Equipment & instructions")}</article>' for a in attachments),'@@CREDITS@@':''.join(f'<li>{link(a["source"],a["credit"]+" · "+a["id"]+" photograph")}</li>' for a in assets.values())}
 offline=template
 for key,value in parts.items():offline=offline.replace(key,value)
 if re.search(r'@@\w+@@',offline):raise ValueError('Unreplaced template token')
 online=offline
 paths=set(re.findall(r'(?:src="|url\()(assets/[^"\)]+)',online))
 for path in paths:
  data=(ROOT/path).read_bytes();mime='image/jpeg' if path.endswith('.jpg') else 'font/ttf'
  online=online.replace(path,'data:'+mime+';base64,'+base64.b64encode(data).decode())
 return {'offline':offline,'online':online}
def build():return {'index.html':render()['online']}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args();outputs=build();bad=[]
 for name,content in outputs.items():
  path=DIST/name
  if args.check:
   if not path.exists() or path.read_text()!=content:bad.append(name)
  else:DIST.mkdir(exist_ok=True);path.write_text(content)
 if bad:print('Stale: '+', '.join(bad));return 1
 print(('Verified' if args.check else 'Built')+' self-contained online page into dist/index.html.');return 0
if __name__=='__main__':sys.exit(main())
