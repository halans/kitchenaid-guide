import asyncio,json,pathlib
from playwright.async_api import async_playwright
root=pathlib.Path(__file__).resolve().parents[1]; results=[]
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,args=['--no-sandbox'])
  for width in [1440,390,320,768]:
   page=await browser.new_page(viewport={'width':width,'height':1000},device_scale_factor=1)
   errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   await page.goto((root/'dist'/'index.html').as_uri());await page.evaluate('document.fonts.ready')
   assert await page.locator('.recipe').count()==25
   assert await page.locator('.attachment').count()==9
   overflow=await page.evaluate('document.documentElement.scrollWidth>innerWidth')
   assert not overflow,f'Overflow {width}'
   imgs=await page.evaluate('Array.from(document.images).map(i=>({src:i.getAttribute("src"),ok:i.complete&&i.naturalWidth>0}))')
   # Force-load lazy chapter images before validating.
   await page.evaluate('document.querySelectorAll("img").forEach(i=>i.loading="eager")')
   await page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
   await page.locator('#equipment-filter').select_option('standard')
   assert await page.locator('.recipe:visible').count()==17
   await page.locator('#reset').click();await page.locator('#search').fill('sorbet')
   assert await page.locator('.recipe:visible').count()==2
   await page.locator('#expand').click()
   assert await page.locator('.recipe:visible details.recipe-body[open]').count()==2
   await page.locator('#expand').click()
   assert await page.locator('.recipe:visible details.recipe-body[open]').count()==0
   await page.locator('#search').fill('xxxxx');assert await page.locator('#empty').is_visible()
   await page.locator('#reset').click();await page.locator('#equipment-filter').select_option('roller')
   assert await page.locator('.recipe:visible').count()==2
   await page.locator('#reset').click();await page.locator('#equipment-filter').select_option('icecream')
   assert await page.locator('.recipe:visible').count()==6
   await page.locator('#reset').click();await page.locator('#expand').click()
   assert await page.locator('details.recipe-body[open]').count()==25
   assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth'),f'Expanded overflow {width}'
   await page.locator('#expand').click()
   await page.evaluate('window.scrollTo(0,0)')
   if width in [1440,390]:await page.screenshot(path=f'/tmp/kitchenaid-desktop.png' if width==1440 else '/tmp/kitchenaid-phone.png',full_page=False)
   assert not errors,errors
   results.append({'viewport':width,'recipes':25,'images':5,'horizontalOverflow':False,'filters':'pass','expandCollapse':'pass','consoleErrors':errors})
   await page.close()
  # Ensure direct file no-JavaScript remains useful.
  page=await browser.new_page(java_script_enabled=False,viewport={'width':390,'height':900})
  await page.goto((root/'dist'/'index.html').as_uri());assert await page.locator('.recipe').count()==25
  await page.locator('#pizza-dough details.recipe-body>summary').click()
  assert await page.locator('#pizza-dough .ingredients').is_visible()
  results.append({'javascriptDisabled':'pass','nativeRecipeDrawer':'pass'})
  # Print events expose all recipes and restore a filtered view.
  page=await browser.new_page(viewport={'width':390,'height':900})
  await page.goto((root/'dist'/'index.html').as_uri());await page.locator('#search').fill('sorbet')
  await page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
  assert await page.locator('details.recipe-body[open]').count()==25
  assert await page.locator('.recipe:visible').count()==25
  await page.evaluate('window.dispatchEvent(new Event("afterprint"))')
  assert await page.locator('.recipe:visible').count()==2
  assert await page.locator('details.recipe-body[open]').count()==0
  results.append({'printExpansionAndRestoration':'pass'})
  # Fully embedded publication version must make no network requests.
  page=await browser.new_page(viewport={'width':1440,'height':900});requests=[]
  page.on('request',lambda r:requests.append(r.url) if r.url.startswith('http') else None)
  await page.goto((root/'dist'/'page-online.html').as_uri());await page.evaluate('document.fonts.ready');assert not requests,requests
  results.append({'onlineNetworkRequests':0,'selfContained':'pass'})
  await browser.close()
 pathlib.Path('/tmp/kitchenaid-browser-tests.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
asyncio.run(main())
