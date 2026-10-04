#!/usr/bin/env python3
"""Offline structural and cross-surface equivalence tests, Python standard library only."""
import unittest,json,pathlib,re,base64,html.parser
import build
ROOT=pathlib.Path(__file__).resolve().parent
DIST=ROOT/'dist'
class Page(html.parser.HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=[];self.images=[];self.links=[];self.recipe_count=0;self.attachment_count=0;self.attrs=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.attrs.append((tag,a))
  if 'id' in a:self.ids.append(a['id'])
  if tag=='img':self.images.append(a)
  if tag=='a':self.links.append(a)
  if 'recipe' in a.get('class','').split():self.recipe_count+=1
  if 'attachment' in a.get('class','').split():self.attachment_count+=1
class GuideTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.recipes=json.loads((ROOT/'data/recipes.json').read_text());cls.offline=build.render()['offline'];cls.online=(DIST/'index.html').read_text();cls.page=Page(cls.offline)
 def test_data_shape(self):
  self.assertEqual(len(self.recipes),25)
  for r in self.recipes:
   for key in ['id','title','category','equipment','bowl','requirement','yield','time','intro','ingredients','steps','cue','troubleshoot','sources','note']:self.assertTrue(r[key],(r['id'],key))
   for s in r['sources']:self.assertTrue(s['url'].startswith('https://'))
 def test_counts(self):
  self.assertEqual(self.page.recipe_count,25);self.assertEqual(self.page.attachment_count,9);self.assertEqual(len(self.page.images),5)
 def test_unique_ids(self):self.assertEqual(len(self.page.ids),len(set(self.page.ids)))
 def test_external_link_security(self):
  for a in self.page.links:
   if a.get('href','').startswith('http'):
    self.assertEqual(a.get('target'),'_blank');self.assertIn('noopener',a.get('rel',''));self.assertIn('noreferrer',a.get('rel',''))
 def test_internal_links(self):
  for a in self.page.links:
   if a.get('href','').startswith('#'):self.assertIn(a['href'][1:],self.page.ids)
 def test_assets_exist(self):
  for im in self.page.images:self.assertTrue((ROOT/im['src']).exists());self.assertTrue(im.get('alt'))
  for asset in re.findall(r'url\((assets/[^)]+)\)',self.offline):self.assertTrue((ROOT/asset).exists())
 def test_rebuild_is_current(self):
  for name,content in build.build().items():self.assertEqual((DIST/name).read_text(),content)
 def test_online_offline_equivalence(self):
  normalized=self.online
  for path in set(re.findall(r'(?:src="|url\()(assets/[^"\)]+)',self.offline)):
   data=(ROOT/path).read_bytes();mime='image/jpeg' if path.endswith('.jpg') else 'font/ttf';url='data:'+mime+';base64,'+base64.b64encode(data).decode();self.assertIn(url,normalized);normalized=normalized.replace(url,path)
  self.assertEqual(normalized,self.offline)
 def test_no_external_runtime_dependencies(self):
  for text in [self.offline,self.online]:
   p=Page(text)
   for tag,a in p.attrs:
    if tag in ['script','img','link']:self.assertFalse(a.get('src',a.get('href','')).startswith('http'))
 def test_equipment_counts(self):
  self.assertEqual(sum(r['requirement']=='standard' for r in self.recipes),17);self.assertEqual(sum(r['requirement']=='roller' for r in self.recipes),2);self.assertEqual(sum(r['requirement']=='icecream' for r in self.recipes),6)
 def test_food_safety_guards(self):
  self.assertIn('speed 2, never faster',self.offline);self.assertIn('1.4 L',self.offline);self.assertIn('≥24 h',self.offline);self.assertIn('Do not taste raw',self.offline);self.assertIn('not kitchen-tested',self.offline)
 def test_ksm195_profile(self):
  self.assertIn('id="your-mixer"',self.offline);self.assertIn('≤2 kg',self.offline);self.assertIn('2.8 L',self.offline);self.assertIn('4 bowl tools',self.offline)
 def test_ksm195_recipe_tools(self):
  recipes={r['id']:r for r in self.recipes}
  self.assertIn('pastry beater',recipes['shredded-chicken']['equipment']);self.assertIn('pastry beater',recipes['shortcrust-pastry']['equipment'])
  self.assertIn('flex-edge beater',recipes['vanilla-butter-cake']['equipment'])
  for key in ['pizza-dough','sandwich-bread','rosemary-focaccia','overnight-brioche']:
   self.assertFalse(any('Stir' in step for step in recipes[key]['steps']),key)
 def test_ksm195_cleaning_and_compatibility(self):
  self.assertIn('hand-wash the supplied wire whisk',self.offline);self.assertIn('5KSMICM explicitly fits KSM195',self.offline)
  self.assertIn('KSMPRA',self.offline);self.assertIn('KSM192_195_Manual_W11556021C',self.offline)
 def test_basic_no_churn_ice_cream(self):
  r=next(r for r in self.recipes if r['id']=='basic-vanilla-ice-cream')
  self.assertEqual(r['requirement'],'standard');self.assertEqual(len(r['ingredients']),3)
  self.assertIn('wire whisk',r['equipment']);self.assertIn('no ice-cream attachment',r['equipment'])
  self.assertTrue(any(r['id']=='basic-vanilla-ice-cream' for r in self.recipes))
 def test_crepe_batter(self):
  r=next(r for r in self.recipes if r['id']=='crepe-batter')
  self.assertEqual(r['requirement'],'standard');self.assertEqual(r['category'],'batter')
  self.assertIn('100 ml water',r['ingredients']);self.assertIn('flex-edge beater',r['equipment'])
  self.assertTrue(any('30 minutes' in s for s in r['steps']));self.assertTrue(any('flip' in s for s in r['steps']))
 def test_quick_churn_vanilla(self):
  r=next(r for r in self.recipes if r['id']=='quick-churn-vanilla')
  self.assertEqual(r['requirement'],'icecream');self.assertEqual(len(r['ingredients']),4)
  self.assertIn('BEFORE',r['steps'][2]);self.assertIn('Serve straight away',r['steps'][-1])
  self.assertEqual(next(r for r in self.recipes if r['category']=='frozen')['id'],r['id'])
if __name__=='__main__':unittest.main(verbosity=2)
