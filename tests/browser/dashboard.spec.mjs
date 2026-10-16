import {test,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import {readFile} from 'node:fs/promises';
test('full-year totals reconcile with exported Python results and filters update metrics',async({page})=>{
 const errors=[];page.on('pageerror',e=>errors.push(e.message));await page.goto('/');await expect(page.locator('#status')).toContainText('order selesai');
 const summary=JSON.parse(await readFile('reports/summary.json','utf8'));const format=n=>new Intl.NumberFormat('id-ID',{style:'currency',currency:'IDR',maximumFractionDigits:0}).format(n);
 await expect(page.locator('#net-exact')).toHaveText(format(summary.metrics.net));
 await page.locator('#category').selectOption('Books');await page.locator('#channel').selectOption('Web');await page.locator('#start').fill('2025-12-01');await page.locator('#start').dispatchEvent('change');
 const expected=await page.evaluate(async()=>{const {summarize,filterRows}=await import('./metrics.js');const d=await fetch('data.json').then(r=>r.json());return summarize(filterRows(d.rows.map(r=>Object.fromEntries(d.columns.map((c,i)=>[c,r[i]]))),{category:'Books',channel:'Web',start:'2025-12-01',end:'2025-12-31'}));});
 await expect(page.locator('#net-exact')).toHaveText(format(expected.net));
 await page.locator('#start').fill('2025-01-01');await page.locator('#end').fill('2025-01-01');await page.locator('#end').dispatchEvent('change');await expect(page.locator('#net-exact')).toHaveText(format(0));await expect(page.locator('#status')).toContainText('Tidak ada order');
 await page.locator('#reset').click();await expect(page.locator('#net-exact')).toHaveText(format(summary.metrics.net));expect(errors).toEqual([]);
});
for(const width of [360,768,1440])test(`layout and accessibility at ${width}px`,async({page},info)=>{
 await page.setViewportSize({width,height:950});await page.goto('/');await expect(page.locator('#status')).toContainText('order selesai');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
 const audit=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();expect(audit.violations).toEqual([]);
 await page.screenshot({path:info.outputPath(`dashboard-${width}.png`),fullPage:true});
 await page.keyboard.press('Tab');await expect(page.locator('.skip')).toBeFocused();
});
test('data downloads resolve and invalid dates explain their state',async({page,request})=>{
 await page.goto('/');await expect(page.locator('#status')).toContainText('order selesai');
 for(const file of ['insights.md','quality.csv','data.json'])expect((await request.get('/'+file)).status()).toBe(200);
 await page.locator('#start').fill('2025-12-31');await page.locator('#end').fill('2025-01-01');await page.locator('#end').dispatchEvent('change');await expect(page.locator('#status')).toContainText('Tanggal mulai');
});
test('currency digits remain together on small-screen KPI cards',async({page})=>{
 await page.setViewportSize({width:360,height:950});await page.goto('/');await expect(page.locator('#status')).toContainText('order selesai');
 for(const id of ['net','aov']){
  const y=await page.locator('#'+id).evaluate(el=>{const node=el.firstChild;const result=[];for(let i=0;i<node.textContent.length;i++)if(/\d/.test(node.textContent[i])){const r=document.createRange();r.setStart(node,i);r.setEnd(node,i+1);result.push(Math.round(r.getBoundingClientRect().y));}return [...new Set(result)];});
  expect(y).toHaveLength(1);
 }
});
