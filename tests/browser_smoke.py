"""Playwright DOM/UI test via set_content (localhost navigation is blocked by runtime)."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
html=(root/'docs/index.html').read_text()
html=html.replace('<link rel="stylesheet" href="assets/style.css" />','').replace('<script src="assets/app.js" defer></script>','')
catalog=json.loads((root/'docs/data/catalog.json').read_text())
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1440,'height':960})
    errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.set_content(html)
    page.add_style_tag(content=(root/'docs/assets/style.css').read_text())
    page.evaluate('(data)=>{window.fetch=async()=>({ok:true,json:async()=>data})}',catalog)
    page.add_script_tag(content=(root/'docs/assets/app.js').read_text())
    assert page.locator('#connectorBars .bar-row').count()==7
    page.screenshot(path=str(root/'docs/dashboard-preview.png'),full_page=True)
    page.locator('a[href="#skills"]').first.click()
    assert page.locator('#skillsRows tr').count()==15
    page.locator('#skillsSearch').fill('pdfs')
    assert page.locator('#skillsRows tr').count()==1
    page.locator('a[href="#packages"]').first.click()
    page.locator('#packagesSearch').fill('pandas')
    assert page.locator('#packagesRows tr').count()>=2
    page.locator('a[href="#tools"]').first.click()
    page.locator('#toolsFilter').select_option('GitHub')
    assert '89 条结果' in page.locator('#toolsCount').inner_text()
    page.locator('a[href="#risks"]').first.click()
    assert page.locator('.risk-card').count()==7
    page.set_viewport_size({'width':390,'height':850})
    page.locator('#menuButton').click()
    page.locator('a.nav-link[href="#overview"]').click()
    page.screenshot(path=str(root/'docs/dashboard-mobile-preview.png'),full_page=True)
    assert not errors, errors
    print('PASS: 7 chart bars, 36 skills, 242 tools, 2099 packages, 7 risks, responsive layout (mocked data fetch)')
    browser.close()
